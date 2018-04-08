import sys
import preprocess_data as pp
import question as qu
import wiki_answer_model as wam
import google_search_model as gsm
import bing_search_model as bsm
import combine_models as cm
import pprint
import time
import csv

def main():
	########################################
	# File paths and custom words
	########################################
	hq_data_filename = 'input_data/hq_data.txt'
	stop_words_filename = 'input_data/word_frequency.txt'
	custom_words = \
		['am','are','is','was','were','being','been',
		'has','had', 'an', 'does', 'done', 'did' ,'&',
		'type', 'goes', 'gone']

	########################################
	# Import Data
	########################################
	num_q = 125

	questions, answers, correct_answers, stop_words, tokenized_questions,\
		tokenized_questions_lower,  key_words, lemmatized_key_words \
		= pp.get_n(hq_data_filename,stop_words_filename, custom_words,num_q)



	# answer_dist = [0,0,0]
	# for i in range(len(answers)):
	# 	for j in range(3):
	# 		if (answers[i][j] == correct_answers[i]):
	# 			answer_dist[j] += 1
	# print("answer dist =", answer_dist)

	# answers_csv = 'answers.csv'
	# data_output = [correct_answers]
	# with open (answers_csv, 'w') as output:
	# 	writer = csv.writer(output, lineterminator = '\n')
	# 	writer.writerows(data_output)

	########################################
	# Make Guesses!
	########################################
	bing_guesses = []
	bing_all_counts = []
	bing_num_correct = 0
	bing_total_time = 0

	wiki_guesses = []
	wiki_all_counts = []
	wiki_num_correct = 0
	wiki_total_time = 0


	wiki_true_correct = 0
	wiki_true_num_questions = 0


	final_guesses = []
	final_num_correct = 0

	for i in range(num_q):
		print("***************************")
		print("QUESTION", (i+1),"\n")
		print("Q:", questions[i])
		print("A:", answers[i])
		print("KW:",key_words[i],"\n")

		#print("--BING SEARCH MODEL--")
		bing_start = time.time()
		bing_model = bsm.BingSearchModel(key_words[i], answers[i])
		bing_end = time.time()
		bing_time_diff = (bing_end - bing_start)
		bing_total_time += bing_time_diff
		bing_guess = bing_model.guess
		bing_guesses.append(bing_guess)
		bing_all_counts.append(bing_model.final_counts)
		
		#print("Bing Guess:", bing_guess)
		if bing_guess == correct_answers[i]:
			#print("Guess is correct!\n")
			bing_num_correct += 1 
		# else:
		# 	print("Wrong!\n")
		#print("Bing Search Model took {} seconds".format(bing_time_diff))

		#print("--WIKI SEARCH MODEL--")
		wiki_start = time.time()
		wiki_model = wam.WikiAnswerModel(key_words[i], answers[i])
		wiki_end = time.time()
		wiki_time_diff = (wiki_end - wiki_start)
		wiki_total_time += wiki_time_diff
		wiki_guess = wiki_model.guess
		wiki_guesses.append(wiki_guess)
		wiki_all_counts.append(wiki_model.total_cooccurrences_list)

		#print("Wiki Guess:", wiki_guess)
		if wiki_guess == correct_answers[i]:
			#print("Guess is correct!\n")
			wiki_num_correct += 1
		# else:
		# 	print("Wrong!\n")


		combine_model = cm.CombineModels(
			bing_model.final_counts,\
			wiki_model.total_cooccurrences_list,\
			key_words[i],
			answers[i]
		)
		final_guess = combine_model.guess
		final_counts = combine_model.final_counts


		final_guesses.append(final_guess)
		print("Bing Final Counts:", bing_model.final_counts)
		print("Bing Guess =", bing_guess)
		print("Wiki Final Counts:", wiki_model.total_cooccurrences_list)
		print("Wiki Guess =", wiki_guess)
		print("Final Counts:", final_counts)
		print("Final Guess =", final_guess)


		if final_guess == correct_answers[i]:
			print("Correct!")
			final_num_correct += 1
		else:
			print("Wrong! Correct answer is {}.".format(correct_answers[i]))
		# if sum(wiki_model.total_cooccurrences_list) > 0:
		# 	wiki_true_num_questions += 1
		# 	if wiki_guess == correct_answers[i]:
		# 		wiki_true_correct += 1

		#print("Wiki Search Model took {} seconds".format(wiki_time_diff))
		print("***************************\n")

	########################################
	# Calculate model performance
	########################################
	print("=========== Results ============")

	print("*** Bing Search Model ***")
	print("Got {}/{} questions correct.".format(bing_num_correct, len(questions)))
	print("Accuracy = {}%".format(round(bing_num_correct/len(questions)*100,1)))
	print("Took {} per question to guess, on average.".format(bing_total_time/len(questions)))

	print("*** Wikipedia Answer Model ***")
	print("Got {}/{} questions correct.".format(wiki_num_correct, len(questions)))
	print("Accuracy = {}%\n".format(round(wiki_num_correct/len(questions)*100,1)))
	#print("True Correct =", wiki_true_correct)
	#print("True Num Questions =", wiki_true_num_questions)
	#print("True Accuracy = {}%\n".format(round(wiki_true_correct/wiki_true_num_questions*100,1)))
	print("Took {} per question to guess, on average.".format(wiki_total_time/len(questions)))

	print("*** Combined Model ***")
	print("Got {}/{} questions correct.".format(final_num_correct, len(questions)))
	print("Accuracy = {}%".format(round(final_num_correct/len(questions)*100,1)))
	print("================================")

	########################################
	# Export Answers
	########################################
	export = False
	if export:
		csvfile = 'output.csv'
		bing_output = [bing_guesses, [bing_num_correct, (bing_num_correct/len(questions)), bing_total_time, (bing_total_time/len(questions))]]
		wiki_output = [wiki_guesses, [wiki_num_correct, (wiki_num_correct/len(questions)), wiki_total_time, (wiki_total_time/len(questions))]]
		with open (csvfile, 'w') as output:
			writer = csv.writer(output, lineterminator = '\n')
			writer.writerows(bing_output)
			writer.writerows(wiki_output)

	########################################
	# Print for debugging
	########################################
	debug = False
	if debug:
		for q, ans, tq, tql, kw, lw, tc, wg in zip(
								questions,
								answers,
								tokenized_questions,
								tokenized_questions_lower,
								key_words,
								lemmatized_key_words,
								wiki_total_cooccurences_list,
								wiki_guesses):
			print(
				"question =", q, 
				"\nanswers =", ans,
				"\ntokenized_questions = ", tq,
				"\ntokenized_questions_lower = ", tql,
				"\nkey_words =", kw,
				"\nlemmatized_key_words =", lw,
				"\nwiki_total_cooccurences_list =", tc,
				"\nguesses =", wg)
			print('\n')

if __name__ == '__main__':
	sys.exit(main())