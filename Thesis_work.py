# -*- coding: utf-8 -*-
"""Thesis Work.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tU05ZRpvNn28nMpUidAE7iK_-lBJeozI
"""

!pip install --pre pycaret[full]

import pandas as pd # Import the pandas library and give it the alias 'pd'
from google.colab import drive
from pycaret.regression import *
from pycaret.regression import RegressionExperiment
from pycaret.regression import models
from pycaret.regression import create_model, tune_model, evaluate_model, finalize_model, predict_model, save_model, load_model
!pip install scikit-learn xgboost lightgbm catboost imbalanced-learn pycaret statsmodels mlflow
from pycaret.regression import setup, ensemble_model
from sklearn.ensemble import BaggingRegressor
from catboost import CatBoostRegressor
!pip install catboost
import matplotlib.pyplot as plt
import seaborn as sns

drive.mount('/content/drive')

data = pd.read_csv('/content/drive/MyDrive/Project/student_maths.csv')

data.head()

data.nunique()

# Summary statistics
print(data.describe())

# Impute missing values
for col in data.columns:
    if data[col].isnull().sum() > 0:
        if data[col].dtype == 'object':
            # Impute categorical columns with the mode
            data[col].fillna(data[col].mode()[0], inplace=True)
        else:
            # Impute numerical columns with the median
            data[col].fillna(data[col].median(), inplace=True)

# Verify that there are no missing values
print(data.isnull().sum())

# Demographic Information
demographic_cols = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus']

plt.figure(figsize=(15, 10))
for i, col in enumerate(demographic_cols, 1):
    plt.subplot(2, 3, i)
    if col == 'age':
        sns.histplot(data[col], kde=True, palette="viridis")
    else:
        sns.countplot(data[col], palette="viridis")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'data' is your DataFrame containing the dataset
parental_cols = ['Medu', 'Fedu', 'Mjob', 'Fjob', 'guardian']

plt.figure(figsize=(15, 10))

for i, col in enumerate(parental_cols, 1):
    plt.subplot(2, 3, i)

    # Customize x-axis for 'Medu' and 'Fedu'
    if col in ['Medu', 'Fedu']:
        sns.countplot(x=data[col], palette="viridis", order=['1', '2', '3', '4'])
        plt.xticks([0, 1, 2, 3], ['1', '2', '3', '4'])
    else:
        sns.countplot(x=data[col], palette="viridis")

    plt.title(f'Distribution of {col}')

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

parental_cols = ['Medu', 'Fedu', 'Mjob', 'Fjob', 'guardian']

plt.figure(figsize=(15, 10))
for i, col in enumerate(parental_cols, 1):
    plt.subplot(2, 3, i)
    # Convert numerical columns to categorical for countplot
    if data[col].dtype in ['int64', 'float64']:
        data[col] = data[col].astype(str)
    sns.countplot(x=data[col], palette="viridis")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

academic_cols = ['traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid']

plt.figure(figsize=(15, 10))
for i, col in enumerate(academic_cols, 1):
    plt.subplot(2, 3, i)
    # Check if the column is numerical or categorical
    if data[col].dtype in ['int64', 'float64']:
        sns.histplot(data[col], kde=False, bins=20, color='skyblue')
        plt.xlabel(col)
        plt.ylabel('Count')
    else:
        sns.countplot(x=data[col], palette="cubehelix")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Extracurricular and Personal Activities
activities_cols = ['activities', 'nursery', 'higher', 'internet', 'romantic']

plt.figure(figsize=(15, 6))
for i, col in enumerate(activities_cols, 1):
    plt.subplot(2, 3, i)
    sns.countplot(data[col], palette="coolwarm")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming 'data' is your DataFrame containing the dataset
family_social_cols = ['famrel', 'freetime', 'goout']

plt.figure(figsize=(15, 6))

for i, col in enumerate(family_social_cols, 1):
    plt.subplot(1, 3, i)
    sns.countplot(x=data[col], palette="magma")

    # Set the x-axis labels to 1, 2, 3, 4
    plt.xticks(ticks=[0, 1, 2, 3, 4], labels=['1', '2', '3', '4', '5'])

    plt.title(f'Distribution of {col}')

plt.tight_layout()
plt.show()

# Family and Social Environment
family_social_cols = ['famrel', 'freetime', 'goout']

