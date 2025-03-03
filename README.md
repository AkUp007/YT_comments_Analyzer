YouTube Video Comments Sentiment Analyzer

Overview

The YouTube Video Comments Sentiment Analyzer is a Flask-based web application that extracts comments from a given YouTube video and performs sentiment analysis on them. The application utilizes Selenium for web scraping, Natural Language Toolkit (NLTK) for sentiment analysis, and Matplotlib for data visualization.

Features

Extracts comments from any YouTube video using Selenium.

Cleans and processes the extracted text data.

Performs sentiment analysis (Positive, Neutral, Negative) using VADER.

Generates a word cloud to visualize commonly used words in the comments.

Provides a simple web interface to input the YouTube video URL and view results.

Tech Stack

Backend: Flask (Python)

Web Scraping: Selenium with Chrome WebDriver

Natural Language Processing (NLP): NLTK (VADER Sentiment Analysis)

Visualization: Matplotlib, WordCloud

Installation & Setup

Prerequisites

Ensure you have the following installed:

Python 3.7+

Google Chrome

ChromeDriver (or use webdriver-manager for automatic installation)

Steps to Install

Clone the Repository

git clone https://github.com/yourusername/youtube-comments-sentiment-analyzer.git
cd youtube-comments-sentiment-analyzer

Create a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Download Required NLTK Data

import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('wordnet')

Run the Flask Application

python app.py

Access the Web Interface
Open your browser and go to:

http://127.0.0.1:5000

Usage

Enter the YouTube video URL in the provided input field.

Click the Analyze button.

Wait for the application to fetch and analyze comments.

View sentiment analysis results and word cloud visualization.

Troubleshooting

Chromedriver Issues: Ensure ChromeDriver is updated to match your Chrome browser version.

Permission Errors: Run with administrator privileges if encountering issues.

YouTube Changes: If comments are not fetching, YouTube may have updated its structure. Update Selenium selectors accordingly.

Future Enhancements

Support for multiple sentiment analysis models.

Additional data visualizations (bar charts, pie charts).

Downloadable reports in CSV or PDF format.

License

This project is licensed under the MIT License.

Author

Your NameGitHub: yourusernameLinkedIn: yourlinkedin

