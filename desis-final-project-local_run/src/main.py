import os
from neural_intents import GenericAssistant
import matplotlib.pyplot as plt
import yfinance as yf
import pickle
import sys
import datetime as dt
import plotly.graph_objects as go
import telebot
from io import StringIO
import pandas as pd

with open('portfolio.pkl', 'rb') as f:
    portfolio = pickle.load(f)

# Your own bot token
BOT_TOKEN = "6139937589:AAEPEhmEBgPcpv--RGLCIPNPoMQsCufhH9U"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print(f"Received message: {message.text}")
    add_reply, prob, reply_msg = assistant.request(message.text, message)
    print(F"Probability: {prob}")
    if add_reply:
        bot.reply_to(message, str(reply_msg))

# Handle document uploads.


@bot.message_handler(func=lambda msg: True, content_types=['document'])
def command_handle_any_document(message):
    # This is a file upload.
    file_url = bot.get_file_url(message.document.file_id)
    print(f"Downloading {file_url}")
    try:
        df = pd.read_csv(file_url)
        str_io = StringIO()
        df.to_html(buf=str_io, classes='table table-striped')
        str_io.seek(0)
        bot.send_document(message.chat.id, str_io,
                          visible_file_name="analysis_report.html")
        bot.send_message(message.chat.id, "Analysis complete!")
        return
    except Exception as e:
        print(f"Error in reading file {e}")
        bot.reply_to(
            message, "Cannot read the uploaded file. Please try again.")


def save_portfolio():
    with open('portfolio.pkl', 'wb') as f:
        pickle.dump(portfolio, f)

# ADDING TO PORTFOLIO


def add_portfolio(message):
    stock_name = bot.reply_to(
        message, "Which stock do you want to buy?")
    bot.register_next_step_handler(stock_name, add_stock_name_handler)


def add_stock_name_handler(message):
    stock_name = message.text
    stock_number = bot.reply_to(
        message, f"How many stocks of {stock_name} do you want to buy?")
    # Next message will call the age_handler function
    bot.register_next_step_handler(
        stock_number, add_stock_number_handler, stock_name)


def add_stock_number_handler(message, stock_name):
    stock_number = message.text
    if stock_name in portfolio.keys():
        portfolio[stock_name] += int(stock_number)
    else:
        portfolio[stock_name] = int(stock_number)
    save_portfolio()

    bot.send_message(
        message.chat.id, f"You have bought {stock_number} shares of {stock_name}.")


# REMOVE TO PORTFOLIO
def remove_portfolio(message):
    stock_name = bot.reply_to(
        message, "Which stock do you want to sell?")
    bot.register_next_step_handler(stock_name, remove_stock_name_handler)


def remove_stock_name_handler(message):
    stock_name = message.text
    stock_number = bot.reply_to(
        message, f"How many stocks of {stock_name} do you want to sell?")
    # Next message will call the age_handler function
    bot.register_next_step_handler(
        stock_number, remove_stock_number_handler, stock_name)


def remove_stock_number_handler(message, stock_name):
    stock_number = message.text
    if stock_name in portfolio.keys():
        if int(stock_number) <= portfolio[stock_name]:
            portfolio[stock_name] -= int(stock_number)
        else:
            bot.send_message(
                message.chat.id, f"You don't have enough shares of {stock_name}")
    else:
        bot.send_message(
            message.chat.id, f"You don't have enough shares of {stock_name}")
    for stock, count in list(portfolio.items()):
        if count == 0:
            del portfolio[stock]
    save_portfolio()

    bot.send_message(
        message.chat.id, f"You have sold {stock_number} shares of {stock_name}.")


def show_portfolio(message):
    bot.reply_to(message, "This is your portfolio:")
    for stock in portfolio.keys():
        bot.send_message(
            message.chat.id, f"You own {portfolio[stock]} shares of {stock}")


def portfolio_worth(message):
    if len(portfolio) == 0:
        bot.reply_to(message, "You have no stocks in your portfolio!")
        return
    portfolio_value = 0
    prices = yf.download(list(portfolio.keys()), period="1d")[
        "Adj Close"].iloc[-1]

    portfolio_value = sum(prices * pd.Series(portfolio))
    bot.reply_to(message, f"Your portfolio is worth ${portfolio_value}")


def portfolio_gains(message):
    if len(portfolio) == 0:
        print('You have no stocks in your portfolio!')
        return
    date = bot.reply_to(
        message, "Enter a date for comparison (YYYY-MM-DD): ")
    bot.register_next_step_handler(date, portfolio_gains_handler)


def portfolio_gains_handler(message):
    starting_date = message.text
    sum_now = 0
    sum_then = 0

    try:
        for stock in portfolio.keys():
            data = yf.download(stock, start=starting_date,
                               end=dt.datetime.now())
            price_now = data['Close'].iloc[-1]
            price_then = data.loc[data.index ==
                                  starting_date]['Close'].values[0]
            sum_now += (price_now * portfolio[stock])
            sum_then += (price_then * portfolio[stock])
        bot.reply_to(
            message, f"Relative Gains: {((sum_now - sum_then)/sum_then)*100}")
        bot.reply_to(
            message, f"Absolute Gains: ${sum_now - sum_then}")

    except IndexError:
        bot.reply_to(
            message, "There was no trading on this day")


def plot_chart(message):
    stock_name = bot.reply_to(
        message, "Which stock do you want to plot?")
    bot.register_next_step_handler(stock_name, plotting_handler1)


def plotting_handler1(message):
    stock_name = message.text
    starting_date = bot.reply_to(
        message, "Choose a starting date (DD/MM/YYYY): ")
    bot.register_next_step_handler(
        starting_date, plotting_handler2, stock_name)


def plotting_handler2(message, stock_name):
    starting_date = message.text
    time_interval = bot.reply_to(
        message, "Enter intervals(Eg: 1mo, 1d, 1h, 15m): ")
    bot.register_next_step_handler(
        time_interval, plotting_handler3, stock_name, starting_date)


def plotting_handler3(message, stock_name, starting_date):
    time_interval = message.text
    plt.style.use('dark_background')

    start_ = dt.datetime.strptime(starting_date, "%d/%m/%Y")
    end_ = dt.datetime.now()

    df = yf.download(stock_name, start=start_,
                     end=end_, interval=time_interval)
    print(df)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df.Open, high=df.High, low=df.Low, close=df.Close)])
    fig.show()


def bye(message):
    bot.send_message(message.chat.id, "Goodbye!")
    sys.exit(0)


def default_handler(message):
    bot.reply_to(message, "I did not understand.")


mappings = {
    'plot_chart': plot_chart,
    'add_portfolio': add_portfolio,
    'remove_portfolio': remove_portfolio,
    'show_portfolio': show_portfolio,
    'portfolio_worth': portfolio_worth,
    'portfolio_gains': portfolio_gains,
    'bye': bye,
    None: default_handler
}

assistant = GenericAssistant(
    'src/intents.json', mappings, "financial_assitant_model")

assistant.train_model()
assistant.save_model()


bot.infinity_polling()
