import csv
import numpy as np

class CombineModels(object): 
	def __init__(self, bing_counts, wiki_counts, key_words, answers):
		#guess = ''
		if sum(bing_counts) == 0:
			# both [0,0,0]
			if sum(wiki_counts) == 0:
				guess = answers[2] # guess last one
				final_counts = [0,0,0]
			# only wiki has answer
			else:
				guess = self.guess_answer_one_model(wiki_counts, key_words, answers)
				final_counts = wiki_counts
		else:
			# only bing has answer
			if sum(wiki_counts) == 0:
				guess = self.guess_answer_one_model(bing_counts,key_words,answers)
				final_counts = bing_counts
			else:
				# both have answers, calculate
				final_counts, guess = self.guess_answer_two_models(bing_counts,wiki_counts,key_words,answers)
		self.final_counts = final_counts
		self.guess = guess

	def guess_answer_two_models(self, bing_counts, wiki_counts, key_words, answers):


		bing_sd = np.std(np.array(bing_counts))
		bing_mean = np.mean(bing_counts)
		wiki_sd = np.std(np.array(wiki_counts))
		wiki_mean = np.mean(wiki_counts)

		bing_norm = [(x - bing_mean) / bing_sd for x in bing_counts]
		wiki_norm = [(x - wiki_mean) / wiki_sd for x in wiki_counts]

		final_counts = [sum(x) for x in zip(bing_norm,wiki_norm)]

		guess = self.guess_answer_one_model(final_counts, key_words, answers)

		# #max_count = max(final_counts)
		# if 'not' in key_words:
		# 	count = min(final_counts)
		# else:
		# 	count = max(final_counts)
		# index = final_counts.index(count)
		# guess = answers[index]
		return final_counts, guess

	def guess_answer_one_model(self, final_counts, key_words,answers):
		#count = 0
		#index = 0
		if "not" in key_words:
			count = min(final_counts)
			#sorted_list = sorted(final_counts)
		else:
			count = max(final_counts)
			#sorted_list = sorted(final_counts, reverse = True)

		index = final_counts.index(count)
		return answers[index]


# output = []
# with open ('output.csv', newline = '\n') as csvfile:
# 	reader = csv.reader(csvfile, delimiter= ',', quotechar='"')
# 	for row in reader:
# 		output.append(row)
# 		#print(row)

# data_csv = []
# with open('answers.csv', newline = '\n') as csvfile:
# 	reader = csv.reader(csvfile, delimiter = ',', quotechar='"')
# 	for row in reader:
# 		data_csv.append(row)
# 		#print(row)

# bing_guesses = output[0]
# wiki_guesses = output[2]
# correct_answers = data_csv[0]

#print(len(bing_guesses))
#print(len(wiki_guesses))
#print(len(correct_answers))


