from __future__ import division
import random

class Card(object):
	"""
		card object
	"""
	Suit_Names = ['Clubs', 'Diamonds', 'Hearts','Spades']
	Rank_Names = [ None, 'Ace',2,3,4,5,6,7,8,9,10,'Jack','Queen','King']
	
	def __init__(self, suit =0, rank = 2):
		self.suit = suit
		self.rank = rank
	
	def __str__(self):
		return "%s of %s" %(Card.Rank_Names[self.rank],
		                    Card.Suit_Names[self.suit] )
		                    
	def __cmp__(self, other):
		t1 = self.suit, self.rank
		t2 = other.suit, other.rank
		return cmp(t1,t2)
		
		
class Deck(object):
	"""
		Deck contain 52 Cards
	"""
	def __init__(self):
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit, rank)
				self.cards.append(card)
	
	def __str__(self):
		res = []
		for card in self.cards:
			res.append(str(card))
		
		return '\n'.join(res)
		
	def pop_card(self):
		return self.cards.pop()
	
	def add_card(seld, card):
		self.cards.append(card)
	
	def shuffle(self):
		"""
			Shuffle a Deck of cards
		"""
		random.shuffle(self.cards)
		
	def sort_deck(self):
		self.cards.sort()
	
	def move_cards(self, hand, num):
		"""
			Move one card from one hand
		"""
		for i in range(num):
			hand.cards.append(self.pop_card())
	

	def deal_hands(self, nhands, ncards):
		"""
			deal_hands shuffle a deck and distribute 
			each hands
			nhands - number of hands
			ncards - number of cards per hand
		"""
		handls = []
		random.shuffle(self.cards)
		for i in range(nhands):
			hand = PokerHand(str(i + 1))
			self.move_cards(hand, ncards)
			hand.init_histo()
			handls.append(hand)
		return handls
	
class Hand(Deck):
	"""
		Hand used for each player
	"""
	def __init__(self, label=""):
		self.cards =[]
		self.label = label
		
	def __str__(self):
		res = []
		for card in self.cards:
			res.append(str(card))
		return '\n'.join(res)
	def clear(self):
		self.cards = []
	


class PokerHand(Hand):	
	
	def __init__(self, name=""):
		Hand.__init__(self,name)
		self.dSuits = {}
		self.dRanks = {}
		#Suit_Names = ['Clubs', 'Diamonds', 'Hearts','Spades']
		self.Clubs = []
		self.Diamonds = []
		self.Hearts = []
		self.Spades = []
		self.CardDict = {}
		
		
		
	def init_histo(self):
		for card in self.cards:
			self.dSuits[card.suit] = self.dSuits.get(card.suit,0) +  1
			self.dRanks[card.rank] = self.dRanks.get(card.rank,0) + 1
			
			if card.suit == 0:
				self.Clubs.append(card.rank)
			elif card.suit == 1:
				self.Diamonds.append(card.rank)
			elif card.suit == 2:
				self.Hearts.append(card.rank)
			else:
				self.Spades.append(card.rank)
		
		self.CardDict[0] = self.Clubs
		self.CardDict[1] = self.Diamonds
		self.CardDict[2] = self.Hearts
		self.CardDict[3] = self.Spades
			
	def has_n_pair(self, n):
		"""
			n- indicates number of pairs
			One pair - two cards with same rank
		"""
		countpair = 0
		#for k, v in self.dRanks.items():
		#	print "Rank %r = %r"%(k, v)
		
		for count in self.dRanks.values():
			if count >= 2:
				countpair += 1
			if countpair >= n:	
				return True
		return False
	
	def has_three_of_a_kind(self):
		"""
			3 cards with same rank
		"""
		for count in self.dRanks.values():
			if count >= 3:
				return True
		return False;
	
	def get_int_value_of_a_rank(self, rank):
		if rank == 'Ace':
			return 1
		elif rank == "Jack":
			return 11
		elif rank == "Queen":
			return 12
		elif rank == "King":
			return 13
		else:
			return rank
			

	def has_straight(self):
		"""
			5 Cards with ranks in sequence
			Ace can be high or low
		"""
		return self.has_straight_check(self.dRanks.keys())
		
	
	def has_straight_check(self, ranks):
		"""
			 5 cards with ranks in sequence
			 Ace can be high or low
		"""
	 	rankls = []
	 	has_ace = False
	 	has_more_ace = False
	 	if 'Ace' in ranks:
	 		has_ace = True
		for rank in ranks:
			rankls.append(self.get_int_value_of_a_rank(rank))
		
		rankls.sort()
		#for i in rankls:
		#	print i,
		#print ""
		count = 1
		prev_rank = rankls[0]
		for i in range(1,len(rankls)):
			#print "prevR = %r  Rank = %r" %(prev_rank, rankls[i])
			if rankls[i] == 1:
				has_more_ace = True
			if prev_rank + 1 == rankls[i]:
				count += 1
			else:
				count =  1
			prev_rank = rankls[i]
	
		if count >= 5:
			#print "5 in a row"
			return True
		if count == 4 and has_ace:
			#print "4 in a row and Ace"
			return True
		if count == 3 and has_more_ace:
			#print "3 in a row and two ace"
			return True
		
		return False
			
	
	def has_flush(self):
		"""
			five cards with same suit
		"""
		for i in self.dSuits.values():
			if i >= 5:
				return True
		return False
	
	def has_full_house(self):
		"""
			1st condition = 3 cards with same rank, 
			2nd condition = 2 cards with another rank
		"""
		firstcon = False
		secondcon = False
		for count in self.dRanks.values():
			if count >= 3 and firstcon == False:
				firstcon = True
			elif count >= 2:
				secondcon = True
				
		return firstcon and secondcon
	
	def has_four_of_a_kind(self):
		"""
			four cards with the same suit
		"""
		for count in self.dRanks.values():
			if count >= 4:
				return True
		return False
	
	def has_straight_flush(self):
		"""
			Five cards with ranks in sequence and same suit
		"""
		#print " call to straight flush" 
		for suit, count in self.dSuits.items():
			#print suit, count
			if count >=5:
				return self.has_straight_check(self.CardDict[suit])
				
		return False 
	
	def classify(self):
		if self.has_straight_flush() == True:
			return "SF"
		elif self.has_four_of_a_kind() == True:
			return "4K"
		elif self.has_full_house() == True:
			return "FH"
		elif self.has_flush() == True:
			return "F"
		elif self.has_straight() == True:
			return "S"
		elif self.has_three_of_a_kind() == True:
			return "3K"
		elif self.has_n_pair(2) == True:
			return "TP"
		elif self.has_n_pair(1) == True:
			return "P"
		else:
			return "SNL"
	
