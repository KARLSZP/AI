# Tutorial for Q-Learning - Reinforcement Learning
# @ 17341137 Zhenpeng Song

import numpy as np


def get_accessible_action(state):
    legal_actions = [idx for idx, val in enumerate(
        list(R[state])) if val != -1]
    action_idx = np.random.randint(len(legal_actions))
    return legal_actions[action_idx]


def get_max_Q_value_by_state(state):
    return max(Q[state])


""" Initialization """
# R: State - Action matrix
R = np.array([
    [-1, -1, -1, -1,  0,  -1],
    [-1, -1, -1,  0, -1, 100],
    [-1, -1, -1,  0, -1, -1],
    [-1,  0,  0, -1,  0,  -1],
    [0, -1, -1,  0, -1, 100],
    [-1, -1, -1, -1,  0, 100],
])

# Q_value matrix
num_state, num_action = R.shape
Q = np.zeros((num_state, num_action))

GAMMA = 0.5     # gamma parameters
trace = []      # Trace of path


def Q_Learning(cur_state, end_state, iters=200):
    trace.append(cur_state)
    # Run some episodes
    # while cur_state != end_state:
    for i in range(iters):
        # get next action
        next_state = get_accessible_action(cur_state)
        # When the next state is chosen,
        # an R-value is chosen.
        R_value = R[cur_state, next_state]
        max_Q_value = get_max_Q_value_by_state(next_state)
        # update Q matrix
        Q[cur_state, next_state] = round(R_value + GAMMA * max_Q_value)

        # update current state
        cur_state = next_state
        trace.append(cur_state)


def solve_with_Q_matrix(init_state, end_state, Q):
    path = [init_state]
    cur_state = init_state
    while cur_state != end_state:
        cur_state = np.argmax(Q[cur_state])
        path.append(cur_state)
    return path


def main(state):
    init_state, end_state = state
    Q_Learning(init_state, end_state, 200)
    path = solve_with_Q_matrix(init_state, end_state, Q)
    print(Q, path)


if __name__ == "__main__":
    for i in range(6):
        main((i, 5))
