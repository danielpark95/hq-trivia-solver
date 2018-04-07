import nltk, csv, re, sys, pickle, copy
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

########################################
# Import HQ data
########################################
def import_hq_data(filename):
	questions, answers, correct_answers = [],[],[]
	with open(filename) as f:
		answer_choices = []
		for line in f.read().splitlines():
			if re.match(r'^[a-zA-Z0-9].*', line):
				questions.append(line)
				answers.append(answer_choices)
			elif re.match(r'.*[a-zA-Z0-9].*',line):
				tab_index = line.index('\t')
				if '*' in line:
					#print(line)
					correct_answers.append(line[tab_index+1:])
				answer_choices.append(line[tab_index+1:])
				if len(answer_choices) == 3:
					answer_choices = []
	return questions, answers, correct_answers

def import_n_hq_data(filename, num_examples):
	questions, answers, correct_answers = [],[],[]
	with open(filename) as f:
		answer_choices = []
		for line in f.read().splitlines():
			if re.match(r'^[a-zA-Z0-9].*', line):
				questions.append(line)
				answers.append(answer_choices)
			elif re.match(r'.*[a-zA-Z0-9].*',line):
				tab_index = line.index('\t')
				if '*' in line:
					#print(line)
					correct_answers.append(line[tab_index+1:])
				answer_choices.append(line[tab_index+1:])
				if len(answer_choices) == 3:
					answer_choices = []
					if len(answers)== num_examples:
						break
	return questions, answers, correct_answers

########################################
# Import Stop Words
########################################
def import_stop_words(filename, custom_words):
	stop_words = [] + custom_words			# add custom words
	with open(filename) as f:
		reader = csv.reader(f, delimiter='\t')
		for rank, word, pos, count, freq in reader:
			if pos.strip() != 'n':
				stop_words.append(word.strip())
	stop_words.remove('not') 					# we want to keep NOT
	return stop_words

########################################
# Tokenizer
########################################
def combine_tokens(tokens):
	compound_token = ""
	for index, token in enumerate(tokens):
		if index != len(tokens)-1:
			compound_token += format_token(token) + ' '
		else:
			compound_token += format_token(token)
	return compound_token


def find_compound_token_indices(tokens):
	# TODO: find consecutive uppercased words ("Best Picture Oscar")
	startIndices, endIndices = [], []
	for index, token in enumerate(tokens):
		if token.startswith('"') and not token.endswith('"'):
			startIndices.append(index)
		if token.endswith('"') and not token.startswith('"'):
			endIndices.append(index+1)
	indices = []
	for s, e in zip(startIndices, endIndices):
		indices.append([s,e])
	return indices

def not_compound(index, indices):
	for start, end in indices:
		if index >= start and index < end:
			return False
	return True

def start_of_compound(index,indices):
	for start, end in indices:
		if index == start:
			return True
	return False

def convert_to_ascii(token):
	ascii_token = re.sub(u'[\u2018\u2019\u0027\u0060\u0027]', "'", token)
	ascii_token = re.sub(u'[\u201c\u201d]', '"', ascii_token)
	return ascii_token

def format_token(token):
	new_token = convert_to_ascii(token)
	if new_token.endswith("?") or new_token.endswith(",") or new_token.endswith(".") or new_token.endswith("'"):
		new_token = new_token[:-1]
	if len(new_token) > 2:
		if new_token[-2] == ',':
			new_token = new_token[:-2] + new_token[-1]
	if new_token.endswith("'s"):
		new_token = new_token[:-2]
	return new_token

def remove_duplicates(tokenized_questions):
	removed = []
	[removed.append(tq) for tq in tokenized_questions if tq not in removed]
	return removed

def get_compound_tokens(tokens):
	compound_tokens = []
	compound_tokens_lower = []
	compound_indices = find_compound_token_indices(tokens)
	compound_count = 0
	for start, end in compound_indices:
		compound_tokens.append(combine_tokens(tokens[start:end]))
		compound_tokens_lower.append(combine_tokens(tokens[start:end]).lower())
	return compound_tokens, compound_tokens_lower, compound_indices, compound_count

