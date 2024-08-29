# import pandas as pd
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import accuracy_score
# import joblib
#
# # Step 1: Read the dataset
# file_path = r'C:\Users\siddh\Desktop\Project\validation_set.xlsx'
# df = pd.read_excel(file_path)
#
# # Checking the first few rows to understand the structure
# print(df.head())
#
# # Separate features and target
# X = df.drop(['Val', 'Label'], axis=1)
# print(X)
# output_csv_path = r'C:\Users\siddh\Desktop\Project\features_only.csv'
# X.to_csv(output_csv_path, index=False)
# y = df['Val']
#
# # Step 2: Preprocess the data
# # Define which columns are categorical and binary
# binary_features = [
#     'has_caps', 'num_exclamation', 'has_urls', 'has_excessive_punctuation',
#     'has_all_caps_usage', 'has_urgency_phrases', 'has_misspelled_words',
#     'has_specific_keywords', 'has_attachments','has_suspicious_attachment'
# ]
#
# # Create a column transformer
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('bin', 'passthrough', binary_features)
#     ])
# print(preprocessor)
#
# # Step 3: Set up the model pipeline with GridSearchCV
# # Define the Random Forest classifier
# rf = RandomForestClassifier(random_state=42)
#
# # Define the parameter grid for GridSearchCV
# param_grid = {
#     'classifier__n_estimators': [50, 100, 200],
#     'classifier__max_depth': [None, 10, 20, 30],
#     'classifier__min_samples_split': [2, 5, 10],
#     'classifier__min_samples_leaf': [1, 2, 4]
# }
#
# # Create a pipeline
# pipeline = Pipeline(steps=[
#     ('preprocessor', preprocessor),
#     ('classifier', rf)
# ])
# print(pipeline)
#
# # Set up GridSearchCV
# grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')
#
# # Step 4: Train and evaluate the model
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # Fit GridSearchCV
# grid_search.fit(X_train, y_train)
#
# # Best parameters and best score
# print(f'Best parameters found: {grid_search.best_params_}')
# print(f'Best cross-validation accuracy: {grid_search.best_score_:.2f}')
#
# # Predict on the test set
# y_pred = grid_search.predict(X_test)
#
# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Test set accuracy: {accuracy:.2f}')
#
# # Save the model
# model_path = r'C:\Users\siddh\Desktop\Project\random_forest_model.pkl'
# joblib.dump(grid_search, model_path)
#
# # Load the model
# loaded_model = joblib.load(model_path)
#
# # Prepare the specific input for prediction
# # Example input
# input_data = pd.DataFrame([{
#     'has_caps': False,
#     'num_exclamation': 0,
#     'has_urls': False,
#     'has_excessive_punctuation': False,
#     'has_all_caps_usage': False,
#     'has_urgency_phrases': False,
#     'has_misspelled_words': False,
#     'has_specific_keywords': False,
#     'has_attachments': True,
#     'has_suspicious_attachment': False
# }])
# print(input_data)
#
# # Make a prediction using the loaded model (the pipeline includes the preprocessor)
# prediction = loaded_model.predict(input_data)
# print(f'Prediction for the input data: {prediction[0]}')











import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Read the dataset
file_path = r'C:\Users\siddh\Desktop\Project\validation_set.xlsx'
df = pd.read_excel(file_path)

# Checking the first few rows to understand the structure
print(df.head())

# Separate features and target
X = df.drop(['Val', 'Label'], axis=1)
y = df['Val']

# Step 2: Preprocess the data
# Define which columns are categorical and binary
binary_features = [
    'has_caps', 'num_exclamation', 'has_urls', 'has_excessive_punctuation',
    'has_all_caps_usage', 'has_urgency_phrases', 'has_misspelled_words',
    'has_specific_keywords', 'has_attachments', 'has_suspicious_attachment'
]
extension = ['attachement_extensions']
# Add dummy features to ensure ColumnTransformer is consistent
dummy_features = ['feature1', 'feature2', 'feature3', 'feature4']
X[dummy_features] = 0

# Update binary features list
binary_features.extend(dummy_features)

# Create a column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('bin', 'passthrough', binary_features)
    ]
)
print(preprocessor)

# Print the number of features the column transformer is intaking
num_features = len(preprocessor.transformers[0][2])
print(f'Number of features column transformer is intaking: {num_features}')

# Print the names of all features used in the column transformer
feature_names = preprocessor.transformers[0][2]
print(f'Feature names used in the column transformer: {feature_names}')

# Step 3: Set up the model pipeline with GridSearchCV
# Define the Random Forest classifier
rf = RandomForestClassifier(random_state=42)

# Define the parameter grid for GridSearchCV
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [None, 10, 20, 30],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Create a pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', rf)
])
print(pipeline)

# Set up GridSearchCV
grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')

# Step 4: Train and evaluate the model
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit GridSearchCV
grid_search.fit(X_train, y_train)

# Best parameters and best score
print(f'Best parameters found: {grid_search.best_params_}')
print(f'Best cross-validation accuracy: {grid_search.best_score_:.2f}')

# Predict on the test set
y_pred = grid_search.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Test set accuracy: {accuracy:.2f}')

# Save the model
model_path = r'C:\Users\siddh\Desktop\Project\random_forest_model.pkl'
joblib.dump(grid_search, model_path)

# Load the model
loaded_model = joblib.load(model_path)

# Prepare the specific input for prediction
# Example input
input_data = pd.DataFrame([{
    'has_caps': False,
    'num_exclamation': 0,
    'has_urls': False,
    'has_excessive_punctuation': False,
    'has_all_caps_usage': False,
    'has_urgency_phrases': False,
    'has_misspelled_words': False,
    'has_specific_keywords': False,
    'has_attachments': True,
    'has_suspicious_attachment': False,
    'feature1': 0,
    'feature2': 0,
    'feature3': 0,
    'feature4': 0
}])
print(input_data)

# Make a prediction using the loaded model (the pipeline includes the preprocessor)
prediction = loaded_model.predict(input_data)
print(f'Prediction for the input data: {prediction[0]}')

