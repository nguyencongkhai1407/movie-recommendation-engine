import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("data/movie_dataset.csv")
# print(df.info())
# print(df.columns)
# Helper functions
# Get the title of the movie from its index in dataframe
def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]
# Get the index of the matched movie title
def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

# Content-based features
features = ['keywords','cast','genres','director']

# Fill all the nan values in each feature with empty string to apply combine_features later
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
	return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]


df["combined_features"] = df.apply(combine_features,axis=1)
# print(df["combined_features"].head())

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

cosine_sim = cosine_similarity(count_matrix)
# print(cosine_sim)
movie_user_likes = "Avatar"

movie_index = get_index_from_title(movie_user_likes)

similar_movies = list(enumerate(cosine_sim[movie_index]))
# print(similar_movies)
sorted_similar_movies = sorted(similar_movies, key = lambda x:x[1], reverse = True)

print("Movies similar to", movie_user_likes, ":\n")
for x, movie in enumerate(sorted_similar_movies):
	if x != 0:
		print(get_title_from_index(movie[0]))
	if x == 50:
		break