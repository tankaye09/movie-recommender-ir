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
        json_data = json.loads(json_str)["doc"]
        new_json_data = {}

        # remove nested keys
        # colorinfo: {genre: {genre: [Music, Horror, Thriller]}} -> {genre: [Music, Horror, Thriller]}
        new_json_data["docid"] = json_data["docid"]
        new_json_data["title"] = json_data["title"]
        new_json_data["year"] = json_data["year"]
        new_json_data["genres"] = json_data.get("genres", {}).get("genre")
        new_json_data["languages"] = json_data.get("languages", {}).get("language")
        new_json_data["countries"] = json_data.get("countries", {}).get("country")
        new_json_data["directors"] = json_data.get("directors", {}).get("director")
        new_json_data["composers"] = json_data.get("composers", {}).get("composer")
        new_json_data["cast"] = json_data.get("cast", {}).get("credit")
        new_json_data["editors"] = json_data.get("editors", {}).get("editor")
        new_json_data["keywords"] = json_data.get("keywords", {}).get("keyword")
        new_json_data["writers"] = json_data.get("writers", {}).get("writer")

        # preprocess plot text
        json_plot = json_data["plot"]

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
        new_json_data["plot"] = json_plot

        data_list.append(new_json_data)

df = pd.DataFrame(data_list)
df.to_csv("processed_data.csv", encoding="utf-8")
