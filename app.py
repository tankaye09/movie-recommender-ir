from flask import Flask,request,render_template
from flask_cors import CORS
import BERT
import collaborative

# Initialize Flask app
app = Flask(__name__, static_folder='./client/build', static_url_path='/')
CORS(app) 

# BERT Cosine Similarity
@app.route("/search", methods=['GET'])
def search():
    print("Searching for movie...")
    args = request.args
    query = args.get("query")
    try: 
        res = BERT.getBertRecommendations(query)
    except:
        return "Movie not found", 400
    return res

# Collaborative Filtering KNN
@app.route("/collab", methods=['GET'])
def collab():
    args = request.args
    query = args.get("query")
    query = query.split(",")
    try:
        res = collaborative.collaborative_recommender(query)
    except:
        return "An error occured", 400
    return res

# Serving React app
@app.route("/")
def home():
    return app.send_static_file('index.html')

if __name__=='__main__':
    app.run(port = 5000, debug = True)