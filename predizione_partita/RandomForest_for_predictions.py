import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.ensemble import RandomForestClassifier
def stampa_learning_curve(metodo):
    train_sizes, train_scores, test_scores = learning_curve(
        metodo, X, y, cv=5, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10))

    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.legend(loc="best")
    plt.show()

df = pd.read_csv('../dataset/squadre.csv')
df = df.drop(['casa_puntiFatti'], axis='columns')
df =df.drop(['casa_puntiSubiti'], axis='columns')
df =df.drop(['ospiti_puntiFatti'], axis='columns')
df =df.drop(['ospiti_puntiSubiti'], axis='columns')
df =df.drop(['casa_t1_r'], axis='columns')
df =df.drop(['casa_t2_r'], axis='columns')
df =df.drop(['casa_t3_r'], axis='columns')
df =df.drop(['ospiti_t1_r'], axis='columns')
df =df.drop(['ospiti_t2_r'], axis='columns')
df =df.drop(['ospiti_t3_r'], axis='columns')

X = pd.get_dummies(df.drop(['result'], axis='columns'))
y = df['result'].apply(lambda x: 0 if x == 'victory' else 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)


from sklearn.ensemble import RandomForestClassifier

# Define a range of values to test for max_depth
max_depth_values = [2, 4, 6, 8, 10]

# Define a range of values to test for random_state
random_state_values = [0, 4, 16, 64, 256, 1024,4096]

# Store the mean cross-validation scores for each combination of max_depth and random_state
scores = []
for max_depth in max_depth_values:
    for random_state in random_state_values:
        RFC = RandomForestClassifier(max_depth=max_depth, random_state=random_state)
        cv_scores = cross_val_score(RFC, X, y, cv=5)
        scores.append((max_depth, random_state, cv_scores.mean()))

# Convert the scores list to a numpy array
scores = np.array(scores)

# Get the index of the maximum score
best_index = np.argmax(scores[:,2])

# Get the best max_depth and random_state values
best_max_depth = scores[best_index, 0]
best_random_state = scores[best_index, 1]

# Print the best max_depth and random_state values
print("Best max_depth value: {}".format(best_max_depth))
print("Best random_state value: {}".format(best_random_state))

RFC = RandomForestClassifier(max_depth=int(best_max_depth), random_state=int(best_random_state))
RFC.fit(X, y)
scores = cross_val_score(RFC, X, y, cv=5)
print("Cross-validation scores: {}".format(scores))
print("Average cross-validation score: {:.2f} +/- {:.2f}".format(scores.mean(), scores.std()))
stampa_learning_curve(RFC)
