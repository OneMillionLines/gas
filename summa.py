from flask import Flask, request
import json
import threading
from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import urllib2
from bs4 import BeautifulSoup
from flask import Flask
import json
import threading
from random import random

app = Flask(__name__,static_url_path="")

	
class FrequencySummarizer:
	def __init__(self, min_cut=0.1, max_cut=0.9):
		self._min_cut = min_cut
		self._max_cut = max_cut 
		self._stopwords = set(stopwords.words('english') + list(punctuation))
	def _compute_frequencies(self, word_sent):
		freq = defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in self._stopwords:
					freq[word] += 1
		m = float(max(freq.values()))
		for w in list(freq):
			freq[w] = freq[w]/m
			if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
				del freq[w]
		return freq
    
	def summarize(self, text, n):
		sents = sent_tokenize(text)
		assert n <= len(sents)
		word_sent = [word_tokenize(s.lower()) for s in sents]
		self._freq = self._compute_frequencies(word_sent)
		ranking = defaultdict(int)
		for i,sent in enumerate(word_sent):
			for w in sent:
				if w in self._freq:
					ranking[i] += self._freq[w]
		sents_idx = self._rank(ranking, n)    
		return [sents[j] for j in sents_idx]
		
	def _rank(self, ranking, n):
		return nlargest(n, ranking, key=ranking.get)
		
def get_only_text(url):
	page = urllib2.urlopen(url).read().decode('utf8')
	soup = BeautifulSoup(page,"html.parser")
	text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
	return soup.title.text, text

@app.route("/abridge", methods=['GET','POST'])
def func():
	try:
		data=request.data
		print(data)
		print("Hello here")
		data=data.encode("utf-8")
		data=data.decode('ascii','ignore')

		url,lines = data.split('~')
		n = int(lines)
		#feed_xml = urllib2.urlopen('https://www.nytimes.com/').read()
		#print('--------------------------------FEED_XML-------------------------------')
		#print(feed_xml)
		#print('--------------------------------FEED-------------------------------')
		#feed = BeautifulSoup(feed_xml.decode('utf8'),"html.parser")
		#print(feed)
		#print('--------------------------------TO SUMMARIZE-------------------------------')
		#to_summarize = list(map(lambda p: p.text, feed.find_all('a',href=True)))
		to_summarize=[url]
		#for i in feed.find_all('a',href=True):
		#	if '#' not in i['href']:
		#			to_summarize.append(i['href'])
		print(to_summarize)
		fs = FrequencySummarizer()
		#to_summarize=['https://domypapers.com/blog/syrian-refugees/']
		for article_url in to_summarize:
			xx=""
			title, text = get_only_text(article_url)
			print('----------------------------------')
			print(title)
			xx+='<html><head><link href="https://fonts.googleapis.com/css?family=Poiret+One|Sanchez" rel="stylesheet"> <link rel="stylesheet" type="text/css" href="window.css"></head><body><h1>'+title+'</h1>'
			for s in fs.summarize(text, n):
				xx+="<p> * "+s+"</p>"
				print ('*',s)
			xx+="</body></html>"	
		return str(xx)
	except urllib2.URLError:
		return '<html><head><link href="https://fonts.googleapis.com/css?family=Poiret+One|Sanchez" rel="stylesheet"> <link rel="stylesheet" type="text/css" href="window.css"></head><body><p>This url cannot be summarized</p></body></html>'
if __name__=="__main__":
	app.run(host='localhost',debug=True)