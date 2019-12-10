import Hanabi

# Initialise the game with five named players.
hanabi = Hanabi.Game(["Alice","Bob","Coco","Dora","Eli"])

# Everything that happens inside this loop will occur on each turn. 
# Just running it once for now though.
for turn in range(1):

	# Print a summary of the game in its current state.
	print(hanabi,'\n')

	# Get the name of the player whose turn it is.
	p = hanabi.whos_turn
	print(p+"'s turn.")

	# Show what p is allowed to observe of the game state.
	print("Game state observation:\n",hanabi.observe(p))
	valid_info = hanabi.validInfo(p)
	print("Valid info options:\n",valid_info)

	# Choose an action, specified by an action type and args.

	action_type = "play"	# Action type: play card.
	args = 0				# Args: integer specifying which card in the hand to play.
		
	'''
	action_type = "discard"	# Action type: discard card.
	args = 0 				# Args: integer specifying which card in the hand to discard.

	action_type = "info"	# Action type: give info to another player.
	args = valid_info[0]	# Args: an element from the valid_info vector.

	'''

	# Execute the desired action.
	print("Chosen action:\n",action_type,"-->",args)
	outcome = hanabi.act(p, action_type, args)
	print("\n==========================\n")

	# If the game has come to an end, display the final score.
	if outcome == -1: print("Final score =",hanabi.score); break