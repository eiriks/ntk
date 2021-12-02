import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVC
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('data/names_with_features.csv',
                        sep=',')

# , dtype=np.float64

features = tpot_data.drop(['Gender', 'Name'], axis=1)
#features = tpot_data.drop('Gender', axis=1)
print(features.head())
training_features, testing_features, training_target, testing_target = \
    train_test_split(features, tpot_data['Gender'], random_state=42)

# # Average CV score on the training set was: 0.8589454871474242
exported_pipeline = make_pipeline(
    StackingEstimator(estimator=LinearSVC(C=0.1, dual=False,
                                          loss="squared_hinge", penalty="l1", tol=0.001)),
    MultinomialNB(alpha=0.001, fit_prior=True)
)
# # Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)

print(results)

# 0.8674435542607429
print(exported_pipeline.score(testing_features, testing_target))
