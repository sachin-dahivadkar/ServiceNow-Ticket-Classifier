from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import joblib

df = pd.read_csv("F:\Chatbot topics\incidents.csv")

df.head()
df.shape
df.isnull().any()

df['category'] = df['category'].fillna('Software')
df.isnull().any()
df.shape
database = df['category'] == 'Database'
df_resampleTry = df[database]
df = df.append([df_resampleTry]*14, ignore_index=True)

network = df['category'] == 'Network'
df_resampleNet = df[network]
df = df.append([df_resampleNet]*6, ignore_index=True)

hardware = df['category'] == 'Hardware'
df_resampleHW = df[hardware]
df = df.append([df_resampleHW]*3, ignore_index=True)

software = df['category'] == 'Software'
df_resampleSW = df[software]
df = df.append([df_resampleSW]*2, ignore_index=True)

df['category'].value_counts()

x = df['short_description']
y = df['category']

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42)

y_train.shape

x_train.shape

count_vect = CountVectorizer()

x_train_count = count_vect.fit_transform(x_train)

x_train_count.toarray()

x_train_count.shape

transformerTfid = TfidfTransformer()

x_train_Tfid = transformerTfid.fit_transform(x_train_count)
x_train_Tfid.shape

clf = MultinomialNB().fit(x_train_Tfid, y_train)

text_clf = Pipeline([('Vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])


text_clf = text_clf.fit(x_train, y_train)


#Save the model
joblib.dump(text_clf, 'NB_TC_Model.pkl')

predicted = text_clf.predict(x_test)
prob = text_clf.predict_proba(x_test)

print(str(predicted[0]))
print(prob)
print(text_clf.classes_)
print(max(prob[0]))
