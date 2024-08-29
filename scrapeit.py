# Import necessary modules
import pandas as pd
from main import FeatureExtractor
from webtuto.webtuto.spiders.urlscraper import Itemss
from selenium import webdriver
import numpy as np
import traceback
from sklearn.impute import SimpleImputer
import pickle
from sklearn.preprocessing import StandardScaler

# Load the saved models and scaler
with open('combined_model.pkl', 'rb') as f:
    saved_data = pickle.load(f)
    saved_cnn_model = saved_data['cnn_model']
    saved_rf_model = saved_data['rf_model']
    saved_scaler = saved_data['scaler']
    print("Model Loaded successfully")

# Create a webdriver instance
driver = webdriver.Chrome()

# Define function to check phishing
def check_phishing(features):
    try:
        # Extract features values
        features_values = [value if value is not None else np.nan for key, value in features.items() if key != 'Domain']
        # Reshape features values for prediction
        features_np = np.array(features_values, dtype=np.float32)
        features_np = features_np.reshape(1, -1)
        print("Original Features:", features_values)
        print("Preprocessed Features:", features_np)
        print("Number of features before combining:", features_np.shape[1])

        features_np_scaled = saved_scaler.transform(features_np)

        # Use stacked model for prediction
        cnn_predictions = saved_cnn_model.predict(features_np_scaled)

        # Concatenate predictions with original features
        combined_prediction = np.concatenate((features_np_scaled, cnn_predictions), axis=1)
        phishing_result = saved_rf_model.predict(combined_prediction)
        print("Stacked Model Predictions:", phishing_result)
        phishing_label = "Phished" if phishing_result == 1 else "Legitimate"
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        phishing_result = 0
        phishing_label = "Unknown"

    return phishing_result, phishing_label

# Define function to detect phishing
def detect_phishing(url):
    try:
        # Extract features from URL
        item = Itemss(url=url)
        features = FeatureExtractor.extract_features(item, driver)
        print("Extracted features:", features)
        # Check for phishing using extracted features
        phishing_result, phishing_label = check_phishing(features)

        result_dict = {
            'URL': url,
            'Have_IP': features.get('Have_IP', None),
            'Have_AT': features.get('Have_AT', None),
            'URL_Length': features.get('URL_Length', None),
            'Span_Url': features.get('Span_Url', None),
            'Url_Depth': features.get('Url_Depth', None),
            'Domain': features.get('Domain', None),
            'Dom_Extent': features.get('Domain_Length', None),
            'Path_Measure': features.get('Path_Length', None),
            'Subdomains': features.get('Num_Subdomains', None),
            'Title_Size': features.get('Title_Length', None),
            'Content_Size': features.get('Rawpage_Length', None),
            'Num_Redirects': features.get('Num_Redirects', None),
            'Redirection': features.get('Redirection', None),
            'HTTPS_Domain': features.get('HTTPS_Domain', None),
            'Tiny_URL': features.get('Tiny_URL', None),
            'Prefix_Suffix': features.get('Prefix_Suffix', None),
            'Domain_Age': features.get('Domain_Age', None),
            'Domain_End': features.get('Domain_End', None),
            'Iframe': features.get('Iframe', None),
            'Mouse_Over': features.get('Mouse_Over', None),
            'Right_Click': features.get('Right_Click', None),
            'Forwarding': features.get('Forwarding', None),
            'Num_Popups': features.get('Num_Popups', None),
            'Flag_Illegitimate_Time': features.get('Flag_IlLegitimate_Time', None),
            'Num_Third_Party_Clicks': features.get('Num_Third_Party_Clicks', None),
            'Final_Val': int(phishing_result),
            'Result': phishing_label
        }

    except Exception as e:
        print(f"Error: {e}")
        result_dict = {'URL': url, 'Result': 'Error'}

    return result_dict

# Main code
# try:
#     url = "https://www.google.com"
#     result = detect_phishing(url)
#     print(result)
# finally:
    driver.quit()
