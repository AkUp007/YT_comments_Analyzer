import os
import time
import re
import nltk
import numpy as np
import matplotlib
matplotlib.use('Agg')# Use 'Agg' backend for Matplotlib to avoid GUI dependency
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS

#  Set Matplotlib cache directory to a writable location
os.environ['MPLCONFIGDIR'] = "/tmp/matplotlib_cache"

#  Set NLTK Data Directory to a Writable Location
NLTK_DATA_DIR = "/tmp/nltk_data"
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DATA_DIR)

#  Download required NLTK resources only if they are missing
for package in ['vader_lexicon', 'stopwords', 'wordnet']:
    try:
        nltk.data.find(f'corpora/{package}')
    except LookupError:
        nltk.download(package, download_dir=NLTK_DATA_DIR)

# Download NLTK Resources
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP Tools
wnl = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# WebDriver Configuration (Update the path accordingly)
CHROMEDRIVER_PATH = r"C:\Windows\chromedriver.exe"
if not os.path.exists(CHROMEDRIVER_PATH):
    raise FileNotFoundError("Chromedriver not found at the specified path. Please update CHROMEDRIVER_PATH.")

# Function to Fetch YouTube Comments
def returnytcomments(url):
    data = []
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    
    with webdriver.Chrome(service=service, options=options) as driver:
        wait = WebDriverWait(driver, 15)
        driver.get(url)
        driver.maximize_window()

        # Scroll down multiple times to load comments
        for _ in range(10):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        # Extract comments
        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            data.append(comment.text.strip())
            

    return data

# Function to Clean Comments (Removing stopwords, lemmatizing, and filtering)
def clean(org_comments):
    cleaned = []
    for x in org_comments:
        x = re.sub(r'[\U0001F600-\U0001F64F]', '', x)  # Remove emojis
        x = re.sub(r'[^a-zA-Z\s]', '', x.lower().strip())  # irrelevant non_alphabet removal
        words = x.lower().strip().split()
        words = [w for w in words if w not in stop_words and len(w) > 2]
        words = [wnl.lemmatize(w) for w in words]
        cleaned.append(" ".join(words))
    return cleaned

# Function to Generate Word Cloud
def create_wordcloud(clean_reviews):
    text = " ".join(clean_reviews)
    wc = WordCloud(width=1400, height=800, stopwords=set(STOPWORDS), background_color="white").generate(text)
    
    plt.figure(figsize=(20, 10), facecolor="k", edgecolor="k")
    plt.imshow(wc, interpolation="bicubic")
    plt.axis("off")
    plt.tight_layout()
    
    CleanCache(directory="static/img")# Clean previous cache before saving
    plt.savefig("static/img/word_cl.jpeg")
    plt.close()

# Function to Get Sentiment Score
def returnsentiment(comment):
    score = sia.polarity_scores(comment)["compound"]
    if score > 0:
        return score, "Positive"
    elif score < 0:
        return score, "Negative"
    return score, "Neutral"

# Cache Cleaner Class
class CleanCache:
    def __init__(self, directory=None):
        self.clean_path = directory
        if directory and os.path.exists(directory):
            for fileName in os.listdir(directory):
                file_path = os.path.join(self.clean_path, fileName)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("Cache cleaned!")


