from pomegranate import *

PatientAge = DiscreteDistribution(
    {
        'A': 0.10,
        'B': 0.30,
        'C': 0.60
    }
)

CTScanResult = DiscreteDistribution(
    {
        'IS': 0.7,
        'HS': 0.3
    }
)

MRIScanResult = DiscreteDistribution(
    {
        'IS': 0.7,
        'HS': 0.3
    }
)

Anticoagulants = DiscreteDistribution(
    {
        'T': 0.5,
        'F': 0.5
    }
)

StrokeType = ConditionalProbabilityTable(
    [
        ['IS', 'IS', 'IS', 0.8],
        ['IS', 'HS', 'IS', 0.5],
        ['HS', 'IS', 'IS', 0.5],
        ['HS', 'HS', 'IS', 0.0],

        ['IS', 'IS', 'HS', 0.0],
        ['IS', 'HS', 'HS', 0.4],
        ['HS', 'IS', 'HS', 0.4],
        ['HS', 'HS', 'HS', 0.9],

        ['IS', 'IS', 'SM', 0.2],
        ['IS', 'HS', 'SM', 0.1],
        ['HS', 'IS', 'SM', 0.1],
        ['HS', 'HS', 'SM', 0.1],
    ],
    [CTScanResult, MRIScanResult]
)

Mortality = ConditionalProbabilityTable(
    [
        ['IS', 'T', 'F', 0.28],
        ['HS', 'T', 'F', 0.99],
        ['SM', 'T', 'F', 0.10],
        ['IS', 'F', 'F', 0.56],
        ['HS', 'F', 'F', 0.58],
        ['SM', 'F', 'F', 0.05],
        ['IS', 'T', 'T', 0.72],
        ['HS', 'T', 'T', 0.01],
        ['SM', 'T', 'T', 0.90],
        ['IS', 'F', 'T', 0.44],
        ['HS', 'F', 'T', 0.42],
        ['SM', 'F', 'T', 0.95],
    ],
    [StrokeType, Anticoagulants]
)

Disability = ConditionalProbabilityTable(
    [
        ['IS', 'A', 'N', 0.80],
        ['HS', 'A', 'N', 0.70],
        ['SM', 'A', 'N', 0.90],
        ['IS', 'B', 'N', 0.60],
        ['HS', 'B', 'N', 0.50],
        ['SM', 'B', 'N', 0.40],
        ['IS', 'C', 'N', 0.30],
        ['HS', 'C', 'N', 0.20],
        ['SM', 'C', 'N', 0.10],

        ['IS', 'A', 'M', 0.10],
        ['HS', 'A', 'M', 0.20],
        ['SM', 'A', 'M', 0.05],
        ['IS', 'B', 'M', 0.30],
        ['HS', 'B', 'M', 0.40],
        ['SM', 'B', 'M', 0.30],
        ['IS', 'C', 'M', 0.40],
        ['HS', 'C', 'M', 0.20],
        ['SM', 'C', 'M', 0.10],

        ['IS', 'A', 'S', 0.10],
        ['HS', 'A', 'S', 0.10],
        ['SM', 'A', 'S', 0.05],
        ['IS', 'B', 'S', 0.10],
        ['HS', 'B', 'S', 0.10],
        ['SM', 'B', 'S', 0.30],
        ['IS', 'C', 'S', 0.30],
        ['HS', 'C', 'S', 0.60],
        ['SM', 'C', 'S', 0.80],
    ],
    [StrokeType, PatientAge]
)


s1 = Node(PatientAge, name="PatientAge")
s2 = Node(CTScanResult, name="CTScanResult")
s3 = Node(MRIScanResult, name="MRIScanResult")
s4 = Node(Anticoagulants, name="Anticoagulants")
s5 = Node(StrokeType, name="StrokeType")
s6 = Node(Mortality, name="Mortality")
s7 = Node(Disability, name="Disability")

model = BayesianNetwork("Diagnosing Problem")

model.add_states(s1, s2, s3, s4, s5, s6, s7)

model.add_edge(s2, s5)
model.add_edge(s3, s5)

model.add_edge(s5, s6)
model.add_edge(s4, s6)

model.add_edge(s5, s7)
model.add_edge(s1, s7)

model.bake()


# P(1)
print('P(1) = ', model.predict_proba(
    {'PatientAge': 'B', 'CTScanResult': 'IS'})[5].parameters[0]['T'])

# P(2)
print('P(2) = ', model.predict_proba(
    {'PatientAge': 'C', 'MRIScanResult': 'HS'})[6].parameters[0]['M'])

# P(3)
print('P(3) = ', model.predict_proba(
    {'PatientAge': 'C', 'CTScanResult': 'HS', 'MRIScanResult': 'IS'})[4].parameters[0]['SM'])

# P(4)
print('P(4) = ', model.predict_proba(
    {'PatientAge': 'A'})[3].parameters[0]['F'])

# Helper
print('P1 = ', model.predict_proba(
    {})[5].parameters[0]['T'])

print('P2 = ', model.predict_proba(
    {'PatientAge': 'B'})[1].parameters[0]['IS'])

print('P3 = ', model.predict_proba(
    {'PatientAge': 'C', 'CTScanResult': 'HS', 'MRIScanResult': 'IS'})[4].parameters[0]['HS'])

print('P4 = ', model.predict_proba(
    {})[6].parameters[0]['N'])
