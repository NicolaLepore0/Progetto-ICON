
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
    "casa_falliFatti",
    "casa_pallePerse",
    "casa_palleRecuperate",
    "casa_t2_r",
    "casa_t3_r",
    "casa_t1_r",
    "casa_t2_s",
    "casa_t3_s",
    "casa_t1_s",
    "ospiti_puntiFatti",
    "ospiti_puntiSubiti",
    "ospiti_falliFatti",
    "ospiti_pallePerse",
    "ospiti_palleRecuperate",
    "ospiti_t2_r",
    "ospiti_t3_r",
    "ospiti_t1_r",
    "ospiti_t2_s",
    "ospiti_t3_s",
    "ospiti_t1_s",
    "result",
]
df = pd.read_csv("../dataset/squadre.csv", usecols=nodes)

# apply discretization
N_BINS = 2

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
    "lose": "B"
}
data["result"] = [results[r] for r in df["result"]]

# Setting the model
# set the structure
model = BayesianNetwork(
    [
        ("casa_puntiFatti", "result"),
        ("casa_puntiSubiti", "result"),
        ("casa_falliFatti","casa_puntiSubiti"),
        ("casa_pallePerse","casa_puntiSubiti"),
        ("casa_palleRecuperate", "casa_puntiFatti"),
        ('casa_falliFatti', 'casa_pallePerse'),
        ("casa_t2_s","casa_pallePerse"),
        ("casa_t3_s","casa_pallePerse"),
        ("casa_t1_s","casa_pallePerse"),
        ("casa_t2_r","casa_puntiFatti"),
        ("casa_t3_r","casa_puntiFatti"),
        ("casa_t1_r","casa_puntiFatti"),

        ("ospiti_puntiFatti", "result"),
        ("ospiti_puntiSubiti", "result"),
        ("ospiti_falliFatti","ospiti_puntiSubiti"),
        ("ospiti_pallePerse", "ospiti_puntiSubiti"),
        ("ospiti_palleRecuperate", "ospiti_puntiFatti"),
        ('ospiti_falliFatti','ospiti_pallePerse'),
        ("ospiti_t2_s","ospiti_pallePerse"),
        ("ospiti_t3_s","ospiti_pallePerse"),
        ("ospiti_t1_s","ospiti_pallePerse"),
        ("ospiti_t2_r","ospiti_puntiFatti"),
        ("ospiti_t3_r","ospiti_puntiFatti"),
        ("ospiti_t1_r","ospiti_puntiFatti"),
    ]
)

total = len(df['result'])
features_count = {node: val_counter(node, data) for node in nodes[:-1]}

##################################### home

print('TabularCPD casa_pallePerse')
casa_pallePerse_cpd = TabularCPD(
    variable="casa_pallePerse",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["casa_pallePerse", "casa_falliFatti", "casa_t2_s","casa_t3_s","casa_t1_s"], 'AB'),
    evidence=["casa_falliFatti", "casa_t2_s","casa_t3_s","casa_t1_s",],
    evidence_card=[N_BINS, N_BINS,N_BINS, N_BINS],
)

