import math
import pandas as pd

class CosineSimilarity:
    def __init__(self, data: pd.DataFrame) -> None:
        # Assume data will have id, title and plot
        self.data = data
    
    def term_frequency(self, term: str, document: str) -> float:
        return document.count(term) / len(document)
    
    def document_frequency(self, term: str, documents: list) -> int:
        '''
        Get document frequency of a term in a list of documents
        '''
        return len([doc for doc in documents if term in doc])

    def inverse_document_frequency(self, term: str, documents: list) -> float:
        '''
        Get inverse document frequency of a term in a list of documents
        '''
        return 1.0 + math.log(len(documents) / self.document_frequency(term, documents))

    def tf_idf(self, term: str, document: str, documents: list) -> float:
        return self.term_frequency(term, document) * self.inverse_document_frequency(term, documents)

    def tf_idf_matrix(self) -> pd.DataFrame:
        tf_idf_matrix = {}
        for _, document in self.data.iterrows():
            docId = document["docid"]
            plot = document["plot"]
            for token in plot.split(" "):
                if token in tf_idf_matrix:
                    tf_idf_matrix[token][docId] = self.tf_idf(token, plot, self.data["plot"].tolist())
                else:
                    tf_idf_matrix[token] = {docId: self.tf_idf(token, plot, self.data["plot"].tolist())}
        return pd.DataFrame(tf_idf_matrix).fillna(0)

    def cosine_similarity(self, vector1: list, vector2: list) -> float:
        '''
        Calculate cosine similarity between two vectors
        '''
        dot_product = sum([vector1[x] * vector2[x] for x in range(len(vector1))])
        magnitude1 = math.sqrt(sum([value**2 for value in vector1]))
        magnitude2 = math.sqrt(sum([value**2 for value in vector2]))
        return dot_product / (magnitude1 * magnitude2)
    
    def get_movie_recommendations(self, title: str) -> list:
        '''
        Get movie recommendations for a movie
        '''
        tf_idf_matrix = self.tf_idf_matrix()
        # print(tf_idf_matrix)
        indices = pd.Series(self.data.index, index=self.data["title"])
        # print(indices)
        try:
            idx = indices[title]
            # print("idx",idx)
        except:
            return "Movie not found"


        movie_vector = tf_idf_matrix.loc[idx]
        similarities = []
        for _, row in tf_idf_matrix.iterrows():
            if row.name != idx:
                similarities.append((row.name, self.cosine_similarity(movie_vector, row)))
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True);
        similarities = similarities[:10]
        movie_indices = [i[0] for i in similarities]
        print("indices", movie_indices)
        return self.data["title"].loc[movie_indices]


fake_data = {
    "id": [3, 22, 35,  45, 100],
    "title": ["The Shawshank Redemption", "The Godfather", "The Godfather: Part II", "The Dark Knight", "12 Angry"],
    "plot": ["Two imprisoned mothers", "Two imprisoned fathers", "Two imprisoned fathers part two", "Batman strikes fathers again", "angry fathers"],
}

# fake_data_df = pd.DataFrame(fake_data, index=fake_data["id"])

# cosine_similarity = CosineSimilarity(fake_data_df)

# print(cosine_similarity.tf_idf_matrix())
# print(cosine_similarity.get_movie_recommendations("The Godfather"))

# data = pd.read_csv("processed_data_partial.csv")
# data.index=data.docid
# print(data)
# cosine_similarity = CosineSimilarity(data)
# print(cosine_similarity.get_movie_recommendations("1, 2, 3 whiteout"))