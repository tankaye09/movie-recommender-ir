import pickle
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# load pickle file

user_to_movie_df = pd.read_pickle('pickle/user_to_movie.pickle')
refined_dataset = pd.read_pickle('pickle/refined_dataset.pickle')
knn_model = pickle.load(open("pickle/knn_model.pickle", "rb"))
dataset = pd.read_csv('movie_lens_dataset/movies_metadata_processed.csv', encoding='latin-1')

## create a new user row from movies they like

def new_user_from_movies(movies):
    user_id_list = [-1] * len(movies)
    rating_list = [4.5] * len(movies)
    keys = refined_dataset.columns
    values = [user_id_list, movies, rating_list]
    dic = {}
    for col_index in range(len(keys)):
        dic[keys[col_index]] = values[col_index]
    return pd.DataFrame(dic)

#  Giving Input as User id, Number of similar Users to be considered, Number of top movie we want to recommend

def new_recommender_system(user_df, n_similar_users, n_movies): #, user_to_movie_df, knn_model):
  
  print("Movie seen by the User:")
  print(list(user_df["movie title"]))
  print("")
  user_id = -1

  # def get_similar_users(user, user_to_movie_df, knn_model, n = 5):
  def get_similar_users(n = 5):
    movies = list(user_df["movie title"])
    knn_input_array = np.array([4.5 if col in movies else 0 for col in user_to_movie_df.columns])
    
    knn_input = np.asarray([knn_input_array])
    
    distances, indices = knn_model.kneighbors(knn_input, n_neighbors=n+1)
    
    print("Top",n,"users who are very much similar to the User-",user_id, "are: ")
    print(" ")

    for i in range(1,len(distances[0])):
      print(i,". User:", indices[0][i]+1, "separated by distance of",distances[0][i])
    print("")
    return indices.flatten()[1:] + 1, distances.flatten()[1:]


  def filtered_movie_recommendations(n = 10):
  
    first_zero_index = np.where(mean_rating_list == 0)[0][-1]
    sortd_index = np.argsort(mean_rating_list)[::-1]
    sortd_index = sortd_index[:list(sortd_index).index(first_zero_index)]
    n = min(len(sortd_index),n)
    # movies_watched = list(refined_dataset[refined_dataset['user id'] == user_id]['movie title'])
    movies_watched = list(user_df["movie title"])
    filtered_movie_list = list(movies_list[sortd_index])
    count = 0
    final_movie_list = []
    for i in filtered_movie_list:
      if i not in movies_watched:
        count+=1
        final_movie_list.append(i)
      if count == n:
        break
    if count == 0:
      print("There are no movies left which are not seen by the input users and seen by similar users. May be increasing the number of similar users who are to be considered may give a chance of suggesting an unseen good movie.")
    else:
      return final_movie_list

  similar_user_list, distance_list = get_similar_users(n_similar_users)
  weightage_list = distance_list/np.sum(distance_list)
  mov_rtngs_sim_users = user_to_movie_df.values[similar_user_list]
  movies_list = user_to_movie_df.columns
  weightage_list = weightage_list[:,np.newaxis] + np.zeros(len(movies_list))
  new_rating_matrix = weightage_list*mov_rtngs_sim_users
  mean_rating_list = new_rating_matrix.sum(axis =0)
  print("")
  print("Movies recommended based on similar users are: ")
  print("")
  return filtered_movie_recommendations(n_movies)    
  
def collaborative_recommender(movies):
    new_user_dataset = new_user_from_movies(movies)
    titles = new_recommender_system(new_user_dataset, 5,10)
    return dataset[dataset["title"].isin(titles)][["title", "poster_path", "release_date"]].to_json(orient='records')

test_movies_guy = ["The Matrix",
"The Dark Knight",
"Toy Story",
"The Avengers"]

test_movies_girl = ["The Devil Wears Prada",
"Mean Girls",
"Sex and the City",
"Frozen"]

print("Recommended movies: ", collaborative_recommender(test_movies_guy))