import os
import time
import re
import nltk
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
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

# ✅ Fix 1: Set Matplotlib cache directory to a writable location
os.environ['MPLCONFIGDIR'] = "/tmp/matplotlib_cache"

# ✅ Fix 2: Set NLTK Data Directory to a Writable Location
NLTK_DATA_DIR = "/tmp/nltk_data"
os.makedirs(NLTK_DATA_DIR, exist_ok=True)
nltk.data.path.append(NLTK_DATA_DIR)

# ✅ Fix 3: Download NLTK Data to the new writable location
nltk.download('vader_lexicon', download_dir=NLTK_DATA_DIR)
nltk.download('stopwords', download_dir=NLTK_DATA_DIR)
nltk.download('wordnet', download_dir=NLTK_DATA_DIR)

# Download NLTK Resources
nltk.download('vader_lexicon')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Flask App
app = Flask(__name__, template_folder="composites")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize NLP Tools
wnl = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# WebDriver Configuration (Update the path accordingly)
CHROMEDRIVER_PATH = r"C:\Users\ASUS\.wdm\chromedriver-win64\chromedriver.exe"

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
        for _ in range(5):
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(3)

        # Extract comments
        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
            data.append(comment.text.strip())
            

    return data

# Function to Clean Comments
def clean(org_comments):
    cleaned = []
    for x in org_comments:
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
    
    CleanCache(directory="static/img")
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

# Flask Routes
@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/results', methods=['GET'])
def inference():
    url = request.args.get('url')
    
    if not url:
        return render_template('home_page.html', error="Invalid URL")

    org_comments = returnytcomments(url)
        # Handle case where no comments are found
    if not org_comments:
        return render_template('home_page.html', error="No comments found or comments are disabled on this video.")

    # Filter very short or long comments
    org_comments = [c for c in org_comments if 5 < len(c) <= 500]

    # If all comments were filtered out, handle it
    if not org_comments:
        return render_template('home_page.html', error="All comments were too short or too long to analyze.")


    clean_comments = clean(org_comments)
    create_wordcloud(clean_comments)

    np, nn, nne = 0, 0, 0
    predictions, scores = [], []

    for comment in clean_comments:
        score, sentiment = returnsentiment(comment)
        scores.append(score)

        if sentiment == "Positive":
            predictions.append("POSITIVE")
            np += 1
        elif sentiment == "Negative":
            predictions.append("NEGATIVE")
            nn += 1
        else:
            predictions.append("NEUTRAL")
            nne += 1

    results = [
        {
            "sent": predictions[i],
            "clean_comment": clean_comments[i],
            "org_comment": org_comments[i],
            "score": scores[i]
        }
        for i in range(len(clean_comments))
    ]
    return render_template('inference.html', n=len(clean_comments), nn=nn, np=np, nne=nne, dic=results)

@app.route('/word_cloud')
def word_cloud():
    return render_template('word_cloud.html')

class CleanCache:
	'''
	this class is responsible to clear any residual csv and image files
	present due to the past searches made.
	'''
	def __init__(self, directory=None):
		self.clean_path = directory
		# only proceed if directory is not empty
		if os.listdir(self.clean_path) != list():
			# iterate over the files and remove each file
			files = os.listdir(self.clean_path)
			for fileName in files:
				print(fileName)
				os.remove(os.path.join(self.clean_path,fileName))
		print("cleaned!")

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True,  use_reloader=False)
