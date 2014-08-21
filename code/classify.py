from words import text_to_list
from train import train

class classify:
	MIN_WORD_COUNT = 5
	RARE_WORD_PROB = 0.5
	EXCLUSIVE_WORD_PROB = 0.8
	

	def p_for_word(self, db, word):
		total_word_count = self.doctype1_word_count + self.doctype2_word_count

		word_count_doctype1 = db.get_word_count(self.doctype1, word)
		word_count_doctype2 = db.get_word_count(self.doctype2, word)
		
		if word_count_doctype1 + word_count_doctype2 < self.MIN_WORD_COUNT:
			return self.RARE_WORD_PROB

		if word_count_doctype1 == 0:
				return 1 - self.EXCLUSIVE_WORD_PROB
		elif word_count_doctype2 == 0:
				return self.EXCLUSIVE_WORD_PROB

		# P(S|W) = P(W|S) / ( P(W|S) + P(W|H) )

		p_ws = word_count_doctype1 / self.doctype1_word_count
		p_wh = word_count_doctype2 / self.doctype2_word_count

		return p_ws / (p_ws + p_wh)

	def p_from_list(self, l):
		p_product         = reduce(lambda x,y: x*y, l)
		p_inverse_product = reduce(lambda x,y: x*y, map(lambda x: 1-x, l))

		return p_product / (p_product + p_inverse_product)


































