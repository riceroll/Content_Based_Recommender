import nltk
import csv
import re

paper_ID=1213

cur=[]
with open("papers_NLP.csv","rb") as f:
	reader=csv.reader(f)
	for row in reader:
		cur.append(tuple(row))
del(cur[0])
tuple(cur)

PaperID=[]
abstract=[]
size = 0

regex1 = re.compile("<math>.*?</math>")
regex2 = re.compile("<url>.*?</url>")
regex3 = re.compile("<.*?>")
regex4 = re.compile("&.*?;")
regex5 = re.compile("/.*?>")
regex6 = re.compile("i>")

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

text_lower = [[word for word in document.lower().split()]for document in abstract]


from nltk.tokenize import word_tokenize                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
texts_tokenized = [[word.lower() for word in word_tokenize(document.decode(encoding='UTF-8',errors='ignore'))]for document in abstract]


from nltk.corpus import stopwords
english_stopwords = stopwords.words('english')


texts_filtered_stopwords = [[word for word in document if not word in english_stopwords]for document in texts_tokenized]


english_punctuations = [',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%','...','<','>','^','{','}','\\','/']
texts_filtered = [[word for word in document if not word in english_punctuations]for document in texts_filtered_stopwords]
print "Fliter Finished"

from nltk.stem.lancaster import LancasterStemmer
st= LancasterStemmer()


texts = [[st.stem(word)for word in document]for document in texts_filtered]
print "Stemming Finished"

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

doc=texts[paper_ID]
vec_bow = dictionary.doc2bow(doc)
doc_lsi = lsi[vec_bow]

sims = index[doc_lsi]
sort_sims = sorted(enumerate(sims),key=lambda item:-item[1])

print sort_sims[0:10]
f = open('Recommend4Paper_'+PaperID[paper_ID]+'.txt', 'w')

for i in range (0,500):
	f.write( str(sort_sims[i][1])+","+str(PaperID[sort_sims[i][0]])+"\n")
	
f.close()


