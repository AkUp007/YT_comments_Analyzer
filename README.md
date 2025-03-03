# **YouTube Video Comments Sentiment Analyzer**  

## **📌 Overview**  
The **YouTube Video Comments Sentiment Analyzer** is a Flask-based web application that extracts comments from a given YouTube video and performs sentiment analysis on them. The application utilizes **Selenium** for web scraping, **Natural Language Toolkit (NLTK)** for sentiment analysis, and **Matplotlib** for data visualization.  

---

## **✨ Features**  
✔ **Extracts comments** from any YouTube video using **Selenium**.  
✔ **Cleans and processes** the extracted text data.  
✔ **Performs sentiment analysis** (_Positive, Neutral, Negative_) using **VADER**.  
✔ **Generates a word cloud** to visualize commonly used words in the comments.  
✔ **Provides a simple web interface** to input the YouTube video URL and view results.  

---

## **🛠 Tech Stack**  
| **Component** | **Technology** |  
|--------------|--------------|  
| **Backend** | Flask (Python) |  
| **Web Scraping** | Selenium with Chrome WebDriver |  
| **Natural Language Processing** | NLTK (VADER Sentiment Analysis) |  
| **Visualization** | Matplotlib, WordCloud |  

---

## **⚙ Installation & Setup**  

### **🔹 Prerequisites**  
Ensure you have the following installed:  
- **Python 3.7+**  
- **Google Chrome**  
- **ChromeDriver** (_or use webdriver-manager for automatic installation_)  

### **📥 Steps to Install**  

#### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yourusername/youtube-comments-sentiment-analyzer.git
cd youtube-comments-sentiment-analyzer
```

#### **2️⃣ Create a Virtual Environment (Optional but Recommended)**  
```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate  
# On Windows:
venv\Scripts\activate  
```

#### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

#### **4️⃣ Download Required NLTK Data**  
```python
import nltk
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('wordnet')
```

#### **5️⃣ Run the Flask Application**  
```bash
python app.py
```

#### **6️⃣ Access the Web Interface**  
Open your browser and go to:  
👉 **http://127.0.0.1:5000**  

---

## **🚀 Usage**  
1️⃣ **Enter the YouTube video URL** in the provided input field.  
2️⃣ **Click the "Analyze" button.**  
3️⃣ **Wait** for the application to fetch and analyze comments.  
4️⃣ **View the sentiment analysis results** and word cloud visualization.  

---

## **🛠 Troubleshooting**  
⚠ **Chromedriver Issues**: Ensure ChromeDriver is updated to match your Chrome browser version.  
⚠ **Permission Errors**: Run with administrator privileges if encountering issues.  
⚠ **YouTube Changes**: If comments are not fetching, YouTube may have updated its structure. Update Selenium selectors accordingly.  

---

## **🚀 Future Enhancements**  
✅ Support for multiple sentiment analysis models.  
✅ Additional data visualizations (bar charts, pie charts).  
✅ Downloadable reports in **CSV or PDF format**.  

---

## **📜 License**  
This project is licensed under the **MIT License**.  

---

## **👨‍💻 Author**  
📌 **Your Name**  
🔗 **GitHub**: [AkUp007](https://github.com/AkUp007/)  
🔗 **LinkedIn**: [AkashUpadhyay](https://www.linkedin.com/in/akashupadhyay007/)
