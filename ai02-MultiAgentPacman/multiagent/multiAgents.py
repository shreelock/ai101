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
        # print "\n\nCalculating best states for ", gameState.getPacmanPosition()
        # print "\n\nGhost present in ", gameState.getGhostPositions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        if len(bestIndices)>1:
            chosenIndex = self.tieBreakUsingGhostPos(bestIndices, legalMoves, gameState) # Pick randomly among the best
        else:
            chosenIndex = bestIndices[0]


        # print "Choosing action : ", legalMoves[chosenIndex]
        return legalMoves[chosenIndex]

    def tieBreakUsingGhostPos(self, tiedIndices, legalMoves, currentGameState):
        # print "\n\nTrying to break tie between :"
        minDistList = []

        # We are calculating distance from the nearest ghost for each tied
        # state and picking the max of those two.
        for index in tiedIndices:
            action = legalMoves[index]
            successorGameState = currentGameState.generatePacmanSuccessor(action)
            newPos = successorGameState.getPacmanPosition()
            newGhostPosList = successorGameState.getGhostPositions()
            # print "\nindex ", index
            # print "newPos ", newPos
            # print "ghostPositions ", newGhostPosList

            nearestGhostDist = min([manhattanDistance(ghostPos, newPos) for ghostPos in newGhostPosList])
            # print "nearestGhost is at : ", nearestGhostDist
            minDistList.append(nearestGhostDist)

        # now that we have gotten Nearest Ghost from each position, we want to go to the position
        # where the ghost is farthest.
        maxOfMinDistList = max(minDistList)

        # Indices which are at the same distance from the nearest ghost
        farthestMinIndices = [index for index in range(len(minDistList)) if minDistList[index] == maxOfMinDistList]

        # Now everything is same, what to do :-|. Ramdon
        chosenIndexFromDistList = random.choice(farthestMinIndices)
        # print "chosenIndex, Action : ", tiedIndices[chosenIndexFromDistList], action

        #The above indices were for the smaller list we processed. Transfer that index to our actual index.
        chosenFromTiedList = tiedIndices[chosenIndexFromDistList]

        return chosenFromTiedList

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
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentStateTempScore = 1000
        minDistFromFoods = 1000

        newFoodPosList = currentGameState.getFood().asList()
        newGhostPosList = successorGameState.getGhostPositions()

        # print "\naction : ",action
        # print "newPos : ",newPos
        # print "newFoodList : ",newFoodPosList

        for foodItemPos in newFoodPosList:
            #TODO: use MazeDistance to resolve fukery
            dist = manhattanDistance(foodItemPos, newPos)
            if dist < minDistFromFoods:
                minDistFromFoods = dist

        # Since we are comparing states based on "Highest" score returned from this function,
        # I am returning "1000 -  distance" to give the highest score to the
        # state which is nearest to any of the available food item
        currentStateTempScore -= minDistFromFoods*5

        # We are Including Ghost distance in the equation to avoid oscillation betwwen foods
        # We use this feature again to break the tie. We keep the one which is farthest from
        # nearest ghost.
        nearestGhostDist = min([manhattanDistance(ghostPos, newPos) for ghostPos in newGhostPosList])
        currentStateTempScore += nearestGhostDist

        # To discourage pacman from stopping
        if newPos == currentGameState.getPacmanPosition():
            currentStateTempScore = 0
        # To not let the pacman go to a place where ghost is.
        for ghosPos in newGhostPosList:
            if manhattanDistance(ghosPos, newPos) <= 1.0:
                currentStateTempScore = float("-inf")

        # print "Got score as 1000", -minDistFromFoods*1.1, "+", nearestGhostDist, "=", currentStateTempScore
        return currentStateTempScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

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
        GLOBAL_MAX_VALUE = 999999
        GLOBAL_MIN_VALUE = -999999
        def getMiniMaxScore(state, agentIndex, depth):

            max_depth = self.depth
            # Process the depth and agent information in the beginning.
            if agentIndex >= state.getNumAgents():
                agentIndex = 0
                # We have crossed all the agents
                depth = depth + 1

            if depth == max_depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                max_output = ["startState", GLOBAL_MIN_VALUE]

                legal_actions_for_pacman = state.getLegalActions(agentIndex)
                if not legal_actions_for_pacman:
                    # no actions left for pacman
                    return self.evaluationFunction(state)

                for pacman_action in legal_actions_for_pacman:
                    next_state = state.generateSuccessor(agentIndex, pacman_action)

                    sc = getMiniMaxScore(next_state, agentIndex + 1, depth)
                    if type(sc) is list:
                        # We are not at leaf nodes
                        max_score = sc[1]
                    else:
                        # reached leaf node
                        max_score = sc

                    if max_score > max_output[1]:
                        max_output = [pacman_action, max_score]

                return max_output

            else:
                min_output = ["startState", GLOBAL_MAX_VALUE]

                legal_actions_for_ghost = state.getLegalActions(agentIndex)
                if not legal_actions_for_ghost:
                    # no actions left for ghost
                    return self.evaluationFunction(state)

                for ghost_action in legal_actions_for_ghost:
                    next_state = state.generateSuccessor(agentIndex, ghost_action)
                    sc = getMiniMaxScore(next_state, agentIndex + 1, depth)

                    if type(sc) is list:
                        # we are at non leaf nodes, so returning action alongwith score to compare
                        min_score = sc[1]
                    else:
                        # reached leaf node, no action t return, only score
                        min_score = sc

                    if min_score < min_output[1]:
                        min_output = [ghost_action, min_score]

                return min_output

        # returning only action to be taken, not score
        minMaxResult = getMiniMaxScore(gameState, 0,0)
        chosenAction = minMaxResult[0]

        return chosenAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        GLOBAL_MAX_VALUE = 999999
        GLOBAL_MIN_VALUE = -999999
        alphaValue = GLOBAL_MIN_VALUE #Initially Alpha
        betaValues = [] #Initial Beta Values
        for temp in range(1, gameState.getNumAgents()):
            betaValues.append(GLOBAL_MAX_VALUE)

        tempValForComparingAlpha = GLOBAL_MIN_VALUE
        nextaction = None

        def alphaBetaPrune(state, depth, alphaValue, betaValues):
            # Here, we are considering one depth level = one step by one agent, so
            # actual depth(according to convention) is depth/numAgents
            if state.isWin() or state.isLose() or depth == self.depth * state.getNumAgents():
                return self.evaluationFunction(state)

            agentIndex = depth % state.getNumAgents()
            if agentIndex == 0:
                betaValues = betaValues[:] #python things
                value = GLOBAL_MIN_VALUE
                for children in state.getLegalActions(agentIndex):
                    childState = state.generateSuccessor(agentIndex, children)
                    value = max(value, alphaBetaPrune(childState, depth + 1, alphaValue, betaValues))
                    if value > min(betaValues):
                        # we dont see later childrens
                        return value
                    alphaValue = max(value, alphaValue)
                return value
            else:
                betaValues = betaValues[:]
                value = GLOBAL_MAX_VALUE
                for children in state.getLegalActions(agentIndex):
                    childState = state.generateSuccessor(agentIndex, children)
                    value = min(value, alphaBetaPrune(childState, depth + 1, alphaValue, betaValues))
                    if value < alphaValue:
                        # we dont see later childrens
                        return value
                    betaValues[agentIndex-1] = min(value, betaValues[agentIndex-1])
                return value

        for action in gameState.getLegalActions(0):
            res = alphaBetaPrune(gameState.generateSuccessor(0, action), 1, alphaValue, betaValues)
            if res > tempValForComparingAlpha:
                tempValForComparingAlpha = res
                nextaction = action
            alphaValue = max(alphaValue, tempValForComparingAlpha)
        return nextaction

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
        GLOBAL_MIN_VALUE = -999999
        def getMiniMaxScore(state, agentIndex, depth):

            max_depth = self.depth
            # Process the depth and agent information in the beginning.
            if agentIndex >= state.getNumAgents():
                agentIndex = 0
                # We have crossed all the agents
                depth = depth + 1

            if depth == max_depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                max_output = ["startState", GLOBAL_MIN_VALUE]

                legal_actions_for_pacman = state.getLegalActions(agentIndex)
                if not legal_actions_for_pacman:
                    # no actions left for pacman
                    return self.evaluationFunction(state)

                for pacman_action in legal_actions_for_pacman:
                    next_state = state.generateSuccessor(agentIndex, pacman_action)

                    sc = getMiniMaxScore(next_state, agentIndex + 1, depth)
                    if type(sc) is list:
                        # We are not at leaf nodes
                        max_score = sc[1]
                    else:
                        # reached leaf node
                        max_score = sc

                    if max_score > max_output[1]:
                        max_output = [pacman_action, max_score]

                return max_output

            else:
                total_actions = 0
                total_score = 0

                legal_actions_for_ghost = state.getLegalActions(agentIndex)
                if not legal_actions_for_ghost:
                    # no actions left for ghost
                    return self.evaluationFunction(state)

                for ghost_action in legal_actions_for_ghost:
                    total_actions+=1
                    next_state = state.generateSuccessor(agentIndex, ghost_action)
                    sc = getMiniMaxScore(next_state, agentIndex + 1, depth)

                    if type(sc) is list:
                        # we are at non leaf nodes, so returning action alongwith score to compare
                        score = sc[1]
                    else:
                        # reached leaf node, no action t return, only score
                        score = sc

                    total_score = total_score + score
                # We are assuming ghosts uniformly, randomly selects its state
                random_action = random.sample(legal_actions_for_ghost, 1)
                # However, the expected score from the parent action of pacman
                # is calculated by averaging over scores of all the actions, since
                # our ghost agents are uniformly random.
                expected_score = float(total_score)/float(total_actions)
                # As compared to earlier, this time, we are not maintaining the
                # minimum score for returning the action.
                expectimax_output = [random_action, expected_score]

                return expectimax_output

        # returning only action to be taken, not score
        minMaxResult = getMiniMaxScore(gameState, 0,0)
        chosenAction = minMaxResult[0]

        return chosenAction

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