print('TabularCPD casa_falliFatti')
casa_falliFatti_cpd = TabularCPD(
    variable="casa_falliFatti",
    variable_card=N_BINS,
    values=[
        [features_count['casa_falliFatti']['A'] / total],
        [features_count['casa_falliFatti']['B'] / total],
    ],
)
print('TabularCPD casa_t2_s')
casa_t2_s_cpd = TabularCPD(
    variable="casa_t2_s",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t2_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t2_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_t3_s')
casa_t3_s_cpd = TabularCPD(
    variable="casa_t3_s",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t3_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t3_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_t1_s')
casa_t1_s_cpd = TabularCPD(
    variable="casa_t1_s",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t1_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t1_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_t2_r')
casa_t2_r_cpd = TabularCPD(
    variable="casa_t2_r",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t2_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t2_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_t3_r')
casa_t3_r_cpd = TabularCPD(
    variable="casa_t3_r",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t3_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t3_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_t1_')
casa_t1_r_cpd = TabularCPD(
    variable="casa_t1_r",
    variable_card=N_BINS,
    values=[
        [features_count['casa_t1_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_t1_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD casa_puntiFatti')
casa_puntiFatti_cpd = TabularCPD(
    variable="casa_puntiFatti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["casa_puntiFatti", "casa_t2_r","casa_t3_r","casa_t1_r","casa_palleRecuperate"], 'AB'),
    evidence=["casa_t2_r","casa_t3_r","casa_t1_r","casa_palleRecuperate"],
    evidence_card=[N_BINS,N_BINS,N_BINS,N_BINS],
)
print('TabularCPD casa_puntiSubiti')
casa_puntiSubiti_cpd = TabularCPD(
    variable="casa_puntiSubiti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["casa_puntiSubiti", "casa_falliFatti", "casa_pallePerse"], 'AB'),
    evidence=["casa_falliFatti", "casa_pallePerse"],
    evidence_card=[N_BINS, N_BINS],
)
print('TabularCPD casa_palleRecuperate')
casa_palleRecuperate_cpd = TabularCPD(
    variable="casa_palleRecuperate",
    variable_card=N_BINS,
    values=[
        [features_count['casa_palleRecuperate']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['casa_palleRecuperate']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

##################################### away
print('TabularCPD ospiti_pallePerse')
ospiti_pallePerse_cpd = TabularCPD(
    variable="ospiti_pallePerse",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_pallePerse", "ospiti_falliFatti", "ospiti_t2_s","ospiti_t3_s","ospiti_t1_s"], 'AB'),
    evidence=["ospiti_falliFatti", "ospiti_t2_s","ospiti_t3_s","ospiti_t1_s",],
    evidence_card=[N_BINS, N_BINS,N_BINS, N_BINS],
)

print('TabularCPD ospiti_falliFatti')
ospiti_falliFatti_cpd = TabularCPD(
    variable="ospiti_falliFatti",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_falliFatti']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_falliFatti']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

print('TabularCPD ospiti_puntiFatti')
ospiti_puntiFatti_cpd = TabularCPD(
    variable="ospiti_puntiFatti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_puntiFatti", "ospiti_t2_r","ospiti_t3_r","ospiti_t1_r","ospiti_palleRecuperate"], 'AB'),
    evidence=["ospiti_t2_r","ospiti_t3_r","ospiti_t1_r","ospiti_palleRecuperate"],
    evidence_card=[N_BINS,N_BINS,N_BINS,N_BINS],
)
print('TabularCPD ospiti_puntiSubiti')
ospiti_puntiSubiti_cpd = TabularCPD(
    variable="ospiti_puntiSubiti",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["ospiti_puntiSubiti", "ospiti_falliFatti", "ospiti_pallePerse"], 'AB'),
    evidence=["ospiti_falliFatti", "ospiti_pallePerse"],
    evidence_card=[N_BINS, N_BINS],
)
print('TabularCPD ospiti_palleRecuperate')
ospiti_palleRecuperate_cpd = TabularCPD(
    variable="ospiti_palleRecuperate",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_palleRecuperate']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_palleRecuperate']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

print('TabularCPD ospiti_t2_s')
ospiti_t2_s_cpd = TabularCPD(
    variable="ospiti_t2_s",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t2_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t2_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD ospiti_t3_s')
ospiti_t3_s_cpd = TabularCPD(
    variable="ospiti_t3_s",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t3_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t3_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD ospiti_t1_s')
ospiti_t1_s_cpd = TabularCPD(
    variable="ospiti_t1_s",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t1_s']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t1_s']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD ospiti_t2_r')
ospiti_t2_r_cpd = TabularCPD(
    variable="ospiti_t2_r",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t2_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t2_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD ospiti_t3_r')
ospiti_t3_r_cpd = TabularCPD(
    variable="ospiti_t3_r",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t3_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t3_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)
print('TabularCPD ospiti_t1_r')
ospiti_t1_r_cpd = TabularCPD(
    variable="ospiti_t1_r",
    variable_card=N_BINS,
    values=[
        [features_count['ospiti_t1_r']['A'] / total],  # A: 0.0, 0.1081081081081081
        [features_count['ospiti_t1_r']['B'] / total],  # C: 0.2162162162162162, 0.3243243243243243
    ],
)

#################### result
print('TabularCPD result')
result_cpd = TabularCPD(
    variable="result",
    variable_card=N_BINS,
    values=calc_matrix_with_cols(["result", "casa_puntiFatti", "casa_puntiSubiti", "ospiti_puntiFatti", "ospiti_puntiSubiti"], 'AB'),
    evidence=[
        "casa_puntiFatti",
        "casa_puntiSubiti",
        "ospiti_puntiFatti",
        "ospiti_puntiSubiti",
    ],
    evidence_card=[2, 2, 2, 2],
)

print('Adding cpds')
#################### aggiungo CPD
model.add_cpds(
    casa_puntiFatti_cpd,
    casa_puntiSubiti_cpd,
    casa_falliFatti_cpd,
    casa_pallePerse_cpd,
    casa_palleRecuperate_cpd,
    casa_t2_s_cpd,
    casa_t3_s_cpd,
    casa_t1_s_cpd,
    casa_t2_r_cpd,
    casa_t3_r_cpd,
    casa_t1_r_cpd,

    ospiti_puntiFatti_cpd,
    ospiti_puntiSubiti_cpd,
    ospiti_falliFatti_cpd,
    ospiti_pallePerse_cpd,
    ospiti_palleRecuperate_cpd,
    ospiti_t2_s_cpd,
    ospiti_t3_s_cpd,
    ospiti_t1_s_cpd,
    ospiti_t2_r_cpd,
    ospiti_t3_r_cpd,
    ospiti_t1_r_cpd,

    result_cpd,
)

print('calculating inference')
inference = VariableElimination(model)

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
    }
    expected_result = df.iloc[i]['result']
    del obj['result']
    obj = {k: corr_dict[v] for k, v in obj.items()}
    prob = inference.query(variables=["result"], evidence=obj, show_progress=False)
    str_int = {
        'victory': 0,
        'lose': 1,
    }

    print(f'expected_result: {expected_result}, {np.argmax(prob)},\nactual_result: {prob}')
    if np.argmax(prob) == str_int[expected_result]:
        correct += 1

print(f"Accuracy: {correct / i}")

import matplotlib.pyplot as plt
import networkx as nx

# Get the graph representation of the model
G = nx.DiGraph(model.edges())

# Set the node positions
pos = nx.spring_layout(G)

# Plot the graph
nx.draw(G, pos, with_labels=True, font_size=10, node_size=1000, node_color='lightblue')

# Show the plot
plt.show()