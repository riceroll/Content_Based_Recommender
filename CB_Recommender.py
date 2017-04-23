import sys

import csv
import re
import nltk

# Parameters =====================================
# the paper to be recommended for
try:
	paper_ID = int(sys.argv[1])
except:
	paper_ID=1
# all the papers to be recommended from
file_papers="papers_NLP.csv"

# Variables ======================================
# store the paperIDs and abstracts
PaperID=[]
abstract=[]
size = 0
# get data from the csv
cur=[] 		
with open("papers_NLP.csv","rb") as f:
	reader=csv.reader(f)
	for row in reader:
		cur.append(tuple(row))
del(cur[0])
tuple(cur)

# Text Filtering ==================================
# filter html & formula
regex1 = re.compile("<math>.*?</math>")
regex2 = re.compile("<url>.*?</url>")
regex3 = re.compile("<.*?>")
regex4 = re.compile("&.*?;")
regex5 = re.compile("/.*?>")
regex6 = re.compile("i>")
# read the file into variables
i=0
for row in cur:
	if len(row)>1:
		PaperID.append(row[0])
		string = row[1]
		sub1=re.sub(regex1,'',string)
		sub2=re.sub(regex2,'',sub1)
		sub3=re.sub(regex3,'',sub2)
		sub4=re.sub(regex4,'',sub3)
		sub5=re.sub(regex5,'',sub4)
		sub = re.sub(regex6,'',sub5)
		abstract.append(sub)
		size += 1
print size
# lower the text
text_lower = [[word for word in document.lower().split()]for document in abstract]
# tokenize the text
from nltk.tokenize import word_tokenize                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
texts_tokenized = [[word.lower() for word in word_tokenize(document.decode(encoding='UTF-8',errors='ignore'))]for document in abstract]
# filter stop words
from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')
texts_filtered_stopwords = [[word for word in document if not word in english_stopwords]for document in texts_tokenized]
# filter punctuations
english_punctuations = [',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%','...','<','>','^','{','}','\\','/']
texts_filtered = [[word for word in document if not word in english_punctuations]for document in texts_filtered_stopwords]
print "Fliter Finished"

# Text stemming ===============================================================================
from nltk.stem.lancaster import LancasterStemmer
st= LancasterStemmer()
texts = [[st.stem(word)for word in document]for document in texts_filtered]
print "Stemming Finished"

# Content-based calculation ===================================================================
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

#Extract documnent as bog of words 
#Giving an ID number to each unique token 
dictionary = corpora.Dictionary(texts)
#Counting the frequence of the word, represent as [(0,1),(1,5)]
corpus = [dictionary.doc2bow(text) for text in texts]
#Counting tfidf
tfidf = models.TfidfModel(corpus)
#Represent document as document vector using tfidf: [[(0,0.2),(3,0.1)],[(2,0.3),(5,0.1)]]
corpus_tfidf = tfidf[corpus]

#Building LSI Model 
lsi = models.LsiModel(corpus_tfidf,id2word=dictionary,num_topics=30)
#Transforming corpus to LSI space and index it to initial the query structure
index = similarities.MatrixSimilarity(lsi[corpus])

# Commend papers for a specific paper ==========================================================
doc=texts[paper_ID]
vec_bow = dictionary.doc2bow(doc)
doc_lsi = lsi[vec_bow]
sims = index[doc_lsi]
sort_sims = sorted(enumerate(sims),key=lambda item:-item[1])
# write the result
f = open('Recommend4Paper_'+PaperID[paper_ID]+'.txt', 'w')
for i in range (0,500):
	f.write( str(sort_sims[i][1])+","+str(PaperID[sort_sims[i][0]])+"\n")
f.close()


