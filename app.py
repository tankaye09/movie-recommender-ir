from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
from cosine_similarity import CosineSimilarity
from okapiBM25 import OkapiBM25
import pandas as pd

datafile =  "processed_data.csv"
data = pd.read_csv("processed_data.csv")

# Cosine Similarity
data.index=data.docid
cosine_similarity = CosineSimilarity(data)

# OkapiBM25



def get_suggestions():
    data = pd.read_csv('processed_data_partial.csv')
    return list(data['title'].str.capitalize())

app = Flask(__name__)
CORS(app) 


@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return render_template('home.html',suggestions=suggestions)

if __name__=='__main__':
    app.run(port = 5000, debug = True)