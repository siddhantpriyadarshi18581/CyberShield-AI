import re
import nltk
import email
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class EmailFeatureExtractor:
    def __init__(self,punctuation_threshold=3):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.vectorizer = TfidfVectorizer()
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.punctuation_threshold = punctuation_threshold


    def preprocess_text(self, text):
        text = re.sub('<.*?>', '', text)
        text = re.sub('[^a-zA-Z]', ' ', text).lower()
        words = nltk.word_tokenize(text)
        words = [self.stemmer.stem(w) for w in words if w not in self.stop_words]
        text = ' '.join(words)
        return text

    def extract_content_features(self, email_body):
        text_content = self.preprocess_text(email_body)
        num_excessive_punctuation = len(re.findall(r'[!?.]{3,}', email_body))

        features = {
            "has_caps": any(word.isupper() for word in text_content.split()),
            "num_exclamation": email_body.count("!"),
            "has_urls": bool(re.findall(r"(http|ftp|https):\/\/\S+", email_body)),
            "has_excessive_punctuation": num_excessive_punctuation >= self.punctuation_threshold,
            "has_all_caps_usage": email_body.isupper(),
            "has_urgency_phrases": any(phrase in email_body.lower() for phrase in ["urgent", "act now", "limited time"]),
            "has_misspelled_words": self.has_misspelled_words(email_body),
            "has_specific_keywords": self.has_specific_keywords(email_body)
        }
        return features

    def extract_attachment_features(self, attachments):
        attachment_types = []
        attachment_extensions = ""
        suspicious_extensions = {"jar", "lnk", "ps1", "exe","rar"}
        has_suspicious_attachment = False

        for attachment in attachments:
            filename = attachment.split('.')[-1]
            #attachment_types.append('application/octet-stream')
            attachment_extensions = attachment_extensions + filename
            if filename in suspicious_extensions:
                has_suspicious_attachment = True

        has_attachments = len(attachments) > 0
        #has_multiple_attachments = len(attachment_types) > 1
        extension_status= {"exe", "zip", "rar", "jar", "lnk", "vbs","ps1","docm"}
        attachment_features = {
            "has_attachments": has_attachments,
            #"attachment_types": attachment_types,
            # "attachment_extensions": attachment_extensions,
            "has_suspicious_attachment": has_suspicious_attachment
            #"has_multiple_attachments": has_multiple_attachments,
        }
        return attachment_features

    # def scan_attachment(self, attachment):
    #         return True

    def has_misspelled_words(self, text):
        misspelled_words = {"amzon", "barbee", "lerning","shooping","deels","seal","indla","saeson"}
        words = nltk.word_tokenize(text.lower())
        return any(word in misspelled_words for word in words)

    def has_specific_keywords(self, text):
        specific_keywords = {"urgent", "free", "discount", "offer", "guaranteed","sales","prizes","cashback", "scheme"}
        words = nltk.word_tokenize(text.lower())
        return any(word in specific_keywords for word in words)

    def analyze_email(self, email_address, email_body, attachments=None):
        content_features = self.extract_content_features(email_body)
        #header_features = self.extract_header_features(email_address)
        attachment_features = self.extract_attachment_features(attachments or [])

        return {
            "email_address": email_address,
            "email_body": email_body,
            "attachments": attachments,
            "content_features": content_features,
            "attachment_features": attachment_features
        }

def save_features():
    extractor = EmailFeatureExtractor()
    email_address = ""
    email_body = ""
    attachment = []
    email_features = extractor.analyze_email(email_address, email_body, attachments=attachment)

    return email_features

if __name__ == "__main__":
    features = save_features()
    with open('email_features.py', 'w') as f:
        f.write(f"email_features = {features}")
# if __name__ == "__main__":
#     extractor = EmailFeatureExtractor()
#
#     email_address = "example@example.com"
#     email_body = "Dear recipient, please click on the link to claim your free offer!"
#     attachment = "SampleAttachment.pdf"
#
#     email_features = extractor.analyze_email(email_address, email_body, attachments=[attachment])
#
#     content_features = email_features["content_features"]
#     header_features = email_features["header_features"]
#     attachment_features = email_features["attachment_features"]
#
#     is_spam = content_features["has_specific_keywords"] or content_features["has_excessive_punctuation"]
#
#     if is_spam:
#         print(f"The email address {email_address} is likely spam.")
#     else:
#         print(f"The email address {email_address} is not spam.")
#
# with open("email_features.csv", "w", newline="") as csvfile:
#         fieldnames = ["Feature", "Value"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#         writer.writeheader()
#         for feature, value in content_features.items():
#             writer.writerow({"Feature": feature, "Value": value})
#         for feature, value in header_features.items():
#             writer.writerow({"Feature": feature, "Value": value})
#         for feature, value in attachment_features.items():
#             writer.writerow({"Feature": feature, "Value": value})


# Usage example:
# Create an instance of the EmailFeatureExtractor class
# extractor = EmailFeatureExtractor()
# Extract features from an email
# content_features = extractor.extract_content_features(email)
# header_features = extractor.extract_header_features(email)
# attachment_features = extractor.extract_attachment_features(email)



# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
#
# class EmailTokenizer:
#
#    def extract_features(email):
#         features = {}
#         text_content = EmailTokenizer.preprocess_text(email.body)
#         features["has_caps"] = any(word.isupper() for word in text_content.split())
#         features["num_exclamation"] = text_content.count("!")
#         features["has_urls"] = bool(re.findall(r"(http|ftp|https):\/\/\S+", text_content))
#         # Header analysis (replace with your logic for header checks)
#         features["is_sender_suspicious"] = "suspicious_domain" in email.sender  # Replace with actual check
#         # Attachment analysis (basic check, replace for advanced analysis)
#         features["has_attachments"] = len(email.attachments) > 0
#         return features
#
#    def preprocess_text(text):
#      text = text.lower()
#      text = re.sub(r'[^\w\s]', '', text)
#      stop_words = ["a", "an", "the"]
#      text = " ".join([word for word in text.split() if word not in stop_words])
#      return text
#
#    def to_lower(word):
#      result = word.lower()
#      return result
#
#    def remove_stop_words(words):
#      result = [i for i in words if i not in ENGLISH_STOP_WORDS]
#      return result
#
#    def remove_hyperlink(word):
#      return re.sub(r"http\S+", "", word)
#
#    def clean_text(text):
#        # Remove HTML tags
#        text = re.sub('<.*?>', '', text)
#        # Remove non-alphabetic characters and convert to lowercase
#        text = re.sub('[^a-zA-Z]', ' ', text).lower()
#        # Tokenize the text
#        words = nltk.word_tokenize(text)
#        # Remove stopwords
#        words = [w for w in words if w not in stopwords.words('english')]
#        # Stem the words
#        stemmer = PorterStemmer()
#        words = [stemmer.stem(w) for w in words]
#        # Join the words back into a string
#        text = ' '.join(words)
#        return text
#
#    def message_cleaner(sentence):
#        """
#        Function message_cleaner clean the text using typical Natural Language Processing
#        (NLP) steps.
#        Steps include: Lemmatization, removing stop words, removing punctuations
#        Args:
#            sentence (str): The uncleaned text.
#        Returns:
#            str: The cleaned text.
#        """
#        # Create the Doc object named `text` from `sentence` using `nlp()`
#        text = nlp(sentence)
#        # Lemmatization - remove the lemmas -PRON-
#        text = [token.lemma_ for token in text if token.lemma_ != "-PRON-"]
#        # Remove stop words
#        text = [token for token in text if token not in stopWords]
#        # Remove punctuations
#        text = [token for token in text if token not in punctuations]
#        # Use the .join() method on text to convert string
#        text = " ".join(text)
#        # Use re.sub() to substitute multiple spaces or dots`[\.\s]+` to single space `' '`
#        text = re.sub('[\.\s]+', ' ', text)
#
#        # Return the cleaned text
#        return text
#
#    df['num_words'] = df['text'].apply(lambda x: len(nltk.word_tokenize(x)))
#    df['num_characters'] = df['text'].apply(len)
#    df['num_sentences'] = df['text'].apply(lambda x: len(nltk.sent_tokenize(x)))
# def extract_header_features(self, email_message):
#     msg = email.message_from_string(email_message)
#     sender = msg.get("From")
#     recipient = msg.get("To")
#
#     if recipient:
#         recipient_domain = recipient.split('@')[-1]
#         is_internal_recipient = self.is_internal_recipient(recipient)
#     else:
#         # Handle case where recipient is None
#         recipient_domain = None
#         is_internal_recipient = False
#
#     if sender:
#         sender_domain = sender.split('@')[-1]
#         is_valid_sender_domain = self.is_valid_domain(sender_domain)
#         sender_name, sender_email = email.utils.parseaddr(sender)
#         sender_name = sender_name.strip()
#         sender_email = sender_email.strip('<>')
#         is_consistent_sender = self.has_inconsistent_sender(sender_email)
#         is_suspicious_sender = self.is_suspicious_sender(sender_email)
#     else:
#         is_valid_sender_domain = False
#         sender_name = None
#         sender_email = None
#         is_consistent_sender = False
#         is_suspicious_sender = False
#
#     header_features = {
#         "is_valid_sender_domain": is_valid_sender_domain,
#         "is_internal_recipient": is_internal_recipient,
#         "is_consistent_sender": is_consistent_sender,
#         "is_suspicious_sender": is_suspicious_sender
#     }
#     return header_features
#
# def is_suspicious_sender(self, sender_email):
#
#         suspicious_domains = {"suspici0us_domain.com", "example.co.in","secure-login.net", "beispiel.de","important-documents.org "}
#         domain = sender_email.split('@')[-1]
#         return domain in suspicious_domains
#
# def is_internal_domain(self, domain):
#     internal_domains = {"bnmit.in", "gmail.com", "college.org", "dept.edu", "institution.ac.in"}
#     return domain in internal_domains
#
# def is_internal_recipient(self, recipient_email):
#
#     internal_domains = {"bnmit.in", "gmail.com","college.org","dept.edu","institution.ac.in"}
#     domain = recipient_email.split('@')[-1]
#     return domain in internal_domains
#
# def has_invalid_domain(self, sender_email):
#
#     invalid_domains = {"invalid.com", "badsender.org","example.com"}
#     domain = sender_email.split('@')[-1]
#     return domain in invalid_domains
#
# def has_inconsistent_sender(self, sender_email):
#
#     display_name, sender_address = email.utils.parseaddr(sender_email)
#     sender_address = sender_address.strip('<>')
#     return display_name.lower() != sender_address.lower()

