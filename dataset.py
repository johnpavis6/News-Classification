import json
import sys
from os import listdir
from termcolor import colored

from textblob import Word

from preprocess import clean_text

with open('./categories.json') as fp:
    categories = json.loads(fp.read())

if len(sys.argv) == 1:
    print colored('Please give the limit for each category.','red')
    exit()

x, y = [], []
limit = int(sys.argv[1])
index = 1
for category in categories:
    path = './dataset/%s' % (category,)
    files = listdir(path)
    if(len(files) < 81):
        continue
    count = 0
    for file in files:
        with open(path+'/'+file, 'r') as fp:
            data = json.loads(fp.read())
        for article in data['posts']:
            if(count >= limit):
                break
            text = ' '.join([Word(word).lemmatize()
                             for word in clean_text(article['text']).split()])
            if(not len(text)):
                continue
            x.append(text)
            y.append(category)
            count += 1
        else:
            continue
        break
    print colored([index, category, count],'green')
    index += 1

dataset = [x, y]

with open('dataset.json', 'w') as fp:
    fp.write(json.dumps(dataset))
