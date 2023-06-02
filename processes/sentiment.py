"""
FUNCTION FOR SENTIMENT ANALYSIS.
This script imports the relevant modules to perform the sentiment analysis, 
as well as contians a function that takes a string and returns a sentiment score 
on the form; score: int = positive - negative
"""

"""MODEL IMPORTS
"""
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import re

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = re.sub(r'@\S+', '@user', text)
    return new_text
MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)
#model.save_pretrained(MODEL)


def sentiment_score(text):
    """ 
    Detects the sentiment of a string of text, using the RoBERTa model.
    :param text: string containing tweet text 
    :returns: sentiment score: int = positive - negative
    """
    score_sum = 'NI'
    try:
        # Sentiment detection
        text_processed = preprocess(str(text))
        encoded_input = tokenizer(text_processed, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        score_sum = (scores[2] - scores[0]) # score = positive - negative
    except Exception as e:
        print(e)
        pass

    return score_sum
