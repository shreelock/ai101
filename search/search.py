# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    We should be able to run the following after this implementation

    python pacman.py -l tinyMaze -p SearchAgent
    python pacman.py -l mediumMaze -p SearchAgent
    python pacman.py -l bigMaze -z .5 -p SearchAgent
    """
    print "Start:", problem.getStartState()

    #Since we want to implement Depth First Search, we are using stack as our fringe list
    fringeList = util.Stack()
    alreadyExpandedItemsList = []

    currentState = problem.getStartState()
    # This variable contains the path followed from the start state to reach to current state.
    # Its the same as the valeues to be put in FringeList
    currentStatePath = [(currentState, 'Start', 0,)]
    foundGoal = False

    while True:
        if not problem.isGoalState(currentState):
            # print "\n\nalreadyExpandedItemsList : ", alreadyExpandedItemsList
            if currentState not in alreadyExpandedItemsList:

                successorsRichData =  problem.getSuccessors(currentState)
                # print "successors : ", successorsRichData

                for successor in successorsRichData :
                    tempStatePath = list(currentStatePath)
                    tempStatePath.insert(0, successor)
                    fringeList.push(tempStatePath)

                alreadyExpandedItemsList.append(currentState)

            else:
                # print "already expanded : ", currentState
                pass
            currentStatePath = fringeList.pop()
            # print "Popped Item from the stack : ", currentStatePath, len(currentStatePath)
            # Since current State Path - variable contains all the redundant information,
            # we are extracting only the coordinates that will be used ib multiple functions.

            currentState = currentStatePath[0][0]
            # print "Got currentState as : ", currentState

        else:
            # print "found goal state : ", currentStatePath
            foundGoal = True

        if foundGoal:
            break

    dirPath = []
    for state in currentStatePath:
        step = state[1]
        if step is not 'Start':
            dirPath.append(step)
    # Since we are traversing in Latest to Oldest manner, we need to reverse the list to get directions from
    # Oldest Node to Latest node.
    dirPath.reverse()

    # print "found direction path as : ", list(dirPath)
    return list(dirPath)

def breadthFirstSearch(problem):
    """
    *** Search the shallowest nodes in the search tree first ***
    """

    print "Start:", problem.getStartState()

    # Since we want to implement Breadth First Search, we are using queue as our fringe list
    fringeList = util.Queue()
    alreadyExpandedItemsList = []

    currentState = problem.getStartState()
    currentStatePath = [(currentState, 'Start', 0,)]
    foundGoal = False

    while True:
        if not problem.isGoalState(currentState):
            # print "\n\nalreadyExpandedItemsList : ", alreadyExpandedItemsList
            if currentState not in alreadyExpandedItemsList:

                successorsRichData = problem.getSuccessors(currentState)
                # print "successors : ", successorsRichData

                for successor in successorsRichData:
                    tempStatePath = list(currentStatePath)
                    tempStatePath.insert(0, successor)
                    fringeList.push(tempStatePath)

                alreadyExpandedItemsList.append(currentState)

            else:
                # print "already expanded : ", currentState
                pass
            currentStatePath = fringeList.pop()
            # print "Popped Item from the stack : ", currentStatePath, len(currentStatePath)
            currentState = currentStatePath[0][0]
            # print "Got currentState as : ", currentState
        else:
            # print "found goal state : ", currentStatePath
            foundGoal = True

        if foundGoal:
            break
    '''
    The explanation is provided in the function above : implementation of DFS.
    '''
    dirPath = []
    for state in currentStatePath:
        step = state[1]
        if step is not 'Start':
            dirPath.append(step)
    dirPath.reverse()

    return list(dirPath)

def uniformCostSearch(problem):
    """
        *** Search the node of least total cost first **

    """

    print "Start:", problem.getStartState()

    # Since we want to implement Uniform Cost Search, we are using Priority Queue as our fringe list
    fringeList = util.PriorityQueue()
    alreadyExpandedItemsList = []

    currentState = problem.getStartState()
    currentStatePath = [(currentState, 'Start', 0,)]
    foundGoal = False

    while True:
        if not problem.isGoalState(currentState):
            # print "\n\nalreadyExpandedItemsList : ", alreadyExpandedItemsList
            if currentState not in alreadyExpandedItemsList:

                successorsRichData = problem.getSuccessors(currentState)
                # print "successors : ", successorsRichData

                for successor in successorsRichData:
                    tempStatePath = list(currentStatePath)
                    tempStatePath.insert(0, successor)
                    # The - "getCurrentStatePathCost" function calculates the total cost of the path till now,
                    # , after inserting the current state into the current state path
                    currentStatePathCost = getCurrentStatePathCost(tempStatePath)
                    fringeList.push(tempStatePath, currentStatePathCost)

                alreadyExpandedItemsList.append(currentState)
            else:
                # print "already expanded : ", currentState
                pass
            currentStatePath = fringeList.pop()
            # print "Popped Item from the stack : ", currentStatePath, len(currentStatePath)
            currentState = currentStatePath[0][0]
            # print "Got currentState as : ", currentState
        else:
            # print "found goal state : ", currentStatePath
            foundGoal = True

        if foundGoal:
            break

    dirPath = []
    for state in currentStatePath:
        step = state[1]
        if step is not 'Start':
            dirPath.append(step)
    dirPath.reverse()

    return list(dirPath)


# Calculate the total cost of the the path
def getCurrentStatePathCost(currentStatePath):
    cost = 0
    for state in currentStatePath:
        cost=cost+state[2]
    return cost

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    print "Start:", problem.getStartState()

    # Since we want to implement A Star Search, we are using a Priority queue as our fringe list
    fringeList = util.PriorityQueue()
    alreadyExpandedItemsList = []

    currentState = problem.getStartState()
    currentStatePath = [(currentState, 'Start', 0,)]
    foundGoal = False

    while True:
        if not problem.isGoalState(currentState):
            # print "\n\nalreadyExpandedItemsList : ", alreadyExpandedItemsList
            if currentState not in alreadyExpandedItemsList:

                successorsRichData = problem.getSuccessors(currentState)
                # print "successors : ", successorsRichData

                for successor in successorsRichData:
                    tempStatePath = list(currentStatePath)
                    tempStatePath.insert(0, successor)
                    # Forward Cost estimated by heuristic
                    h = heuristic(successor[0], problem)
                    # Backward Cost of the current path travelled
                    g = getCurrentStatePathCost(tempStatePath)
                    totalCost = g + h

                    fringeList.push(tempStatePath, totalCost)

                alreadyExpandedItemsList.append(currentState)

            else:
                # print "already expanded : ", currentState
                pass
            currentStatePath = fringeList.pop()
            # print "Popped Item from the stack : ", currentStatePath, len(currentStatePath)
            currentState = currentStatePath[0][0]
            # print "Got currentState as : ", currentState

        else:
            # print "found goal state : ", currentStatePath
            foundGoal = True

        if foundGoal:
            break

    dirPath = []
    for state in currentStatePath:
        step = state[1]
        if step is not 'Start':
            dirPath.append(step)
    dirPath.reverse()

    print "found direction path as : ", list(dirPath)

    return list(dirPath)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
