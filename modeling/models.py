import numpy as np
import pandas as pd
import pdb

class ContinuousIncrementalRSA():
	def __init__(self, adjectives, nouns,
						objects, utterances, 
						alpha=5, 
						v_adj=0.95, v_noun=0.99,
						adj_cost=None, noun_cost=None):
		self.adjectives = adjectives
		self.nouns = nouns
		self.objects = objects
		self.utterances = utterances
		self.alpha = alpha
		self.v_adj = v_adj
		self.v_noun = v_noun
		self.adj_cost = adj_cost
		self.noun_cost = noun_cost


	def normalize_rows(self, matrix):
		"""
		Helper function that normalize probabilities across rows to sum to 1
		"""
		totals = np.sum(matrix, axis=1)
		return matrix / totals[:, np.newaxis]


	def continuous_meaning(self, obj, utt):
		"""
		Given an object and an utterance, return the semantic value associated with
		that utterance
		"""

		def token_applies_to_obj(obj, token):
			return token in obj.values()

		total = 1
		for token in utt.split():
			if token_applies_to_obj(obj, token):
				if token in self.adjectives: total *= self.v_adj
				if token in self.nouns: total *= self.v_noun
			else:
				if token in self.adjectives: total *= (1 - self.v_adj)
				if token in self.nouns: total *= (1 - self.v_noun)
					
		return total


	def cost(self, utt):
		"""
		Return the production cost for the given utterance
		"""
		if utt in self.nouns and self.noun_cost is not None: return self.noun_cost
		if utt in self.adjectives and self.adj_cost is not None: return self.adj_cost

		return 0


	def inc_cont_meaning(self, obj, utt):
		num_true_extensions = []
		num_possible_extensions = []
		
		utility = 0
		for curr_utt in self.utterances:
			
			utt_starts_with = curr_utt.startswith(utt)
			
			if utt_starts_with:
				num_possible_extensions.append(curr_utt)
				
				curr_utt_as_tokens = curr_utt.split()
				utility += self.continuous_meaning(obj, utt)
				
		return utility/len(num_possible_extensions)


	def word_level_literal_listener(self, word, meaning_fn):
		"""
		generate the matrix of utterances x world states
		"""
		all_counts = np.zeros(shape=(len(self.utterances), len(self.objects)))
		for i in range(len(self.utterances)):
			for j in range(len(self.objects)):
				curr_utt = self.utterances[i]
				curr_obj = self.objects[j]

				all_counts[i, j] = meaning_fn(curr_obj, curr_utt)
		
		data = self.normalize_rows(all_counts)
		df_cols = [obj["string"] for obj in self.objects]
		df = pd.DataFrame(data, columns=df_cols, index=self.utterances)
		return df, df.loc[word]


	def get_possible_completions(self, utt):
		"""
		Given a partial utterance, return all the possible completions
		"""
		max_utt_len = len(utt.split()) + 1
		
		possible_completions = []
		for curr_utt in self.utterances:
			if curr_utt.startswith(utt) and len(curr_utt.split()) <= max_utt_len:
				possible_completions.append(curr_utt)
				
		return possible_completions


	def word_level_pragmatic_speaker(self, obj, context):
		"""
		Given an object and a context, get the associated probabilities over all possible 
		continuations of the context
		"""
		all_vals = []
		possible_utterances = self.get_possible_completions(context)
		for curr_utt in possible_utterances:
			_, probs = self.word_level_literal_listener(curr_utt, meaning_fn=self.inc_cont_meaning) # specify meaning_fn here
			utility = np.array(probs)
			val = np.exp(self.alpha * (np.log(utility) - self.cost(curr_utt)))

			all_vals.append(val)

		data = self.normalize_rows(np.array(all_vals).T)
		df_idx = [obj["string"] for obj in self.objects]
		df = pd.DataFrame(data, columns=possible_utterances, index=df_idx)
		
		return df, df.loc[obj["string"]]


	def incremental_pragmatic_speaker(self, obj, utt):
		"""
		Compute the product of the probabilities produced by the incremental speaker
		"""
		all_vals = []
		utt_len = len(utt.split())
		context = ''
		val = 1
		
		"""
		in order to avoid the issue where 1 token utterances are always higher probability
		than 2 token utterances (regardless of the object), we need to iterate over both
		the tokens (if it's a 2 token utterance) or the single token and a null token (if
		it's a 1 token utterance)
		"""
		for i in range(2):	
			breakpoint()
			_, probs = self.word_level_pragmatic_speaker(obj, context)
			partial_utt = " ".join(utt.split()[:i+1])

			if len(probs.shape) == 2:	# handling the case where there are duplicate objects
				probs = probs.iloc[0]

			index_of_partial_utt = list(probs.index).index(partial_utt)
			val *= probs[index_of_partial_utt]

			context = partial_utt

		return val
