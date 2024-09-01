# Financial Advisory Chatbot

Welcome to the Financial Advisory Chatbot project! This project was developed by **Group 4** (JUNIHERS GROUP 4) under the mentorship of **Sandeep Manthi**. The chatbot is designed to help users with personal finance management through an easy-to-use Telegram interface. It offers features like portfolio management, real-time market information, goal setting, and more.

## Project Overview

### Introduction
Finance management is a critical aspect of daily life, and our chatbot aims to simplify this process. The bot integrates with Telegram, providing users with tools to manage their finances efficiently. Whether you're tracking your portfolio or setting financial goals, our chatbot is designed to be your go-to resource.

### Key Features
- **Financial Goal Planning**: Upload your bank statement in CSV format, set a financial goal, and receive a tailored monthly budget to help you achieve your goal.
- **Portfolio Management**: Add or remove stocks from your portfolio and analyze your investments with ease.
- **Real-Time Market Information**: Get up-to-date market data, including portfolio valuation and gains, and visualize stock performance with interactive charts.
- **Bank Statement Analysis**: Upload your financial goals and monthly expenses to receive a custom budget and a timeline for reaching your savings target.

## Components of the Project

### Telegram Bot Creation
1. **API Key Setup**: Obtain an API Key using Telegram’s BotFather to interact with the bot via HTTP-based interfaces.
2. **Bot Development**: Developed using Python's Telebot library, this bot processes commands and handles user interactions.
3. **File Handling**: Users can upload CSV files containing bank statements, which are then processed and analyzed.

### Dummy Data Creation
Dummy bank statements were generated using Mockaroo to simulate real-world scenarios. The data includes transaction details such as date, description, debit/credit amounts, and more, categorized for analysis.

### Portfolio Management
Users can manage their portfolios by adding, removing, and viewing stocks. The bot fetches real-time stock prices and provides portfolio valuation and performance over time.

### Real-Time Market Information
The bot uses Yahoo Finance to fetch market data, enabling features like:
- Portfolio valuation
- Portfolio gains analysis over time
- Candlestick chart plotting for detailed stock performance analysis

### Bank Statement Analysis
The chatbot analyzes monthly expenses and helps users create a budget to meet their financial goals. It calculates savings and provides visual comparisons between current and expected expenditures.

### Database Management
MongoDB Atlas is used for managing user data, including transaction history and portfolio details, ensuring that all information is securely stored and easily retrievable.

## Libraries Used
- **NeuralIntents (modified)**: NLP model for intent recognition.
- **Matplotlib**: For plotting bar graphs of expected savings.
- **Plotly**: For interactive candlestick charts.
- **Yahoo Finance**: Real-time market data retrieval.
- **Telebot**: Telegram bot integration.
- **Pandas**: Data handling and analysis.
- **Numpy**: Mathematical computations.
- **PyMongo**: Integration with MongoDB Atlas for database management.

## Challenges Faced
- Integrating file upload functionality in Telegram.
- Transferring and displaying graphs in the Telegram chat.
- Updating deprecated functions in the NeuralIntents library.
- Linking the MongoDB backend with the Telegram bot.

## Future Enhancements
- Incorporating AI to categorize expenses in bank statements.
- Deploying the bot on Azure for broader accessibility.
- Enhancing NLP capabilities for better user input interpretation.

## Acknowledgements
We express our gratitude to **DESIS Ascend Educare 2022** for the opportunity to work on this project and to our mentor, **Mr. Sandeep Manthi**, for his guidance.
