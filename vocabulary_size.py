words = []
with open("tweets.txt", "r") as filestream:
  for line in filestream:
    currentline = line.split(",")
    currentline.pop(0)
    for i in currentline:
      j = i.replace("\n", '')
      words.append(j)

#print(words)
uniq_words = set(words)
uniq_count = len(uniq_words)
#print(uniq_words)
print("count of unique words = ", uniq_count)

