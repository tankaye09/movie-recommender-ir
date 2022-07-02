import os
import json
import string
import pandas as pd
import xmltodict
import nltk
from nltk.corpus import stopwords, wordnet2021
from nltk.stem import WordNetLemmatizer

nltk.download("stopwords")
nltk.download("omw-1.4")

# directory = r"complete_dataset\xml-utf8_with_plots_with_url"

# Using for testing
directory = r"partial_dataset\xml-utf8_with_plots_with_url"

cachedStopWords = stopwords.words("english")
lemm = WordNetLemmatizer()
data_list = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file_path = directory + "\\" + filename
        with open(file_path) as xml_file:
            data_dict = xmltodict.parse(xml_file.read(), encoding="utf-8")
            xml_file.close()

        # generate the object using json.dumps()
        # corresponding to json data, but as a string, to be stored in a file

        json_str = json.dumps(data_dict)
        json_data = json.loads(json_str)

        # preprocess plot text
        json_plot = json_data["doc"]["plot"]

        # text lowercase
        json_plot = str(json_plot).lower()

        # remove punctuation
        json_plot = json_plot.translate(str.maketrans("", "", string.punctuation))

        # tokenize, lemmatize and remove stopwords
        json_plot = " ".join(
            [
                lemm.lemmatize(word)
                for word in json_plot.split()
                if word not in cachedStopWords
            ]
        )

        # remove numbers
        # KIV

        # update json data
        json_data["doc"]["plot"] = json_plot

        data_list.append(json_data["doc"])

        # Write the json data to output
        # json file
        # with open("sample.json", "w", encoding="utf8") as json_file:
        #     json.dump(json_data, json_file, ensure_ascii=False)
        #     json_file.close()

df = pd.DataFrame(data_list)
df.to_csv("processed_data.csv", encoding="utf-8")
