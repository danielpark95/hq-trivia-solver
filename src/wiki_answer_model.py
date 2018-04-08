import urllib.request
import requests
import copy, re
class WikiAnswerModel(object):
	def __init__(self, key_words, answers):
		#print("initializing wiki answer model")
		self.wiki_pages = self.get_wiki_pages(answers)
		#print("got wiki pages")
		self.total_cooccurrences_list = self.get_total_cooccurrences_list(self.wiki_pages, key_words)
		
		#print("got total cooccurrences list")
		self.guess = self.guess_answer(self.total_cooccurrences_list, key_words, answers)
		
		#print("got guesses")
		self.all_cooccurrence_pairs = self.get_all_cooccurrence_pairs(self.wiki_pages,key_words)

		#print("got all occurrence pairs")

	def get_all_cooccurrence_pairs(self, wiki_pages,key_words):
		key_words_not_removed = list(key_words)
		if 'not' in key_words:
			key_words_not_removed.remove('not')
		cooccurrence_indices_list = [self.find_all_key_words_indices(wiki_pages[i],key_words_not_removed) for i in range(3)]
		all_cooccurrence_pairs = [self.all_cooccurrence_pairs(key_words_not_removed, cooccurrence_indices_list[i]) for i in range(3)]
		return all_cooccurrence_pairs

	def get_total_cooccurrences_list(self, wiki_pages, key_words):
		#print("entered get_total_cooccurrences_list")
		key_words_not_removed = list(key_words)

		if 'not' in key_words:
			key_words_not_removed.remove('not')
		cooccurrence_indices_list = [self.find_all_key_words_indices(wiki_pages[i],key_words_not_removed) for i in range(3)]
		#print("finished find_all_key_words_indices")
		total_cooccurrences_list = [self.total_cooccurrences(cooccurrence_indices_list[i]) for i in range(3)]
		#print("finished total_cooccurrences")
		#print("finished get_total_cooccurrences_list")
		return total_cooccurrences_list

	def convert_to_ascii(self, token):
		ascii_token = re.sub(u'[\u2018\u2019\u0027\u0060\u0027]', "'", token)
		ascii_token = re.sub(u'[\u201c\u201d]', '"', ascii_token)
		return ascii_token

	def lower_non_first(self, answer):
		new_answer = self.convert_to_ascii(answer)
		split_answer = new_answer.split()
		if len(split_answer) > 1:
			for i in range(1,len(split_answer)):
				split_answer[i] = split_answer[i].lower()
			lower_answer = ' '.join(split_answer)
		else:
			lower_answer = copy.copy(answer)
		return lower_answer

	def format_answer_lower(self, answer):
		#TODO: add more cases
		new_answer = self.lower_non_first(answer)
		if ' ' in answer:
			new_answer = new_answer.replace(' ', '_')

		if "'" in answer:
			new_answer = new_answer.replace("'", '%27')

		if '&' in answer:
			new_answer = new_answer.replace('&', '%26')
		return new_answer


	def format_answer_reg(self,answer):
		#TODO: add more cases
		new_answer = self.convert_to_ascii(answer)
		if ' ' in answer:
			new_answer = new_answer.replace(' ', '_')

		if "'" in answer:
			new_answer = new_answer.replace("'", '%27')

		if '&' in answer:
			new_answer = new_answer.replace('&', '%26')
		return new_answer


	def try_lower(self, answer):
		formatted_answer = self.format_answer_lower(answer)
		link = "https://en.wikipedia.org/w/index.php?format=json&action=raw&title=" + formatted_answer
		f = requests.get(link)
		return f

	def try_reg(self, answer):
		formatted_answer = self.format_answer_reg(answer)
		link = "https://en.wikipedia.org/w/index.php?format=json&action=raw&title=" + formatted_answer
		f = requests.get(link)
		return f

	def get_wiki_pages(self,answers):
		pages = []
		##print(answers)
		for answer in answers:
			f = self.try_lower(answer)
			page = ""
			if f.status_code == 404:
				f = self.try_reg(answer)
				if f.status_code != 404:
					page = f.text.lower()
			if '#REDIRECT' in f.text:
				index1 = f.text.index('[[')
				index2 = f.text.index(']]')
				redirect_answer = f.text[index1+2:index2]
				f = self.try_reg(redirect_answer)
				if f.status_code != 404:
					page = f.text.lower()
			page = f.text.lower()
			pages.append(page)
			# #print("answer =", answer)
			##print("answer = ", answer)
			##print("page = ", f.text[:100], "\n")

		return pages

	# return the highest/lowest cooccurrence count 
	def guess_answer(self, total_cooccurrences_list, key_words, answers):
		if "not" in key_words:
			sorted_list = sorted(total_cooccurrences_list)
		else:
			sorted_list = sorted(total_cooccurrences_list, reverse = True)

		index = total_cooccurrences_list.index(sorted_list[0])
		return answers[index]

	# totalCooccurrence
	# count all co-occurrences of key_words in a page 
	def total_cooccurrences(self, key_word_indices):
		count = 0
		for i in range(len(key_word_indices)):
			for j in range(i+1, len(key_word_indices)):
				count += self.count_coccurrences(key_word_indices[i], key_word_indices[j])
		return count

	# countCooccurrence
	# count co-occurrences of all two word pairs appearing within a window from list1 and list2
	def count_coccurrences(self, key_word_index_list1, key_word_index_list2):
		count = 0
		window = 500
		for i in range(len(key_word_index_list1)):
			for j in range(i+1,len(key_word_index_list2)):
				if abs(key_word_index_list1[i] - key_word_index_list2[j]) <= window:
					count += 1
		return count

	def all_cooccurrence_pairs(self,key_words,key_word_indices):
		all_cooccurrence_pairs = []
		for i in range(len(key_words)):
			for j in range(i+1, len(key_words)):
				all_cooccurrence_pairs.append(self.cooccurrence_pairs(key_words[i],key_words[j],key_word_indices[i],key_word_indices[j]))
		return all_cooccurrence_pairs

	def cooccurrence_pairs(self,key_word1,key_word2,key_word_index_list1,key_word_index_list2):
		cooccurrence_pairs = []
		window = 100
		for i in range(len(key_word_index_list1)):
			for j in range(i+1,len(key_word_index_list2)):
				if abs(key_word_index_list1[i] - key_word_index_list2[j]) <= window:
					##print("difference =", key_word_index_list1[i] - key_word_index_list2[j])
					##print(key_word_index_list1[i],"[",key_word1,"]",key_word_index_list2[j],"[",key_word2,"]")
					cooccurrence_pairs.append([key_word1,key_word2])
		return cooccurrence_pairs

	# getAllFeatureIndices
	# list of index list for all key_words in a wiki page
	def find_all_key_words_indices(self, page, key_words):
		list = []
		#print("page =", page[:100])
		#print("key words =", key_words)
		for i in range(len(key_words)):
			#print("i = {} started the loop".format(i))
			list.append(self.find_key_word_indices(page, key_words[i]))
			#print("i = {} ended the loop".format(i))
		return list

	# getFeatureIndices
	# helper for find_all_cooccurence_indeices - returns index list for a key_word in a wiki page
	def find_key_word_indices(self, page, key_word):
		list = []
		last_index = 0
		#print("entered find_key_word_indices")
		while key_word in page[last_index:]:
			stripped_key_word = key_word.replace('"','')
			if len(stripped_key_word) == 0:
				break
			#print("stripped_key_word =", stripped_key_word)
			last_index = page.index(stripped_key_word, last_index)
			list.append(last_index)
			last_index += len(stripped_key_word)
			#print("last index =", last_index)
		#print("finished find_all_key_words_indices")
		return list









