# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]
		
	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		curFood = currentGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
		if action == 'Stop':
			return -1
		score = 0
		# score will be made up with:
		# 1. System score >> score += successorGameState.getScore()
		# 2. Super Food at new pos >> score += scared time of all ghosts
		# 3. Closest Food and closest ghost >>
		#	dist(Food) > dist(Ghost) >> score += dist(Ghost)/dist(Food)^2 * 0.7
		#	dist(Food) <= dist(Ghost) >> score += dist(Ghost)/dist(Food)^2 * 1.1
		# 4. Food at new pos >> score * 1.2

		# 1
		score += successorGameState.getScore()
		
		# 2
		for scaredTime in newScaredTimes:
			score += scaredTime
		
		# 3
		foodList = newFood.asList()
		ghostDist = []
		foodDist = []
		for ghost in newGhostStates:
			ghostDist.append(manhattanDistance(ghost.getPosition(), newPos))
		for pos in foodList:
			foodDist.append(manhattanDistance(pos, newPos))
		if len(foodDist):
			if min(foodDist) > min(ghostDist):
				score += (min(ghostDist) * (1.0/min(foodDist))**2) * 0.8
			else:
				score += (min(ghostDist) * (1.0/min(foodDist))**2) * 1.1

		# 4
		curFoodList = curFood.asList()
		if newPos in curFoodList:
			score = score * 1.1

		return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

# def scoreEvaluationFunction(currentGameState):
# 	"""
# 		This default evaluation function just returns the score of the state.
# 	  The score is the same one displayed in the Pacman GUI.

# 	  This evaluation function is meant for use with adversarial search agents
# 	  (not reflex agents).
# 	"""
# 	# Useful information you can extract from a GameState (pacman.py)
# 	curPos = currentGameState.getPacmanPosition()
# 	curFood = currentGameState.getFood()
# 	curGhostStates = currentGameState.getGhostStates()
# 	curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]

# 	score = 0
# 	# score will be made up with:
# 	# 1. System score >> score += currentGameState.getScore()
# 	# 2. Super Food >> score += scared time of all ghosts
# 	# 3. Closest Food and closest (not scared) ghost >>
# 	#	dist(Food) > dist(Ghost) >> score += dist(Ghost)/dist(Food)^2 * 0.8
# 	#	dist(Food) <= dist(Ghost) >> score += dist(Ghost)/dist(Food)^2 * 1.1
# 	# 4. Closest Food and closest (not scared) ghost >>
# 	# 	score += (max(ghostDist) * (1.0/min(ghostDist)) * (1.0/min(foodDist))) * 1.5

# 	# 1
# 	score += currentGameState.getScore()
	
# 	# 2
# 	scared_flag = True
# 	for scaredTime in curScaredTimes:
# 		if not scaredTime:
# 			scared_flag = False
# 			break
# 		else:
# 			score += scaredTime
	
# 	# 3
# 	foodList = curFood.asList()
# 	ghostDist = []
# 	foodDist = []
# 	for ghost in curGhostStates:
# 		ghostDist.append(manhattanDistance(ghost.getPosition(), curPos))
# 	for pos in foodList:
# 		foodDist.append(manhattanDistance(pos, curPos))
# 	if not scared_flag and len(foodDist):
# 		if min(foodDist) > min(ghostDist):
# 			score += (min(ghostDist) * (1.0/min(foodDist))**2) * 0.8
# 		else:
# 			score += (min(ghostDist) * (1.0/min(foodDist))**2) * 1.1
# 	elif scared_flag and len(foodDist):
# 		score += (max(ghostDist) * (1.0/min(ghostDist)) * (1.0/min(foodDist))) * 1.5

# 	return score


class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
		Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
			Returns the minimax action from the current gameState using self.depth
			and self.evaluationFunction.

			Here are some method calls that might be useful when implementing minimax.

			gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

			gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

			gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		# max ply (pacman ply)
		def max_ply(state, depth):
			if state.isWin() or state.isLose() or depth == self.depth:
				return self.evaluationFunction(state), None

			score = float('-Inf')
			max_action = ''
			for action in state.getLegalActions(0):
				tmp_score = min_ply(state.generateSuccessor(0, action), depth, 1)[0]
				if score < tmp_score:
					score = tmp_score
					max_action = action
			return score, max_action
		
		# min ply (ghosts ply)
		def min_ply(state, depth, ghostNum):
			if state.isWin() or state.isLose():
				return self.evaluationFunction(state), None

			score = float('Inf')
			min_action = ''
			# Last ghost, go to next max ply
			if ghostNum == gameState.getNumAgents() - 1:
				for action in state.getLegalActions(ghostNum):
					tmp_score = max_ply(state.generateSuccessor(ghostNum, action), depth + 1)[0]
					if score > tmp_score:
						score = tmp_score
						min_action = action
			else:
				for action in state.getLegalActions(ghostNum):
					tmp_score = min_ply(state.generateSuccessor(ghostNum, action), depth, ghostNum + 1)[0]
					if score > tmp_score:
						score = tmp_score
						min_action = action
			return score, min_action

		maxiscore, bestAction = max_ply(gameState, 0)
		return bestAction
		util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
		Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
			Returns the minimax action using self.depth and self.evaluationFunction
		"""
		# max ply (pacman ply)
		def max_ply(state, depth, alpha, beta):
			if state.isWin() or state.isLose() or depth == self.depth:
				return self.evaluationFunction(state), None

			score = float('-Inf')
			max_action = ''
			for action in state.getLegalActions(0):
				tmp_score = min_ply(state.generateSuccessor(0, action), depth, 1, alpha, beta)[0]
				if score < tmp_score:
					score = tmp_score
					max_action = action
				if score > beta:
					return score, max_action
				alpha = max(alpha, score)
			return score, max_action
		
		# min ply (ghosts ply)
		def min_ply(state, depth, ghostNum, alpha, beta):
			if state.isWin() or state.isLose():
				return self.evaluationFunction(state), None

			score = float('Inf')
			min_action = ''
			# Last ghost, go to next max ply
			if ghostNum == gameState.getNumAgents() - 1:
				for action in state.getLegalActions(ghostNum):
					tmp_score = max_ply(state.generateSuccessor(ghostNum, action), depth + 1, alpha, beta)[0]
					if score > tmp_score:
						score = tmp_score
						min_action = action
					if score < alpha:
						return score, min_action
					beta = min(beta, score)
			else:
				for action in state.getLegalActions(ghostNum):
					tmp_score = min_ply(state.generateSuccessor(ghostNum, action), depth, ghostNum + 1, alpha, beta)[0]
					if score > tmp_score:
						score = tmp_score
						min_action = action
					if score < alpha:
						return score, min_action
					beta = min(beta, score)
			return score, min_action

		maxiscore, bestAction = max_ply(gameState, 0, float('-Inf'), float('Inf'))
		return bestAction
		util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

