from VE import *

# Nodes for Bayes Net
# B     J
#  \.  /'
#    A
#  /'  \.
# E     M
B = Node("B", ["B"])
E = Node("E", ["E"])
A = Node("A", ["A", "B", "E"])
J = Node("J", ["J", "A"])
M = Node("M", ["M", "A"])

# Cpts for each Node
B.setCpt({'0': 0.999, '1': 0.001})
E.setCpt({'0': 0.998, '1': 0.002})
A.setCpt({'111': 0.95, '011': 0.05,
          '110': 0.94, '010': 0.06,
          '101': 0.29, '001': 0.71,
          '100': 0.001, '000': 0.999})
J.setCpt({'11': 0.9, '01': 0.1,
          '10': 0.05, '00': 0.95})
M.setCpt({'11': 0.7, '01': 0.3,
          '10': 0.01, '00': 0.99})

# Results
print("P(A) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['A'],
    ['B', 'E', 'J', 'M'],
    {}
)

print("P(J && ~M) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['J'],
    ['B', 'E', 'A'],
    {'M': 0}
)

print("P(A | J && ~M) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['A'],
    ['B', 'E'],
    {'J': 1, 'M': 0}
)

print("P(B | A) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['B'],
    ['E', 'J', 'M'],
    {'A': 1}
)

print("P(B | J && ~M) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['B'],
    ['E', 'A'],
    {'J': 1, 'M': 0}
)

print("P(J && ~M | ~B) **********************")
VariableElimination.inference(
    [B, E, A, J, M], ['J', 'M'],
    ['E', 'A'],
    {'B': 0}
)
