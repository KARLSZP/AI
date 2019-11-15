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
    """
    from util import Stack
    from game import Directions
 
    Stk = Stack()
    closed = []
 
    Stk.push((problem.getStartState(), []))
 
    while not Stk.isEmpty():
        
        cur_node, actions = Stk.pop()
 
        if problem.isGoalState(cur_node):
            return actions
 
        if cur_node not in closed:
            expand = problem.getSuccessors(cur_node)
            closed.append(cur_node)
            for location, direction, cost in expand:
                if (location not in closed):
                    Stk.push((location, actions + [direction]))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from game import Directions
    queue = util.Queue()
    visited = []
    queue.push([problem.getStartState(), []])

    while not queue.isEmpty():
        state, actions = queue.pop()
        
        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.append(state)
            succs = problem.getSuccessors(state)

            for succ, action, c in succs:
                if succ not in visited:
                    queue.push([succ, actions + [action]])
    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start = problem.getStartState()                           
    queue = util.PriorityQueueWithFunction(lambda x: x[2])         
    queue.push((start,None,0))                               
    cost = 0
    visited = []                                                    
    actions = []                                                       
    parents = {}
    parents[(start,None,0)]=None
    while queue.isEmpty() == False:
        cur_state = queue.pop()                            

        if (problem.isGoalState(cur_state[0])):             
            break
        else:
            current_state = cur_state[0]
            if current_state not in visited:
                visited.append(current_state)
            else:
                continue
            successors = problem.getSuccessors(current_state)           
            for state in successors:
                cost= cur_state[2] + state[2]
                
                if state[0] not in visited:
                    queue.push((state[0],state[1],cost))
                    
                    parents[(state[0],state[1])] = cur_state
 
    child = cur_state
 
    while (child != None):
        actions.append(child[1])
        if child[0] != start:
            child = parents[(child[0],child[1])]
        else:
            child = None
    actions.reverse()
    actions = actions[1:]
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Use Priority Queue to implement non-recursive A*:
    # 1. Push the start node into the queue.
    # 2. Do while-loop until the queue is empty:
    #   - Get the top node.
    #   - IF the node is the GOAL
    #       * break the while-loop and return
    #   - ELSE IF the top node has been visited or has no successor:
    #       * continue
    #   - ELSE
    #       * Go through its successors.
    #       * Push those unvisited successors into the queue with their cost.
    # Return:
    #   actions: a list of actions that approach the GOAL.
    #
    from util import PriorityQueue
    actions = [] # Store the result
    tmp_actions = [] # Store the temp result in the while-loop
    visited = [] # Store the nodes that have been visited
    pQueue = PriorityQueue()
    # The priority queue
    # element type : [current state, actions so far]
    pQueue.push((problem.getStartState(), actions), 0) # Initialization

    # While-Loop
    while not pQueue.isEmpty():
        # Get the top node
        cur_node, actions = pQueue.pop()

        # GOAL, which means the cur_node is the target state, 
        # and is also the last element of the actions list.
        if problem.isGoalState(cur_node): 
            break
            
        # Check visited
        if cur_node in visited:
            continue
        
        visited.append(cur_node)
        succs = problem.getSuccessors(cur_node)
        # As declare above, getSuccessors() return a generator contains
        # elements in the form: (succ[list], Direction[n, s, e, w], cost[int])
        for succ, action, _ in succs:
            # Also, Checl visited
            tmp_actions = actions + [action]
            next_cost = problem.getCostOfActions(tmp_actions) + heuristic(succ, problem)
            if succ not in visited:
                pQueue.push((succ, tmp_actions), next_cost)

    # Return the Goal actions
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
