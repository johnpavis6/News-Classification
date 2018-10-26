import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier

with open('dataset.json', 'r') as fp:
    dataset = json.loads(fp.read())
x, y = dataset[0], dataset[1]

vect = TfidfVectorizer(stop_words='english', min_df=2)
X = vect.fit_transform(x)
Y = y

classifiers = [
    # LinearSVC(),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MultinomialNB(),
    GradientBoostingClassifier(),
    KNeighborsClassifier(),
    # SVC(probability=True),
    # NuSVC(probability=True),
    # AdaBoostClassifier(),
]

log_cols = ["Classifier", "Accuracy", "Log Loss"]
log = pd.DataFrame(columns=log_cols)

for clf in classifiers:
    try:
        clf.fit(X, Y)
    except:
        continue
    name = clf.__class__.__name__

    print("="*30)
    print(name)

    print('****Results****')
    train_predictions = clf.predict(vect.transform(x))
    acc = accuracy_score(Y, train_predictions)
    print("Accuracy: {:.4%}".format(acc))

    train_predictions = clf.predict_proba(vect.transform(x))
    ll = log_loss(Y, train_predictions)
    print("Log Loss: {}".format(ll))

    log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
    log = log.append(log_entry)
print("="*30)
# exit()
sns.set_color_codes("muted")
sns.barplot(x='Accuracy', y='Classifier', data=log, color="b")

plt.xlabel('Accuracy %')
plt.title('Classifier Accuracy')
plt.show()

sns.set_color_codes("muted")
sns.barplot(x='Log Loss', y='Classifier', data=log, color="g")

plt.xlabel('Log Loss')
plt.title('Classifier Log Loss')
plt.show()
