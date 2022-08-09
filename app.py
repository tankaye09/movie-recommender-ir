from flask import Flask,request,render_template
from flask_cors import CORS
import BERT
import collaborative

# Initialize Flask app
app = Flask(__name__)
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

# Testing
@app.route("/", methods=['GET'])
def hello():
    return "Hello!"

# @app.route("/")
# @app.route("/home")
# def home():
#     suggestions = get_suggestions()
#     return render_template('home.html',suggestions=suggestions)



if __name__=='__main__':
    app.run(port = 5000, debug = True)