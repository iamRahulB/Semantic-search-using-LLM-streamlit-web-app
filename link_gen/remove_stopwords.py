import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download("stopwords")
nltk.download('punkt')

class StopWordsRemoval:
    def __init__(self) -> None:
        pass

    def stopwords_removal(self,response):
       

        words=word_tokenize(response)
        stop_words=set(stopwords.words('english'))

        filtered_words=[re.sub(r'[^a-zA-Z0-9\s]','',word) for word in words if word.lower() not in stop_words]


        filtered_text=' '.join(filtered_words)

        

        return filtered_text