def write_header():
	fp= open("pokerdata.txt", 'a')
	header = "P\tTP\t3K\tS\tF\tFH\t4K\tSF\n"
	fp.write(header)
	fp.close()
	
def write_to_file(d):
	fp = open("pokerdata.txt", 'a')
	data = "%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % \
			(d.get('P',0), d.get('TP',0), \
			 d.get('3K',0), d.get('S',0), \
			 d.get('F',0), d.get('FH',0), 
			 d.get('4K',0), d.get('SF',0))
	fp.write(data)
	fp.close()
	
def calculate_proba(d, n):
	totalhands = n * 7
	print "========================"
	print "Probability of P  : %.5f" % (d.get('P',0)/totalhands)
	print "Probability of TP : %.5f" % (d.get('TP',0)/totalhands)
	print "Probability of 3K : %.5f" % (d.get('3K',0)/totalhands)
	print "Probability of S  : %.5f" % (d.get('S',0)/totalhands)
	print "Probability of F  : %.5f" % (d.get('F',0)/totalhands)
	print "Probability of FH : %.5f" % (d.get('FH',0)/totalhands)
	print "Probability of 4K : %.5f" % (d.get('4K',0)/totalhands)
	print "Probability of SF : %.5f" % (d.get('SF',0)/totalhands)
	
	
	
			
		
if __name__ == '__main__':
	count = 0
	
	out_shuffle = []
	n = 10000
	#write_header()
	for idx in range(1):
		fData = {}
		for i in range(n):
			deck = Deck()
			res = deck.deal_hands(7, 7)
			for h in res:
				s =  h.classify()
				if s == "P":
					fData["P"] = fData.get("P",0) + 1
				elif s == "TP":
					fData["TP"] = fData.get("TP",0) + 1
				elif s == "3K":
					fData["3K"] = fData.get("3K",0) + 1
				elif s == "S":
					fData["S"] = fData.get("S",0) + 1
				elif s == "F":
					fData["F"] = fData.get("F",0) + 1
				elif s == "FH":
					fData["FH"] = fData.get("FH",0) + 1
				elif s == "4K":
					fData["4K"] = fData.get("4K",0) + 1
				elif s == "SF":
					fData["SF"] = fData.get("SF",0) + 1
				else:
					fData["SNL"] = fData.get("SNL",0) + 1
		write_to_file(fData)
		calculate_proba(fData,n)
	
	

			
	


























