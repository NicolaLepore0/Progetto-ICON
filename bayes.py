
import pandas as pd
import itertools
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference.ExactInference import VariableElimination
from string import ascii_uppercase
from pandas import DataFrame

# Gathering data
nodes = [
    "casa_puntiFatti",
    "casa_puntiSubiti",
    "casa_tiri",
    "casa_pallePerse",
    "casa_falli",
    "ospiti_puntiFatti",
    "ospiti_puntiSubiti",
    "ospiti_tiri",
    "ospiti_pallePerse",
    "ospiti_falli",
    "result",
]
df = pd.read_csv("./datasets/dataset_for_NN.csv", usecols=nodes)

# apply discretization
N_BINS = 3

def equal_width(values, n_bins):
    min_val = min(values)
    max_val = max(values)
    interval_width = (max_val - min_val) / n_bins
    intervals = [min_val + interval_width * i for i in range(n_bins + 1)]
    return intervals


def count_per_interval(values, intervals):
    n_bins = len(intervals) - 1
    count_arr = [0 for _ in range(n_bins)]
    for j, val in enumerate(values):
        for i in range(n_bins):
            if intervals[i] <= val <= intervals[i + 1]:
                count_arr[i] += 1
                break
        else:
            print(j, val)
    return count_arr


def get_index_of_count(val: float, intervals: list) -> int:
    for i in range(len(intervals) - 1):
        if intervals[i] <= val <= intervals[i + 1]:
            return ascii_uppercase[i]


def create_dataframe(nodes: list, df: DataFrame, n_bins: int) -> dict:
    dataframe = {}
    for col in nodes[:-1]:
        values = df[col]
        intervals = equal_width(values, n_bins)
        dataframe[col] = [get_index_of_count(value, intervals) for value in values]
    return dataframe

def val_counter(cols: str, data: DataFrame) -> dict:
    val_count = {ascii_uppercase[i]: 0 for i in range(0, N_BINS)}
    for val in data[cols]:
        val_count[val] += 1
    return val_count

def multi_val_counter(cols: list, indexMatrix: str, data: DataFrame) -> int:
    val_count = 0
    for v in data.iloc:
        for i, c in enumerate(cols):
            if v[c] != indexMatrix[i]:
                break
        else:
            val_count += 1
    return val_count

def generate_tuples(cols: list, indexLen: int):
    tup = [chr(ord("A") + c) for c in range(indexLen)]
    return [p for p in itertools.product(tup, repeat=len(cols))]

def calc_matrix_with_cols(cols: list, indexes: str):
    matrix = [[] for _ in range(len(indexes))]
    t = generate_tuples(cols, len(indexes))
    for i, index in enumerate(indexes):
        part = [p for p in t if p[0] == index]
        for p in part:
            matrix[i].append(multi_val_counter(cols, "".join(p), data))
    matrix_sum = []
    N_ROWS = len(matrix)
    for i in range(len(matrix[0])):
        sum_col = 0
        for j in range(N_ROWS):
            sum_col += matrix[j][i]
        matrix_sum.append(sum_col)
    for i, s in enumerate(matrix_sum):
        if s == 0:
            perc_temp = 1 / N_ROWS
            for j in range(len(matrix)):
                matrix[j][i] = perc_temp
        else:
            for j in range(len(matrix)):
                matrix[j][i] /= s
    return matrix

new_column = create_dataframe(nodes, df, N_BINS)
data = DataFrame(data=new_column)
results = {
    "victory": "A",
    "draw": "B",
    "lose": "C"
}
data["result"] = [results[r] for r in df["result"]]

# Setting the model

# set the structure
model = BayesianNetwork(
    [
        ("casa_puntiSubiti", "result"),
        ("casa_puntiFatti", "result"),
        ("casa_tiri", "casa_puntiFatti"),
        ("casa_falli", "casa_puntiSubiti"),
        ('casa_pallePerse', 'casa_puntiSubiti'),
        ("ospiti_puntiSubiti", "result"),
        ("ospiti_puntiFatti", "result"),
        ("ospiti_tiri", "ospiti_puntiFatti"),
        ("ospiti_falli", "ospiti_puntiSubiti"),
        ('ospiti_pallePerse', 'ospiti_puntiSubiti')
    ]
)

total = len(df['result'])
features_count = {node: val_counter(node, data) for node in nodes[:-1]}

##################################### home

print('TabularCPD casa_pallePerse')
casa_pallePerse_cpd = TabularCPD(
    variable="casa_pallePerse",
    variable_card=N_BINS,
    values=[
        [features_count['casa_pallePerse']['A'] / total],  # A
        [features_count['casa_pallePerse']['B'] / total],  # B
        [features_count['casa_pallePerse']['C'] / total],  # C
    ],
)

