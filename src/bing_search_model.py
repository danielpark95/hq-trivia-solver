import requests, pprint, json
import urllib.request
import re
import pprint
from bs4 import BeautifulSoup
from markdown import markdown

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


subscription_key = "1b10cb439d184096b730f1e066ec5d1a"
class BingSearchModel(object):

	def __init__(self, key_words, answers):

		key_words_lower = self.lower_key_words(key_words)
		answers_lower = self.lower_answers(answers)

		kw_query = ' '.join(key_words_lower)

		#print("kw_query = ", kw_query)

		kw_search_results = self.get_search_results(kw_query)
		#pprint.pprint(kw_search_results)

		dict_url = self.make_dict(kw_search_results)

		#print ("BingSearchModel Key Words =", key_words)

		final_counts = self.count_all_answer_appearances_in_dict(dict_url,answers,kw_search_results)
		#print("final counts =", final_counts)


		self.guess = self.guess_answer(final_counts, key_words, answers)
		#print("Bing guess =", guess)

	def format_answer(self, answer):
		answer_lower = answer.lower()
		answer_stripped_dq = answer_lower.replace('"','')
		answer_stripped_sq = answer_stripped_dq.replace("'",'')
		return answer_stripped_sq


	def count_answer_appearances_in_text (self, text, answer):
		answer_formatted = self.format_answer(answer)
		count, last_index = 0,0
		found = True
		while found:
			curr_index = text.find(answer_formatted, last_index)
			if curr_index == -1:
				found = False
			else:
				count += 1
				last_index = curr_index + len(answer_formatted)
		return count


	def count_all_answer_appearances_in_text (self, text, answers):
		count = [0,0,0]
		for i in range(len(answers)):
			count[i] = self.count_answer_appearances_in_text(text,answers[i])
		return count

	def count_all_answer_appearances_in_dict (self, dict_url, answers, search_results):
		urls = self.get_urls(search_results)
		count_list = []
		for url in urls:
			text = dict_url[url]
			count = self.count_all_answer_appearances_in_text(text,answers)
			count_list.append(count)
		
		final_counts = [0,0,0]
		for i in range(len(count_list)):
			final_counts[0] += count_list[i][0]
			final_counts[1] += count_list[i][1]
			final_counts[2] += count_list[i][2]

		return final_counts


	def guess_answer(self, final_counts, key_words,answers):
		if "not" in key_words:
			sorted_list = sorted(final_counts)
		else:
			sorted_list = sorted(final_counts, reverse = True)

		index = final_counts.index(sorted_list[0])
		return answers[index]

	def lower_key_words(self,key_words):
		for kws in key_words:
			for kw in kws:
				kw = kw.lower()
		return key_words

	def lower_answers(self,answers):
		for ans in answers:
			for a in ans:
				a = a.lower()
		return answers

	def get_urls (self, search_results):
		urls = []
		items = search_results.get('webPages').get('value')[:5]
		for item in items:
			url = item.get('url')
			urls.append(url)
		return urls

	def make_dict(self, search_results):
		dict_url = {}
		items = search_results.get('webPages').get('value')[:5] #get top 5
		for item in items:
			url = item.get('url')
			#print ('url =', url)
			url_text = self.get_url_text(url)
			#print ('url_text =', url_text)
			dict_url[url] = url_text
			#print ('dict_url[url] =', dict_url[url])
		#print (dict_url)
		return dict_url

	def get_url_text(self, query_url):
		try:
			opener = AppURLopener()
			html = opener.open(query_url)
			text = ''.join(BeautifulSoup(html, 'html5lib').getText())
			formatted_text = ' '.join(re.split('\s+', text, flags=re.UNICODE))


		except:
			formatted_text = ''
		#url_json = urllib.request.urlopen(query_url)
		#data = json.loads(url_json.read().decode('utf-8'))
		#data = requests.get(url=query_url).json()
		#print(formatted_text)
		return formatted_text.lower()

	def get_search_results(self, query):
		headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
		search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
		search_term = query
		params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML"}
		response = requests.get(search_url, headers=headers, params=params)
		response.raise_for_status()
		search_results = response.json()
		return search_results

	def get_num_matches(self, json_page):
		matches = json_page.get('webPages').get('totalEstimatedMatches')
		return matches


