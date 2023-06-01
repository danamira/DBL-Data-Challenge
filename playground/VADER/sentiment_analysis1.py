from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

my_dict = {'tweet_text': ["I like cats more than I hate them!", "I hate cats more than I love them", "Cats drink milk"]}
df_data = pd.DataFrame.from_dict(data=my_dict, orient='columns')

sid_obj = SentimentIntensityAnalyzer()

for i in range(0, len(df_data.index)):
    sentiment_dict = sid_obj.polarity_scores(df_data['tweet_text'][i])
    print("Overall sentiment dictionary is : ", sentiment_dict)