plt.figure(figsize=(15, 6))
for i, col in enumerate(family_social_cols, 1):
    plt.subplot(1, 3, i)
    sns.countplot(data[col], palette="magma")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

family_social_cols = ['famrel', 'freetime', 'goout']

plt.figure(figsize=(15, 6))
for i, col in enumerate(family_social_cols, 1):
    plt.subplot(1, 3, i)
    sns.histplot(data[col], kde=False, bins=20, color=sns.color_palette("magma")[0], edgecolor='black')
    plt.title(f'Distribution of {col}') # De-indent this line
    plt.xlabel(col)
    plt.ylabel('Count')
plt.tight_layout()
plt.show()

health_lifestyle_cols = ['Dalc', 'Walc', 'health', 'absences']

plt.figure(figsize=(15, 10))
for i, col in enumerate(health_lifestyle_cols, 1):
    plt.subplot(2, 2, i)
    # Check if the column is numerical or categorical
    if col == 'absences':
        # Use a color from the 'cividis' colormap instead of the name
        sns.histplot(data[col], kde=True, color=sns.color_palette("cividis")[0], bins=20)
        plt.xlabel(col)
        plt.ylabel('Count')
    else:
        sns.countplot(x=data[col], palette="cividis")
        plt.xlabel(col)
        plt.ylabel('Count')
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Academic Performance
performance_cols = ['G1', 'G2', 'G3']

plt.figure(figsize=(15, 6))
for i, col in enumerate(performance_cols, 1):
    plt.subplot(1, 3, i)
    sns.histplot(data[col], kde=True, palette="tab20")
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.show()

# Reason for School Choice
plt.figure(figsize=(10, 4))
sns.countplot(data['reason'], palette="inferno")
plt.title('Distribution of Reason for School Choice')
plt.tight_layout()
plt.show()

data.columns

"""

---

Setting up Environment in PyCaret"""

expA = RegressionExperiment()
target = 'G3'
ignore_A = []  # No features to ignore

expA.setup(data,
           target=target,
           ignore_features=ignore_A,
           train_size=0.8,  # 80% training, 20% testing
           preprocess=True,  # Enable preprocessing (optional based on need)
           categorical_features=['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
                                 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
                                 'nursery', 'higher', 'internet', 'romantic'],
           numeric_features=['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                             'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
                             'G1', 'G2'])

expB = RegressionExperiment()
target = 'G3'
ignore_B = ['G2']  # No features to ignore
# Setup the experiment
expB.setup(data,
           target=target,
           ignore_features=ignore_B,
           train_size=0.8,  # 80% training, 20% testing
           preprocess=True,  # Enable preprocessing (optional based on need)
           categorical_features=['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
                                 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
                                 'nursery', 'higher', 'internet', 'romantic'],
           numeric_features=['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                             'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
                             'G1'])

