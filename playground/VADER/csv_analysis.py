import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt

df_data = pd.read_csv('data_short2.csv', encoding='latin-1', header=None)

sid_obj = SentimentIntensityAnalyzer()
df_sentiment = pd.DataFrame(columns=['neg', 'neu', 'pos', 'compound'])

for i in range(0, len(df_data.index)):
    sentiment_dict = sid_obj.polarity_scores(df_data[5][i])
    df_dictionary = pd.DataFrame(sentiment_dict, index=[0])
    df_sentiment = pd.concat([df_sentiment, df_dictionary], ignore_index=True)

# Show neg and pos, scatter plot
sns.scatterplot(data=df_sentiment, x="neg", y="pos")
plt.show()

# Show boxplot over compound
sns.boxplot(x=df_sentiment["compound"])
plt.show()
