from pomegranate import *
import pandas as pd

Burglary = DiscreteDistribution(
    {
        'T': 0.001,
        'F': 0.999
    }
)

EarthQuake = DiscreteDistribution(
    {
        'T': 0.002,
        'F': 0.998
    }
)

Alarm = ConditionalProbabilityTable(
    [
        ['T', 'T', 'T', 0.95],
        ['T', 'F', 'T', 0.94],
        ['F', 'T', 'T', 0.29],
        ['F', 'F', 'T', 0.001],

        ['T', 'T', 'F', 0.05],
        ['T', 'F', 'F', 0.06],
        ['F', 'T', 'F', 0.71],
        ['F', 'F', 'F', 0.999],
    ],
    [Burglary, EarthQuake]
)

JohnC = ConditionalProbabilityTable(
    [
        ['T', 'T', 0.9],
        ['T', 'F', 0.1],
        ['F', 'T', 0.05],
        ['F', 'F', 0.95],
    ],
    [Alarm]
)

MaryC = ConditionalProbabilityTable(
    [
        ['T', 'T', 0.7],
        ['T', 'F', 0.3],
        ['F', 'T', 0.01],
        ['F', 'F', 0.99],
    ],
    [Alarm]
)


s1 = Node(Burglary, name="Burglary")
s2 = Node(EarthQuake, name="EarthQuake")
s3 = Node(Alarm, name="Alarm")
s4 = Node(JohnC, name="JohnC")
s5 = Node(MaryC, name="MaryC")

model = BayesianNetwork("Buglary Problem")

model.add_states(s1, s2, s3, s4, s5)

model.add_edge(s1, s3)
model.add_edge(s2, s3)
model.add_edge(s3, s4)
model.add_edge(s3, s5)

model.bake()

idx = ['P(Alarm)', 'P(J && ~M)', 'P(B | A)', 'P(A | J && ~M)',
       'P(B | J && ~M)', 'P(J && ~M | ~B)']

df = pd.DataFrame(index=idx, columns=['Probability'])

# P(A)
df['Probability']['P(Alarm)'] = str(
    model.predict_proba({})[2].parameters[0]['T'])

# P(J && ~M)
PJ = model.predict_proba({'MaryC': 'F'})[3].parameters[0]['T']
PM = model.predict_proba({'JohnC': 'T'})[4].parameters[0]['F']
df['Probability']['P(J && ~M)'] = str(PJ * PM)

# P(A | J && ~M)
df['Probability']['P(A | J && ~M)'] = str(model.predict_proba(
    {'JohnC': 'T', 'MaryC': 'F'})[2].parameters[0]['T'])

# P(B | A)
df['Probability']['P(B | A)'] = str(
    model.predict_proba({'Alarm': 'T'})[0].parameters[0]['T'])

# P(B | J && ~M)
df['Probability']['P(B | J && ~M)'] = str(model.predict_proba(
    {'JohnC': 'T', 'MaryC': 'F'})[0].parameters[0]['T'])

# P(J && ~M | ~B)
PJ = model.predict_proba({'MaryC': 'F', 'Burglary': 'F'})[3].parameters[0]['T']
PM = model.predict_proba({'JohnC': 'T', 'Burglary': 'F'})[4].parameters[0]['F']
df['Probability']['P(J && ~M | ~B)'] = str(PJ * PM)

print(df)
