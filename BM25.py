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
        tf = {}  # word -> number of documents with word
        num_doc = 0
        for document in data:
            self.doc_len.append(len(document))
            num_doc += len(document)

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word, freq in frequencies.items():
                try:
                    tf[word]+=1
                except KeyError:
                    tf[word] = 1

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

    def get_top_n_titles(self, query, documents, n=5):

        assert self.data_size == len(documents), "The documents given don't match the index data!"

        overview = documents[query]
        tokenized_overview = overview.split(" ")

        scores = self.get_scores(tokenized_overview)
        top_n = np.argsort(scores)[::-1][:n]
        return [documents[i] for i in top_n]


class BM25Okapi(BM25):
    def __init__(self, data, k1 = 1.5, b = 0.75, epsilon=0):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        super().__init__(data)

    def _calc_idf(self, tf):
        """
        Calculates frequencies of terms in documents and in data.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in tf.items():
            # freq is document frequency
            idf = math.log(self.data_size) - math.log(freq)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_scores(self, query):
        """
        The ATIRE BM25 variant uses an idf function which uses a log(idf) score. To prevent negative idf scores,
        this algorithm also adds a floor to the idf value of epsilon.
        See [Trotman, A., X. Jia, M. Crane, Towards an Efficient and Effective Search Engine] for more info
        :param query:
        :return:
        """
        score = np.zeros(self.data_size)
        doc_len = np.array(self.doc_len)
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.doc_freqs])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score

    def get_batch_scores(self, query, doc_ids):
        """
        Calculate bm25 scores between query and subset of all docs
        """
        assert all(di < len(self.doc_freqs) for di in doc_ids)
        score = np.zeros(len(doc_ids))
        doc_len = np.array(self.doc_len)[doc_ids]
        for q in query:
            q_freq = np.array([(self.doc_freqs[di].get(q) or 0) for di in doc_ids])
            score += (self.idf.get(q) or 0) * (q_freq * (self.k1 + 1) /
                                               (q_freq + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)))
        return score.tolist()


corpus = pd.read_csv("movie_lens_dataset\movies_metadata_processed_id_title_overview.csv")

overview = corpus['overview']
tokenized_corpus = [doc.split(" ") for doc in overview]
bm25 = BM25Okapi(tokenized_corpus)

title = "Toy Story"
query = corpus.loc[corpus['original_title'] == title, 'overview'].item()

tokenized_query = query.split(" ")

doc_scores = bm25.get_top_n(tokenized_query, overview, n=5)

top_titles = []
for i in doc_scores:
    top_titles.append(corpus.loc[corpus['overview'] == i, 'original_title'].item())
print(top_titles)