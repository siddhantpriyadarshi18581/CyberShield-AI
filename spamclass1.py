from emailfeature import EmailFeatureExtractor  # Assuming this is your custom module for email feature extraction
import numpy as np
import joblib
import pandas as pd
class SpamClassifier:
    def __init__(self, features_list):
        self.features_list = features_list
        self.loaded_model = joblib.load('random_forest_model.pkl')
        # self.tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
        # self.num_features = joblib.load('num_features.pkl')  # Load the number of features

    def is_spam(self, email_features):
        content_features = email_features["content_features"]
        attachment_features = email_features["attachment_features"]

        print('Content Features:', content_features)
        print('Attachment Features:', attachment_features)

        # Extract and preprocess features for prediction
        content_values = [str(content_features[cv]) for cv in content_features]
        attachment_values = [str(attachment_features[av]) for av in attachment_features]

        print('Content Features Values:', content_values)
        print('Attachment Features Values:', attachment_values)

        # Combine content and attachment features
        combined_features = {**content_features, **attachment_features}

        # Add dummy features to ensure ColumnTransformer consistency
        combined_features['feature1'] = 0
        combined_features['feature2'] = 0
        combined_features['feature3'] = 0
        combined_features['feature4'] = 0

        print('Combined Features with Dummies:', combined_features)

        # Convert combined features into a DataFrame
        input = pd.DataFrame([combined_features])

        print(input)

        # Predict using the loaded model
        prediction = self.loaded_model.predict(input)
        val = int(prediction[0])
        print('Prediction:', val)

        # Determine label based on val
        label = "Spam" if val == 1 else "Not Spam"

        return val, label

    def classify_emails(self):
        classified_emails = []

        for email_features in self.features_list:
            val, label = self.is_spam(email_features)
            classified_email = {
                "email_address": email_features["email_address"],
                "email_body": email_features["email_body"],
                "attachments": ', '.join(email_features["attachments"]) if email_features["attachments"] else '',
                "Val": int(val),
                "Label": label
            }
            classified_email.update(email_features["content_features"])
            classified_email.update(email_features["attachment_features"])
            classified_emails.append(classified_email)

        return classified_emails

if __name__ == "__main__":
    # Define sample test data
    email_address = "ez|h$d11@zoho.com"
    email_body = """ You've won tkts to the EURO2004 CUP FINAL or å£800 CASH, to collect CALL 09058099801 b4190604, POBOX 7876150ppm"""
    attachment = ['docm']

    # Instantiate Email Feature Extractor
    extractor = EmailFeatureExtractor()

    # Extract features from sample test data
    email_features = extractor.analyze_email(email_address, email_body, attachment)

    # Create an instance of Spam Classifier with the extracted features
    classifier = SpamClassifier([email_features])

    # Classify the sample test email
    classified_emails = classifier.classify_emails()

    # Print the classification result
    for email in classified_emails:
        print("Email Address:", email["email_address"])
        print("Email Body:", email["email_body"])
        print("Attachments:", email["attachments"])
        print("Classification:", email["Label"])
