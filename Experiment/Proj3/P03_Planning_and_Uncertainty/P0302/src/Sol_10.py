from VE import *


# Notation
# P - PatientAge
# C - CTScanResult
# M - MRIScanResult
# S - StrokeType
# A - Anticoagulants
# Mo - Mortality
# D - Disability


# Nodes for Bayes Net
# P ---> D
#       /'
# M -> S ---> Mo
#     /'     /'
#    C      A
P = Node("p", ["P"])
M = Node("M", ["M"])
C = Node("C", ["C"])
A = Node("A", ["A"])
S = Node("S", ["S", "C", "M"])
D = Node("D", ["D", "S", "P"])
Mo = Node("Mo", ["Mo", "S", "A"])

# Cpts for each Node
P.setCpt({'0': 0.10, '1': 0.30, '2': 0.60})
# 0 - IS; 1 - HS; 2 - SM
# 0 - Ne; 1 - Mo; 2 - Se
C.setCpt({'0': 0.7, '1': 0.3})
M.setCpt({'0': 0.7, '1': 0.3})
A.setCpt({'0': 0.5, '1': 0.5})
S.setCpt({'000': 0.8, '001': 0.5,
          '010': 0.5, '011': 0.0,
          '100': 0.0, '101': 0.4,
          '110': 0.4, '111': 0.9,
          '200': 0.2, '201': 0.1,
          '210': 0.1, '211': 0.1})
Mo.setCpt({'000': 0.56, '001': 0.28,
           '010': 0.58, '011': 0.99,
           '020': 0.05, '021': 0.10,
           '100': 0.44, '101': 0.72,
           '110': 0.42, '111': 0.01,
           '120': 0.95, '121': 0.90})
D.setCpt({'000': 0.80, '010': 0.70, '020': 0.90,
          '001': 0.60, '011': 0.50, '021': 0.40,
          '002': 0.30, '012': 0.20, '022': 0.10,

          '100': 0.10, '110': 0.20, '120': 0.05,
          '101': 0.30, '111': 0.40, '121': 0.30,
          '102': 0.40, '112': 0.20, '122': 0.10,

          '200': 0.10, '210': 0.10, '220': 0.05,
          '201': 0.10, '211': 0.10, '221': 0.30,
          '202': 0.30, '212': 0.60, '222': 0.80})


# Nodes for Bayes Net
# P ---> D
#       /'
# M -> S ---> Mo
#     /'     /'
#    C      A

# Results
print("P1 **********************")
VariableElimination.inference(
    [P, M, C, A, S, D, Mo], ['Mo', 'C'],
    ['M', 'A', 'S', 'D'],
    {'P': 1}
)

print("P2 **********************")
VariableElimination.inference(
    [P, M, C, A, S, D, Mo], ['D', 'C'],
    ['A', 'S', 'Mo'],
    {'P': 2, 'M': 1}
)

print("P3 **********************")
VariableElimination.inference(
    [P, M, C, A, S, D, Mo], ['S'],
    ['D', 'A', 'Mo'],
    {'P': 2, 'C': 1, 'M': 0}
)

print("P4 **********************")
VariableElimination.inference(
    [P, M, C, A, S, D, Mo], ['A'],
    ['M', 'C', 'S', 'D', 'Mo'],
    {'P': 1}
)

print("P5 **********************")
VariableElimination.inference(
    [P, M, C, A, S, D, Mo], ['D'],
    ['P', 'M', 'C', 'A', 'S', 'Mo'],
    {}
)