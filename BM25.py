import math
import numpy as np
import pandas as pd

class BM25:
    def __init__(self, data):
        self.data_size = 0
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []

        tf = self.cal_tf(data)
        self._calc_idf(tf)

    def cal_tf(self, data):
        tf = {}  # term -> number of documents with term
        num_doc = 0
        for document in data:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for term in document:
                if term not in frequencies:
                    frequencies[term] = 0
                frequencies[term] += 1
            self.doc_freqs.append(frequencies)

            for term, freq in frequencies.items():
                try:
                    tf[term]+=1
                except KeyError:
                    tf[term] = 1

            self.data_size += 1

        self.avgdl = num_doc / self.data_size
        return tf

    def _calc_idf(self, tf):
        raise NotImplementedError()

    def get_scores(self, query):
        raise NotImplementedError()

    def get_batch_scores(self, query, doc_ids):
        raise NotImplementedError()

    def get_top_n(self, query, documents, n=5):

        assert self.data_size == len(documents), "The documents given don't match the index data!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return [documents[i] for i in top_n]


class BM25Okapi(BM25):
    def __init__(self, data, k1 = 1.5, b = 0.75, epsilon=0):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__(data)

    def _calc_idf(self, tf):
        # collect idf sum to calculate an average idf for epsilon value, default floor of idf is set to 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if term is contained in more than half of documents
        idf_sum = 0
        negative_idfs = []
        for term, freq in tf.items():
            # freq is document frequency
            idf = math.log(self.data_size) - math.log(freq)
            self.idf[term] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(term)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for term in negative_idfs:
            self.idf[term] = eps

    def get_scores(self, query):
        score = np.zeros(self.data_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score

    def get_batch_scores(self, query, doc_ids):
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score.tolist()


corpus = pd.read_csv("movie_lens_dataset\movies_metadata_processed_no_stopwords.csv")

def top_related_movies(query_title, corpus, n=10):
    overview = corpus['overview']
    tokenized_corpus = [doc.split(" ") for doc in overview]
    bm25 = BM25Okapi(tokenized_corpus)
    
    query = corpus.loc[corpus['original_title'] == query_title, 'overview'].item()
    tokenized_query = query.split(" ")

    doc_scores = bm25.get_top_n(tokenized_query, overview, n)
    scores = bm25.get_scores(tokenized_query)
    df = pd.DataFrame({"original_title": corpus['original_title'], "release_date": corpus['release_date'], "poster_path": corpus['poster_path'], "rsv_score": scores})
    top_indices = df.sort_values(by="rsv_score", ascending=False)[1:11].index
    output = df[['original_title', 'release_date', 'poster_path', 'rsv_score']].iloc[top_indices]
       
    return output

print(top_related_movies("Toy Story", corpus))