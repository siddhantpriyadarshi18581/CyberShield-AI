import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras import layers, models
import pickle

# Load and preprocess data
data = pd.read_excel(r"C:\Users\siddh\Desktop\Project\training_dataset (1).xlsx")

# Drop unnecessary columns
df = data.drop(['URL', 'Domain', 'Result'], axis=1)

# Handling missing values (if any)
df.fillna(0, inplace=True)

# Split the data into features (X) and target variable (y)
X = df.drop('Final_Val', axis=1)  # Features
y = df['Final_Val']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define your CNN architecture
model = models.Sequential([
    layers.Conv1D(128, 3, activation='relu', input_shape=(X_train_scaled.shape[1], 1)),
    layers.MaxPooling1D(2),
    layers.Conv1D(64, 3, activation='relu'),
    layers.MaxPooling1D(2),
    layers.Conv1D(32, 3, activation='relu'),
    layers.MaxPooling1D(2),
    layers.Flatten(),
    layers.Dense(64, activation='sigmoid'),
    layers.Dense(1)  # Output layer with one unit for regression
])

# Compile the CNN model
model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mae', 'accuracy'])

# Train the CNN model
history = model.fit(X_train_scaled, y_train, epochs=100, batch_size=32, validation_data=(X_test_scaled, y_test))

# Generate predictions from the CNN model for training and test data
cnn_train_predictions = model.predict(X_train_scaled)
cnn_test_predictions = model.predict(X_test_scaled)

# Concatenate CNN predictions with original features
X_train_combined = np.concatenate((X_train_scaled, cnn_train_predictions), axis=1)
X_test_combined = np.concatenate((X_test_scaled, cnn_test_predictions), axis=1)

# Train Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train_combined, y_train)

# Save the trained models and scaler using pickle
with open('combined_model.pkl', 'wb') as f:
    pickle.dump({'cnn_model': model, 'rf_model': rf_classifier, 'scaler': scaler}, f)

# Predict the value of X[4]
# Load the saved models and scaler
with open('combined_model.pkl', 'rb') as f:
    saved_data = pickle.load(f)
    saved_cnn_model = saved_data['cnn_model']
    saved_rf_model = saved_data['rf_model']
    saved_scaler = saved_data['scaler']

# Assume 'cnn_model' and 'rf_model' are your trained models
import joblib

# model.save('cnn_model.h5')
# joblib.dump(rf_classifier, 'rf_model.pkl')
# joblib.dump(scaler, 'scaler.pkl')

# from keras.models import load_model
# Preprocess X[4]
# Load the models
# cnn_model = load_model('cnn_model.h5')
# rf_model = joblib.load('rf_model.pkl')
# scaler = joblib.load('scaler.pkl')
X_4 = X.iloc[[2]]
X_4_scaled = saved_scaler.transform(X_4)
X_4_cnn_predictions = saved_cnn_model.predict(X_4_scaled.reshape(1, -1, 1))

# Concatenate predictions with original features
X_4_combined = np.concatenate((X_4_scaled, X_4_cnn_predictions), axis=1)

# Predict using the Random Forest model
X_4_prediction = saved_rf_model.predict(X_4_combined)
print("Prediction for X[4]:", X_4_prediction)
