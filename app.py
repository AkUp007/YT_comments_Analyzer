from flask import Flask, render_template, request
from comments import returnytcomments, clean, create_wordcloud, returnsentiment
from summarizer import summarize_transcript
import os

# Initialize Flask App
app = Flask(__name__, template_folder="composites")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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

    np, nn, nne = 0, 0, 0 #  Counters for sentiment categories
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

@app.route('/summarize', methods=['GET'])
def summarize():
    url = request.args.get('url')
    if not url:
        return render_template('home_page.html', error="Invalid URL")
    summary = summarize_transcript(url)
    return render_template('summary.html', summary=summary, video_url=url)

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