expC = RegressionExperiment()
target = 'G3'
ignore_C = ['G1', 'G2']  # No features to ignore
# Setup the experiment
expC.setup(data,
           target=target,
           ignore_features=ignore_C,
           train_size=0.8,  # 80% training, 20% testing
           preprocess=True,  # Enable preprocessing (optional based on need)
           categorical_features=['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob',
                                 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
                                 'nursery', 'higher', 'internet', 'romantic'],
           numeric_features=['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                             'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences'])

"""---
Compare Models

1. MODEL A
"""

Scenario_A = expA.compare_models(sort='RMSE')

best_A = expA.compare_models(include = ['rf','lightgbm', 'catboost','ada','gbr'])

# List of model names you want to create
model_names = ['rf', 'lightgbm', 'catboost', 'ada', 'gbr']

# Loop through each model, print a message, and create the model
create_model_A = []

for model in model_names:
    print(f"The below model is {model.upper()}")
    created_model = expA.create_model(model)
    create_model_A.append(created_model)

# Empty list to store tuned models
tuned_models_A = []

# Loop through each created model, print a message, and tune the model
for i, model in enumerate(create_model_A):
    model_name = model_names[i]
    print(f"Tuning the {model_name.upper()} model...")
    tuned_model = expA.tune_model(model)
    tuned_models_A.append(tuned_model)

from sklearn.metrics import mean_squared_error

# Retrieve the validation data from PyCaret, applying the same preprocessing
X_val = expA.get_config('X_test_transformed')  # Use transformed data
y_val = expA.get_config('y_test')

# Function to calculate RMSE (unchanged)
def calculate_rmse(model, X_val, y_val):
    predictions = model.predict(X_val)
    return mean_squared_error(y_val, predictions, squared=False)

# Placeholder for storing the final models (unchanged)
final_models_A = []

# Loop through each model, and check if tuning improved performance (unchanged)
for i, model in enumerate(create_model_A):
    # Calculate RMSE for original and tuned models
    original_rmse = calculate_rmse(model, X_val, y_val)
    tuned_rmse = calculate_rmse(tuned_models_A[i], X_val, y_val)

    if tuned_rmse < original_rmse:
        print(f"Tuned model for {model_names[i].upper()} was better and is retained.")
        final_models_A.append(tuned_models_A[i])
    else:
        print(f"Original model for {model_names[i].upper()} was retained.")
        final_models_A.append(model)

"""2. MODEL B"""

Scenario_B = expB.compare_models(sort='RMSE')

best_B = expB.compare_models(include = ['rf','lightgbm', 'catboost','ada','gbr'])

# List of model names you want to create
model_names = ['rf', 'lightgbm', 'catboost', 'ada', 'gbr']

# Loop through each model, print a message, and create the model
create_model_B = []

for model in model_names:
    print(f"The below model is {model.upper()}")
    created_model = expB.create_model(model)
    create_model_B.append(created_model)

# Empty list to store tuned models
tuned_models_B = []

# Loop through each created model, print a message, and tune the model
for i, model in enumerate(create_model_B):
    model_name = model_names[i]
    print(f"Tuning the {model_name.upper()} model...")
    tuned_model = expB.tune_model(model)
    tuned_models_B.append(tuned_model)

"""3. MODEL C"""

Scenario_C = expC.compare_models(sort='RMSE')

best_C = expC.compare_models(include = ['rf','lightgbm', 'catboost','ada','gbr'])

# List of model names you want to create
model_names = ['rf', 'lightgbm', 'catboost', 'ada', 'gbr']

# Loop through each model, print a message, and create the model
create_model_C = []

for model in model_names:
    print(f"The below model is {model.upper()}")
    created_model = expC.create_model(model)
    create_model_C.append(created_model)

# Empty list to store tuned models
tuned_models_C = []

# Loop through each created model, print a message, and tune the model
for i, model in enumerate(create_model_C):
    model_name = model_names[i]
    print(f"Tuning the {model_name.upper()} model...")
    tuned_model = expC.tune_model(model)
    tuned_models_C.append(tuned_model)

"""---

PLOT MODEL
"""

# Iterate over each tuned model and plot it individually
for model in tuned_models_A:
    plot1 = expA.plot_model(model)

for model in tuned_models_A:
    plot2 = expA.plot_model(model, plot = 'feature')

for model in tuned_models_A:
    plot2 = expA.plot_model(model, plot = 'learning')

for model in tuned_models_A:
    plot2 = expA.plot_model(model, plot = 'vc')

for model in tuned_models_A:
    plot2 = expA.plot_model(model, plot = 'manifold')

"""Ensemble

1. Bagging
"""

# Perform bagging ensemble with the tuned models
bagged_model_A = expA.ensemble_model(create_model_A[0], method='Bagging')

"""2. Boosting"""

# Perform boosting ensemble with the tuned models
boosted_model_A = expA.ensemble_model(create_model_A[0], method='Boosting')

"""3. Stacking"""

catboost = expA.create_model('catboost')
lightgbm = expA.create_model('lightgbm')
Ada = expA.create_model('ada')
gbr = expA.create_model('gbr')
rf = expA.create_model('rf')

stacker_A= expA.stack_models(estimator_list=[catboost,lightgbm, Ada , gbr, rf])

# Perform stacking ensemble with the tuned models
stacked_model_A = expA.stack_models(estimator_list=[catboost,lightgbm, Ada , gbr,rf ], meta_model=lightgbm)

print(stacked_model_A)

"""PREDICT MODEL"""

holdout_pred = expA.predict_model(stacker_A)

"""FINALISE MODEL"""

final_stacker = expA.finalize_model(stacker_A)

final_stacker

"""SAVE MODEL"""

expA.save_model(final_stacker, 'my_pycaret_regression')

"""LOAD MODEL"""

my_winning_regressor = load_model('my_pycaret_regression')

print(my_winning_regressor)