print('TabularCPD casa_falli')
casa_falli_cpd = TabularCPD(
    variable="casa_falli",
    variable_card=N_BINS,
    values=[
        [features_count['casa_falli']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_falli']['B'] / total],  # B: 0.1081081081081081, 0.2162162162162162
        [features_count['casa_falli']['C'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

print('TabularCPD casa_tiri')
casa_tiri_cpd = TabularCPD(
    variable="casa_tiri",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["home_bigChances", "home_accurateCrosses", "home_accurateOppositionHalfPasses"], 'ABC'),
    evidence=["home_accurateCrosses", "home_accurateOppositionHalfPasses"],
    evidence_card=[N_BINS, N_BINS],
)

print('TabularCPD casa_puntiFatti')
casa_puntiFatti_cpd = TabularCPD(
    variable="casa_puntiFatti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["casa_puntiFatti", "home_bigChances", "casa_tiri"], 'ABC'),
    evidence=["home_bigChances", "casa_tiri"],
    evidence_card=[N_BINS, N_BINS],
)
print('TabularCPD casa_puntiSubiti')
casa_puntiSubiti_cpd = TabularCPD(
    variable="casa_puntiSubiti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["casa_puntiSubiti", "casa_falli", "home_errorsLeadingToShot", "casa_pallePerse"], 'ABC'),
    evidence=["casa_falli", "home_errorsLeadingToShot", "casa_pallePerse"],
    evidence_card=[N_BINS, N_BINS, N_BINS],
)

##################################### away

print('TabularCPD ospiti_pallePerse')
ospiti_pallePerse_cpd = TabularCPD(
    variable="ospiti_pallePerse",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_pallePerse']['A'] / total],  # A:
        [features_count['ospiti_pallePerse']['B'] / total],  # B:
        [features_count['ospiti_pallePerse']['C'] / total],  # C:
    ],
)

print('TabularCPD ospiti_falli')
ospiti_falli_cpd = TabularCPD(
    variable="ospiti_falli",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_falli']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_falli']['B'] / total],  # B: 0.1081081081081081, 0.2162162162162162
        [features_count['ospiti_falli']['C'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

print('TabularCPD ospiti_tiri')
ospiti_tiri_cpd = TabularCPD(
    variable="ospiti_tiri",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_tiri", "away_accurateCrosses", "away_accurateOppositionHalfPasses"], 'ABC'),
    evidence=["away_accurateCrosses", "away_accurateOppositionHalfPasses"],
    evidence_card=[N_BINS, N_BINS],
)

print('TabularCPD ospiti_puntiFatti')
ospiti_puntiFatti_cpd = TabularCPD(
    variable="ospiti_puntiFatti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_puntiFatti", "away_bigChances", "ospiti_tiri"], 'ABC'),
    evidence=["away_bigChances", "ospiti_tiri"],
    evidence_card=[N_BINS, N_BINS],
)
print('TabularCPD ospiti_puntiSubiti')
ospiti_puntiSubiti_cpd = TabularCPD(
    variable="ospiti_puntiSubiti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_puntiSubiti", "ospiti_falli", "away_errorsLeadingToShot", "ospiti_pallePerse"], 'ABC'),
    evidence=["ospiti_falli", "away_errorsLeadingToShot", "ospiti_pallePerse"],
    evidence_card=[N_BINS, N_BINS, N_BINS],
)

#################### result
print('TabularCPD result')
result_cpd = TabularCPD(
    variable="result",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["result", "casa_puntiFatti", "casa_puntiSubiti", "ospiti_puntiFatti", "ospiti_puntiSubiti"], 'ABC'),
    evidence=[
        "casa_puntiFatti",
        "casa_puntiSubiti",
        "ospiti_puntiFatti",
        "ospiti_puntiSubiti",
    ],
    evidence_card=[3, 3, 3, 3],
)

print('Adding cpds')
#################### aggiungo CPD
model.add_cpds(
    casa_pallePerse_cpd,
    casa_falli_cpd,
    casa_tiri_cpd,
    casa_puntiFatti_cpd,
    casa_puntiSubiti_cpd,
    ospiti_pallePerse_cpd,
    ospiti_falli_cpd,
    ospiti_tiri_cpd,
    ospiti_puntiFatti_cpd,
    ospiti_puntiSubiti_cpd,
    result_cpd,
)

print('calculating inference')
inference = VariableElimination(model)
#prob = inference.query(variables=["result"])
#print(prob)

max_n = 10
correct = 0
import numpy as np
import tqdm
for i, r in enumerate(tqdm.tqdm(data.iloc)):
    if i > max_n:
        break
    obj = {**r}
    corr_dict = {
        'A': 0,
        'B': 1,
        'C': 2,
    }
    expected_result = df.iloc[i]['result']
    del obj['result']
    obj = {k: corr_dict[v] for k, v in obj.items()}
    prob = inference.query(variables=["result"], evidence=obj, show_progress=False)
    str_int = {
        'victory': 0,
        'draw': 1,
        'lose': 2,
    }

    print(f'expected_result: {expected_result}, {np.argmax(prob)},\nactual_result: {prob}')
    if np.argmax(prob) == str_int[expected_result]:
        correct += 1

print(f"Accuracy: {correct / i}")