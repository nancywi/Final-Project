#Importing libraries
import argparse
import re
import sys
import numpy as np

# Cleaning the tweets
# reference link: https://gist.github.com/aniruddha27/8d112b87ff4014b80f606dc68080066d#file-preprocess_tweets-py
def preprocess(tweet):
    # remove links
    tweet = re.sub(r'http\S+', '', tweet)
    # remove mentions
    tweet = re.sub("@\w+","",tweet)
    # alphanumeric and hashtags
    tweet = re.sub("[^a-zA-Z#]"," ",tweet)
    #tweet = re.sub("[#+a-zA-Z]"," ",tweet)
    # remove multiple spaces
    tweet = re.sub("\s+"," ",tweet)
    tweet = tweet.lower()
    return tweet

#Getting all text from tweets.txt and converting to a string called 'data'
text_file = open("tweets.txt", "r")
data = text_file.read()
text_file.close()
data = data.replace('\n','')

#splitting it on date comma and then space as this is how our tweets.txt was generated (using regular expression)
data = re.split('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9], ',data)
data = data[1::]

#adding in spaces before and after to avoid 'this is' vs 'is', tweets preprocessing
for i in range(len(data)):
    data[i] = ' '+data[i]+' '
    data[i] = preprocess(data[i])

#declaring empty array words
words = []

#segregating all the words and appending to array words
for i in range(len(data)):
  currentline = data[i].split()
  for j in range(len(currentline)):
    words.append(currentline[j])

#removing hashtags from the array
words = [item for item in words if item[0] != '#']
words

#getting the unique words in the array using set
uniq_words = set(words)
uniq_count = len(uniq_words)
print("count of unique words = ", uniq_count)
