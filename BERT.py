import pandas as pd
import pickle

# Constants
METADATA_FILE =  "./movie_lens_dataset/movies_metadata_processed.csv"
BERT_COSINE_SIM_FILE = "./pickle/bert_cosine_similarity.pickle"
MOVIE_INDICES_FILE = "./pickle/movie_indices.pickle"

# Initialising objects
data = pd.read_csv(METADATA_FILE, low_memory=False)
bert_cosine_sim = pickle.load(open(BERT_COSINE_SIM_FILE, 'rb'))
movie_indices = pickle.load(open(MOVIE_INDICES_FILE, 'rb'))

def getBertRecommendations(name: str):
    print("Getting recommendations for:", name)

    # Get index of query movie
    movie_index = movie_indices[name]
    
    # Get pairwsie similarity scores of all movies with that movie
    similarity_scores = pd.DataFrame(bert_cosine_sim[movie_index], columns=['score'])
    
    # Top 10
    top_indices = similarity_scores.sort_values(by="score", ascending=False)[1:11].index
    
    # Get movie title, release date and poster path
    output = data[['title', 'release_date', 'poster_path']].iloc[top_indices]

    output['score'] = similarity_scores.sort_values(by="score", ascending=False)['score'][1:11]
    
    return output.to_json(orient="records")