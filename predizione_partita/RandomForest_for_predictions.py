import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
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
X = pd.get_dummies(df.drop(['result'], axis='columns'))
y = df['result'].apply(lambda x: 0 if x == 'victory' else 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
pred = list(np.array(model.predict(X_test)))
y_test = list(y_test)
print(pred)
print(y_test)
val=0
i = 0
for a in pred:
    if y_test[i] == pred[i]:
        val = val + 1
    i = i+1

val = val/len(pred)

print(val)
stampa_learning_curve(model)