# -*- coding: utf-8 -*-
"""Best States By Rating.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NHQ3YUYPb5Wetsg6JX-QODsJdRFfc7VM
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('provider.csv', encoding='iso-8859-1')

zip_code_counts = df['Provider Zip Code'].value_counts()

print(zip_code_counts)

filtered_df = df[df['Overall Rating'] > 3]

counts = filtered_df.groupby('Provider Zip Code').size()

sorted_counts = counts.sort_values(ascending=False).head(25)

print(sorted_counts)

import seaborn as sns

top150 = sorted_counts.head(150).index.tolist()
df150 = df[df['Provider Zip Code'].isin(top150)]

rate150 = df150[df150['Overall Rating'] >= 3].groupby('Provider State').size().sort_values(ascending=False).head(10)

rate150_df = rate150.reset_index()
rate150_df.columns = ['State', 'Total Ratings']

plt.figure(figsize=(10, 6))
sns.barplot(x='State', y='Total Ratings', data=rate150_df, color='green')
plt.title('Top 150 Above Average ZIP Code Ratings Per State')
plt.xlabel('State')
plt.ylabel('Total Ratings')
plt.xticks(rotation=0)
plt.show()

top25 = sorted_counts.head(25).index.tolist()
df25 = df[df['Provider Zip Code'].isin(top25)]

rate25 = df25[df25['Overall Rating'] >= 3].groupby('Provider State').size().sort_values(ascending=False).head(10)

rate25_df = rate25.reset_index()
rate25_df.columns = ['State', 'Total Ratings']

plt.figure(figsize=(10, 6))
sns.barplot(x='State', y='Total Ratings', data=rate25_df, color='green')
plt.title('Top 25 Above Average ZIP Code Ratings Per State')
plt.xlabel('State')
plt.ylabel('Total Ratings')
plt.xticks(rotation=0)
plt.show()

fdf = df[df['Overall Rating'] > 3]
fd = fdf[['Provider Zip Code', 'Provider State']]
fd_filtered = fd[fd['Provider State'].isin(['OH', 'CA', 'NY', 'CO'])]

filtered_sorted_counts = sorted_counts.loc[sorted_counts.index.intersection(fd_filtered['Provider Zip Code'].astype(sorted_counts.index.dtype))]
zip_code_list = filtered_sorted_counts.index.tolist()

print(zip_code_list)