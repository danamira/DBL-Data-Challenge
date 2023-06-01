import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt

my_dict = {'neg': [0, 0.3, 0.5, 0.7, 1], "pos": [0, 0.3, 0.5, 0.7, 1]}
df_data = pd.DataFrame.from_dict(data=my_dict, orient='columns')

print(df_data)

#sns.scatterplot(data=df_data, x="neg", y="pos")
#plt.show()