def get_final_tokens(tokens, compound_tokens, compound_tokens_lower, compound_indices, compound_count):
	final_tokens = []
	final_tokens_lower = []
	for index, token in enumerate(tokens):
		formatted_token = format_token(token)
		if not_compound(index, compound_indices) and formatted_token not in final_tokens:
			final_tokens.append(formatted_token)
			final_tokens_lower.append(formatted_token.lower())
		elif start_of_compound(index,compound_indices):
			final_tokens.append(compound_tokens[compound_count])
			final_tokens_lower.append(compound_tokens_lower[compound_count])
			compound_count += 1
	return final_tokens, final_tokens_lower

def tokenize_questions(questions):
	tokenized_questions = []
	tokenized_questions_lower = []
	for q in questions:
		raw_tokens = q.split()
		formatted_tokens = [format_token(raw_token) for raw_token in raw_tokens]
		compound_tokens, compound_tokens_lower, \
			compound_indices, compound_count = get_compound_tokens(formatted_tokens)
		final_tokens, final_tokens_lower = get_final_tokens(formatted_tokens, compound_tokens, \
			compound_tokens_lower, compound_indices, compound_count)
		tokenized_questions.append(final_tokens)
		tokenized_questions_lower.append(final_tokens_lower)
	return tokenized_questions, tokenized_questions_lower

########################################
# Key Words
########################################
def get_key_words(tokenized_questions, stop_words):
	key_words = []
	for tq in tokenized_questions:
		mylist = []
		for t in tq:
			if t not in stop_words:
				mylist.append(t)
		key_words.append(mylist)

	wh_removed_key_words = copy.deepcopy(key_words)
	for i in range(len(tokenized_questions)):
		tq = tokenized_questions[i]
		if 'which' in tq or 'what' in tq:
			if 'which' in tq:
				wh_index = tq.index('which')
			else:
				wh_index = tq.index('what')
			for j in range(len(key_words[i])):
				key_word_index = tq.index(key_words[i][j])
				if key_word_index <= wh_index + 3 and key_word_index > wh_index and key_words[i][j] != 'not':
					wh_removed_key_words[i].remove(key_words[i][j])
	return wh_removed_key_words

########################################
# Lemmatizer
########################################
def get_lemmatized_key_words(key_words):
	l = WordNetLemmatizer()
	lemmatized_key_words = []
	for token_list in key_words:
		tmpList = []
		for token in token_list:
			tmpList.append(l.lemmatize(token))
		lemmatized_key_words.append(tmpList)
	return key_words

########################################
# Export key words
########################################
def export_key_words(filename, questions, key_words, answers, correct_answers):
	with open (filename, 'w') as output:
		for row in range(len(questions)):
			pickle.dump(questions[row], output)
			pickle.dump(key_words[row], output)
			pickle.dump(answers[row], output)
		output.close()

########################################
# Return all results
########################################
def get_n(hq_data_filename, stop_words_filename, custom_words, n):
	questions, answers, correct_answers = import_n_hq_data(hq_data_filename,n)
	stop_words = import_stop_words(stop_words_filename, custom_words)[:500] 
	tokenized_questions, tokenized_questions_lower = tokenize_questions(questions)
	key_words = get_key_words(tokenized_questions_lower, stop_words)
	lemmatized_key_words = get_lemmatized_key_words(key_words)
	return questions, answers, correct_answers, stop_words, \
		tokenized_questions, tokenized_questions_lower,  key_words, lemmatized_key_words


########################################
# Return all results
########################################
def get_all(hq_data_filename, stop_words_filename, custom_words):
	questions, answers, correct_answers = import_hq_data(hq_data_filename)
	stop_words = import_stop_words(stop_words_filename, custom_words)[:500] 
	tokenized_questions, tokenized_questions_lower = tokenize_questions(questions)
	key_words = get_key_words(tokenized_questions_lower, stop_words)
	lemmatized_key_words = get_lemmatized_key_words(key_words)
	return questions, answers, correct_answers, stop_words, \
		tokenized_questions, tokenized_questions_lower,  key_words, lemmatized_key_words