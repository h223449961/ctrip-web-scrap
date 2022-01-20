import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import warnings
import nltk
import re
import string
warnings.filterwarnings('ignore')
import requests
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from styleframe import StyleFrame, Styler
from nltk.corpus import stopwords
EngStopWords = set(stopwords.words('english'))
respon = requests.get('https://tw.hotels.com/ho246909')
res = BeautifulSoup(respon.content, 'lxml')
comments = res.find_all('p',class_='oZl9tt')
df01 = pd.DataFrame(columns=["評論",'字詞','強烈'])
xon = []
for words in res.findAll('p',class_='oZl9tt'):  
        word = words.string
        if word is None:
            print("NO WORD")
        else:
            #print(word)
            sentence = nltk.word_tokenize(word)
            sent = nltk.pos_tag(sentence)
            zon = []
            for s in sent:
                if s[1]=='JJ':
                    #print(s[0])
                    zon.append(s[0])
                    vetype = ' '.join([str(elem) for elem in zon])
                    surie = pd.Series([word,vetype], index=['評論','字詞'])
            xon.append(word)
            df01 = df01.append(surie, ignore_index=True)
            df01.index = df01.index+1
#print(df01)
n = 3 # top n TF-IDF words
tfidf = TfidfVectorizer(token_pattern=r"\w+") # no words are left out
X = round(tfidf.fit_transform(df01['字詞']),3)
ind = (-X.todense()).argpartition(n)[:, :n]
top_words = pd.Series(
    map(
        lambda words_values: dict(zip(*words_values)),
        zip(
            np.array(tfidf.get_feature_names())[ind],
            np.asarray(np.take_along_axis(X, ind, axis=1).todense()),
        ),
    ),
)
top_words.index += 1
#print(top_words)
df01['強烈'] = top_words
#print(df01)
print(df01['強烈'])
aresut = []
bresut = []
cresut = []
mresut = []
nresut = []
gresut = []
for ind in df01.index:
    values = [float(x) for x in list(df01['強烈'][ind].values())]
    word = [str(x) for x in list(df01['強烈'][ind].keys())]
    print(word)
    a = values[0]
    b = values[1]
    c = values[2]
    m = word[0]
    n = word[1]
    g = word[2]
    aresut.append(a)
    bresut.append(b)
    cresut.append(c)
    mresut.append(m)
    nresut.append(n)
    gresut.append(g)
df01['強烈字詞一'] = mresut
strongmap =  {'nice':0 , 'great':12, 'good':2} 
df01['強烈分數一'] = df01['強烈字詞一'].map(strongmap)
df01['強烈經元一'] = aresut
df01['強烈字詞二'] = nresut
df01['強烈分數二'] = df01['強烈字詞二'].map(strongmap)
df01['強烈經元二'] = bresut
df01['強烈字詞三'] = gresut
df01['強烈分數三'] = df01['強烈字詞三'].map(strongmap)
df01['強烈經元三'] = cresut
print(df01)
sf = StyleFrame(df01)
sf.set_column_width_dict(col_width_dict={("評論"): 68,("字詞"): 43,("強烈"):68})
sname = 'ogc.xlsx'
output = sf.to_excel(sname).save()