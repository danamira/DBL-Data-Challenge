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
# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
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
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        score_sum = (scores[ranking[0]] - scores[ranking[2]]) # score = positive - negative
    except Exception:
        pass

    return score_sum


# Test
my_text = "Hello, I am happy and very sad"
score = sentiment_score(my_text)
print(score)