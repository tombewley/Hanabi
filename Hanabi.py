import random	

class Game:

	def __init__(	self,
					players,								# If this is a positive integer, create this many players with names 0, 1, 2... . If it is a list, create players with the list elements as names.
					suits = 	['r','y','b','g','w'],		# List of suits.
					counts =	[3,2,2,2,1],				# List of counts, with element 0 corresponding to number 1 etc. Extend this list to allow higher card values.
					clocks = 	8,							# Clocks moderate players' ability to give information.
					fuse = 		4,							# Fuse tracks wrongly-played cards.
				):

		# Create and shuffle the deck.
		self.cards = []
		for s in suits: 
			for n, c in enumerate(counts): self.cards += [(s,n+1)] * c
		self.deck = list(self.cards)
		random.shuffle(self.deck)
		
		# Create players.
		if type(players) == int and players > 1 and players < 6: self.players = list(range(players))
		elif type(players) == list: self.players = players 
		else: raise ValueError('Error in player spec.')

		# Create other card-holding data structures: a hand for each player, a firework for each suit, the discard pile and the table.
		self.hands = {p:[] for p in self.players}
		self.fireworks = {s:[] for s in suits}
		self.discard_pile = []
		self.table = [] 	# Should only ever contain 0 or 1 cards at a time.

		# Initialise clocks and fuse.
		self.clocks = clocks; self.max_clocks = clocks; self.fuse = fuse

		# Initialise events log, time indexer, score and counter which starts when deck is empty.
		self.events = []; self.t = 0; self.score = 0; self.empty_deck_counter = 0

		# Compute maximum score.
		self.max_score = len(suits) * len(counts)

		# Decide who's turn it is. Turns cycle according to the order of the player list.
		self.whos_turn = self.players[self.t % len(self.players)] 

		# Deal the cards.
		if len(self.players) > 3: 	self.hand_size = 4
		else: 						self.hand_size = 5
		self.deal(self.hand_size)


	# Define string behaviour.
	def __repr__(self):
		intro = 'Hanabi game state @ t = ' + str(self.t) + ', clocks = ' + str(self.clocks) + ', fuse = ' + str(self.fuse) + ', score = ' + str(self.score)
		fireworks = 'Fireworks:\n' + str(self.fireworks)
		hands = 'Hands:\n' + str(self.hands)
		deck = 'Deck:\n' + str(self.deck)
		discard = 'Discard:\n' + str(self.discard_pile)
		table = 'Table:\n' + str(self.table)
		events= 'Events:\n' + str(self.events)
		return '\n'.join([intro, fireworks, hands, deck, discard, table, events])


	# ---------------------------------------------------
	# ELEMENTARY EVENTS

	# Return a data structure with everything that p is permitted to see.
	def observe(self, p):
		return {	't':			self.t,
					'fireworks': 	self.fireworks,
					'hands': 		{pp:h for pp,h in self.hands.items() if pp != p},
					'discard_pile': self.discard_pile,
					'score': 		self.score,
					'clocks':		self.clocks,
					'fuse': 		self.fuse,
					'events': 		self.events,
					'play_order':	self.players[(self.t % len(self.players))+1:] + self.players[:self.t % len(self.players)],
				}


	# Deal cards from the deck to the players' hands.
	def deal(self, hand_size):
		for c in range(hand_size):
			for p in self.players:
				self.hands[p].append(self.deck.pop())


	# Discard the nth card in p's hand to the discard pile.
	def discard(self, p, n):
		card = self.hands[p].pop(n)
		self.discard_pile.append(card)
		self.clocks = min(self.max_clocks, self.clocks + 1)
		self.events.append((self.t, 'discard', p, n, card))
		

	# Play the nth card in p's hand to the table.
	def play(self, p, n):
		card = self.hands[p].pop(n)
		self.table.append(card)
		self.events.append((self.t, 'play', p, n, card))


	# Evaluate whether the card on the table can be added to a firework.
	# If so, add it. If not, discard it and decrement the fuse counter.
	def playEval(self):
		card = self.table.pop()
		# Success.
		if ( len(self.fireworks[card[0]]) == 0 and card[1] == 1 ) or ( len(self.fireworks[card[0]]) > 0 and card[1] == self.fireworks[card[0]][-1][1] + 1 ):
			self.fireworks[card[0]].append(card)
			self.events.append((self.t, 'playSucc', card)) 
			self.score += 1
		# Failure.
		else: 
			self.discard_pile.append(card)
			self.fuse -= 1
			self.events.append((self.t, 'playFail', self.fuse)) 


	# Top up a player's hand with a card from the deck. *** Note that this appends to their hand ***
	def topup(self, p):
		if len(self.hands[p]) < self.hand_size and len(self.deck) > 0: 
			self.hands[p].append(self.deck.pop())
			self.events.append((self.t, 'topup', p))


	# List all of the pieces of information that p is allowed to communicate. 
	def validInfo(self, p):
		info = []
		for pp in self.players:
			if pp != p:
				suits = set([c[0] for c in self.hands[pp]])
				suit_info = [(pp, 'suit', s, [1 if c[0] == s else 0 for c in self.hands[pp]]) for s in suits]
				info += suit_info
				numbers = set([c[1] for c in self.hands[pp]])
				number_info = [(pp, 'num', n, [1 if c[1] == n else 0 for c in self.hands[pp]]) for n in numbers]
				info += number_info
		return info


	# Give a piece of valid information.
	def giveInfo(self, p, info):
		self.events.append((self.t, 'info', p, info))
		self.clocks = max(0, self.clocks - 1)


	# ---------------------------------------------------
	# GAME PROTOCOL

	def act(self, p, action_type, args):

		# Check if it is p's turn.
		if self.whos_turn != p: print('Not '+str(p)+'\'s turn!'); return 0
		else:

			# Action type 1: giving a piece of information.
			if action_type == 'info':
				# Check that this info is valid.
				if args not in self.validInfo(p): print('Invalid info!'); return 0
				# Check that there are enough clocks remaining.
				if self.clocks < 1: print('Not enough clocks!'); return 0
				self.giveInfo(p, args)

			# Action type 2: discarding a card.
			elif action_type == 'discard': 
				# Check that args is a valid card number.
				if type(args) == int and args >= 0 and args < len(self.hands[p]):
					self.discard(p, args)
					self.topup(p)
				else: print('Invalid card number!'); return 0 

			# Action type 3: playing a card.
			elif action_type == 'play':
				# Check that args is a valid card number.
				if type(args) == int and args >= 0 and args < len(self.hands[p]):
					self.play(p, args)
					self.playEval()
					self.topup(p)
				else: print('Invalid card number!'); return 0 

			else: print('Invalid action type!'); return 0

		# Game end 1: run out of fuses.
		if self.fuse == 0: print('\nt =',self.t,': GAME OVER, OUT OF FUSES'); return -1
		# Game end 2: maximum score reached.
		elif self.score == self.max_score: print('\nt =',self.t,': GAME OVER, MAX SCORE REACHED'); return -1
		# Game end 3: deck is empty and one full round complete after.
		elif self.deck == []:
			print('EMPTY DECK')
			if self.empty_deck_counter == len(self.players): print('\nt =',self.t,': GAME OVER, DECK EMPTY'); return -1
			self.empty_deck_counter += 1

		return 1


	def step(self):
		self.t += 1
		self.whos_turn = self.players[self.t % len(self.players)]