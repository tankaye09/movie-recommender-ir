import math
import pandas as pd

class OkapiBM25:
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

    def ld(self, document: str):
        ld = len(document.split(" "))
        return ld
    
    def la(self, documents: list):
        totalLength = 0
        for i in documents:
            docLength = len(i.split(" "))
            totalLength += docLength
        la = totalLength / len(documents)
        return la

    def okapiBM25(self, term: str, document: str, documents: list, k1 = 1.5, b = 0.75) -> float:
        ld = self.ld(document)
        la = self.la(documents)
        tf = self.term_frequency(term, documents)
        idf = self.inverse_document_frequency(term, documents)
        rsv = idf * (k1 + 1) * tf / (k1 * (((1 - b) + b) * ld / la) + tf)
        return rsv

    def okapiBM25_matrix(self) -> pd.DataFrame:
        okapiBM25_matrix = {}
        for _, document in self.data.iterrows():
            docId = document["docid"]
            plot = document["plot"]
            for token in plot.split(" "):
                if token in okapiBM25_matrix:
                    okapiBM25_matrix[token][docId] = self.okapiBM25(token, plot, self.data["plot"].tolist())
                else:
                    okapiBM25_matrix[token] = {docId: self.okapiBM25(token, plot, self.data["plot"].tolist())}
        return pd.DataFrame(okapiBM25_matrix).fillna(0)

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
        okapiBM25_matrix = self.okapiBM25_matrix()
        indices = pd.Series(self.data.index, index=self.data["title"])
        try:
            idx = indices[title]
            # print("idx",idx)
        except:
            return "Movie not found"


        movie_vector = okapiBM25_matrix.loc[idx]
        similarities = []
        for _, row in okapiBM25_matrix.iterrows():
            if row.name != idx:
                similarities.append((row.name, self.cosine_similarity(movie_vector, row)))
        similarities = sorted(similarities, key=lambda x: x[1], reverse=True);
        similarities = similarities[:10]
        movie_indices = [i[0] for i in similarities]
        print("indices", movie_indices)
        return self.data["title"].loc[movie_indices]

# data = pd.read_csv("processed_data.csv")
# data.index=data.docid
# print(data)
# okapiBM25 = OkapiBM25(data)
# print(okapiBM25.get_movie_recommendations("$"))