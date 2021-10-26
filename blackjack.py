import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True

# Card Class: has suit and rank. 
class Card:

	def __init__(self, rank, suit):
		self.suit = suit 	# the suit of the card (heart, diamond...)
		self.rank = rank  	# the rank of the card (2, 3, 4, king...)

	def __str__(self):
		return f"{self.rank} of {self.suit}" 		# returns the name of the card

# Deck Class: holds 52 cards in a double list that can be shuffled. 
# shuffle(): shuffles the cards 
# deal(): returns a card
class Deck:

	def __init__(self):	
		self.deck = [] 		# list of cards in the deck
		for suit in suits:
			for rank in ranks:
				self.deck.append([rank, suit])  		# appends [rank, suit] to deck

	def __str__(self):
		return f"{self.deck}"  		# returns the entire deck

	def shuffle(self):
		random.shuffle(self.deck)	# shuffles the entire deck

	def deal(self):
		for card in self.deck:		
			self.deck.pop(0)		# removes the first card from deck
			return card  			# returns the top card

# Hand Class: represents a player's hand
# add_card(card): takes card and appends to cards[]
# adjust_for_aces(): checks cards[] to see if there are any aces. if aces, checks total value of hand.
# if value of hand > 21, change ace = 1
class Hand:

	def __init__(self):
		self.cards = []		# list of cards in your hand
		self.value = 0 		# total value of the cards in your hand
		self.aces = 0 		# number of aces in your hand

	def add_card(self, card):
		self.cards.append(card)  		# adds a card to cards[] (which represents your hand)

		self.value += values[card[0]]  		# totals the value of the cards in your hand

		if card[0] == 'Ace':  			# checks for aces in your hand (cards[])
			self.aces += 1	

	def adjust_for_aces(self):	
		if self.aces >= 1 and self.value > 21:
			self.value -= 10
			self.aces -= 1		

	def show_all(self): 
		return self.cards 				# prints all cards in hand

	def show_some(self):
		dealercards = []
		for i in range((len(self.cards)) - 1):
			dealercards.append(self.cards[i+1])
			return dealercards

# Chips Class: represents chips and bets
# win_bet(): if a player wins a bet, add bet amount to total
# lose_bet(): if a player loses a bet, subtract bet from total
class Chips:

	def __init__(self):
		self.total = 100  		# start player with 100 chips
		self.bet = 0  			# player's bet

	def amount(self):
		return self.total

	def win_bet(self):
		self.total += self.bet  	# if player wins, add bet amount to total

	def lose_bet(self):
		self.total -= self.bet  	# if player loses, subtract bet from total

# Functions:
# Taking bets: player enters a bet. check to see if bet is valid
def take_bet():
	while True:
		try:
			print(f"Chip amount: {mychips.amount()}")
			bet = int(input("Enter your bet amount: "))  		# Get user input for bet amount
		except:
			print("\nTypeError: Please enter a number...")  		# except: user doesn't enter a number
		else:
			if mychips.amount()-bet >= 0:  						# bet recieved
				print(f"\nYou bet {bet}")
				mychips.bet = bet
				break
			else:
				print("\nError: Not enough chips...")  			# bet is too much, ask again
				continue

# Hit: draw a new card. check to see if bust. takes deck and hand
# Dealer hits while hand is less than 17
def hit(deck, hand):
	hand.add_card(deck.deal())
	hand.adjust_for_aces()
	return hand

# Hit or Stand: takes user input and hits or stands. takes deck and hand
def hit_or_stand(deck, hand):
	global playing

	while True:
		try:
			hitOrStand = str(input("Do you want to hit (h) or stand (s)?: ")).lower()  		# asks for user input
		except:
			print("\nTypeError: Please enter 'h' for hit or 's' for stand...")
		else:
			if hitOrStand != "h" and hitOrStand != "s":
				print("\nError: Please enter 'h' for hit or 's' for stand...")  			# if not a h or s, ask again
				continue
			else:
				if hitOrStand == 'h':				# if h, hit()
					hand = hit(deck, hand)
				else:								# if s, stand... playing = False
					playing = False
				break

# Player Busts:
def player_busts():
	mychips.lose_bet()
	print("\nBUST!")

# Player Wins:
def player_wins():
	mychips.win_bet()
	print(f"You win! Dealer total: {dealerhand.value}")

# Dealer Busts:
def dealer_busts():
	mychips.win_bet()
	print("You win! Dealer busts.")

# Dealer Wins:
def dealer_wins():
	mychips.lose_bet()
	print(f"You lose! Dealer total: {dealerhand.value}")

# Push: Tie
def push():
	print("Push")


mychips = Chips()
while True:
	print("Welcome! Let's play some blackjack\n")

	mydeck = Deck()
	mydeck.shuffle()

	take_bet()

	playerhand = Hand()
	dealerhand = Hand()

	playerhand.add_card(mydeck.deal())
	playerhand.add_card(mydeck.deal())

	dealerhand.add_card(mydeck.deal())
	dealerhand.add_card(mydeck.deal())	

	while playing:
		print(f"\nYour cards: {playerhand.show_all()} Total: {playerhand.value}")
		print(f"Dealer's cards: <-First Card is Hidden-> {dealerhand.show_some()}")
		playerhand.adjust_for_aces()
		hit_or_stand(mydeck, playerhand)		

		if playerhand.value > 21:
			print(f"\nYour cards: {playerhand.show_all()} Total: {playerhand.value}")
			print(f"Dealer's cards: {dealerhand.show_all()} Total: {dealerhand.value}")
			player_busts()
			break

	if playerhand.value <= 21:
		while dealerhand.value < 17:
			dealerhand.adjust_for_aces()
			hit(mydeck, dealerhand)

		print(f"\nYour cards: {playerhand.show_all()} Total: {playerhand.value}")
		print(f"Dealer's cards: {dealerhand.show_all()} Total: {dealerhand.value}")

		if dealerhand.value > 21:
			dealer_busts()

		elif playerhand.value > dealerhand.value:
			player_wins()

		elif dealerhand.value > playerhand.value:
			dealer_wins()

		else:
			push()

	print(f"\nYour chip amount: {mychips.amount()}")

	new_game = input("\nWould you like to play another hand? Enter 'y' or 'n' ")
	if new_game[0].lower() == 'y':
		playing = True
		continue
	else:
		print("Thanks for playing!")
		break






		