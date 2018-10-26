import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import Word


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = [word.strip() for word in word_tokenize(text)]
    words = [Word(word).lemmatize()
             for word in words if len(word) >= 3 and not word in stopwords.words('english')]
    return ' '.join(word for word in words)


def clean(text):
    text = re.sub(r"\'s", "", text)
    text = re.sub(r"\'ve", "", text)
    text = re.sub(r"n\'t", "", text)
    text = re.sub(r"\'re", "", text)
    text = re.sub(r"\'d", "", text)
    text = re.sub(r"\'ll", "", text)
    text = re.sub(r",", "", text)
    text = re.sub(r"!", "", text)
    text = re.sub(r"\(", "", text)
    text = re.sub(r"\)", "", text)
    text = re.sub(r"\?", "", text)
    text = re.sub(r"'", "", text)
    text = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", text)
    text = re.sub(r"[0-9]\w+|[0-9]", "", text)
    text = re.sub(r"\s{2,}", " ", text)
