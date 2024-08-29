import streamlit as st
import pandas as pd
from emailfeature import EmailFeatureExtractor
from spamclass1 import SpamClassifier
from mongo_utils import put_to_mongodb
from streamlit_option_menu import option_menu
from scrapeit import detect_phishing
from mongodb_utils import save_to_mongodb

# Load your pre-existing SpamClassifier
def classify_email(email_address, email_body, attachments):
    extractor = EmailFeatureExtractor()
    email_features = extractor.analyze_email(email_address, email_body, attachments)

    classifier = SpamClassifier([email_features])
    val, label = classifier.is_spam(email_features)
    return val, label, email_features

def display_result_with_color(result):
    if result == 'Phished':
        st.error("Detection Result: Danger ⛔️")
    elif result == 'Unknown':
        st.warning("Detection Result: Suspicious ⚠️")
    elif result == 'Legitimate':
        st.success("Detection Result: Safe ✅")
    else:
        st.error("Invalid detection result")

def phishing_detection_section():
    st.header('Phishing Website Detection')
    check_url = st.text_input('Enter the URL for classification:')
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0)

    if st.button('Check'):
        my_bar.text(progress_text)
        with st.spinner('Detecting...'):
            # Run the detection process
            result_dict = detect_phishing(check_url)
            phishing_label = result_dict['Result']
            display_result_with_color(phishing_label)
            save_to_mongodb(result_dict)

        # Close the spinner and complete the progress bar
        my_bar.empty()

def email_spam_detection_section():
    st.header('Email Spam Detection')

    email_address = st.text_input("Email Address")
    email_body = st.text_area("Email Body")
    attachments = st.file_uploader("Attachments", accept_multiple_files=True)

    if st.button("Classify"):
        if not email_address or not email_body:
            st.error("Please provide both an email address and body.")
        else:
            attachments_names = [attachment.name for attachment in attachments]
            val, label, email_features = classify_email(email_address, email_body, attachments_names)
            st.write(f"Classification Result: {label}")

            email_dict = {
                "email_address": email_address,
                "email_body": email_body,
                "attachments": attachments_names,
                "Val": val,
                "Label": label
            }
            email_dict.update(email_features["content_features"])
            email_dict.update(email_features["attachment_features"])
            put_to_mongodb(email_dict)

def home_section():
    st.header('CyberShield-AI')

    st.write("""
    CyberShield-AI is your ultimate guardian in the digital world, offering advanced solutions to protect against phishing and spam.
    Phishing attacks are fraudulent attempts to obtain sensitive information such as usernames, passwords, and credit card details by disguising as a trustworthy entity.
    Email spam, on the other hand, involves sending unsolicited messages, often commercial in nature, to a large number of recipients.
    Our platform leverages state-of-the-art machine learning and artificial intelligence techniques to accurately detect and mitigate these threats, ensuring a safer online experience.
    """)

    st.markdown(
        """
        <style>
        .card {
            padding: 20px;
            margin: 20px;
            background: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .card:hover {
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .card img {
            max-width: 100%;
            border-radius: 10px;
        }
        .background {
            background-image: url('https://example.com/background_image.jpg');
            background-size: cover;
            background-position: center;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    phishing_img = st.image("phishing-detection-with-Python.jpg", caption="Phishing URL detection involves identifying fraudulent websites designed to steal personal information by mimicking legitimate ones. Techniques for detection include heuristic-based methods, which analyze URL structures for suspicious patterns, and machine learning models trained on features such as URL length, domain age, and keyword usage. Blacklist-based methods reference known malicious URLs, while whitelist-based approaches ensure URLs belong to trusted sites. Advanced systems also utilize natural language processing to scrutinize website content and metadata. Effective phishing URL detection is crucial for cybersecurity, helping prevent identity theft, financial loss, and data breaches by safeguarding users from deceptive online schemes.")
    phishing_img = st.image("email_Spam.jpg",
                            caption="Email spam detection is crucial for maintaining secure and efficient communication. It involves identifying unsolicited and often harmful emails that clutter inboxes. Techniques include heuristic filters, which analyze email content for typical spam characteristics such as excessive links or common spam keywords. Machine learning models are trained on vast datasets to recognize subtle patterns indicative of spam. Bayesian filters use probabilistic approaches to classify emails based on word frequency. Additionally, blacklists of known spammers and reputation-based systems assess the sender's credibility. Effective spam detection enhances productivity, protects users from phishing and malware attacks, and ensures the integrity of email communication.")
    # Use markdown to render the rest of the HTML content
    st.markdown(
        """
        <div class="background">
            <div class="container">
                <div class="card">
                    <h3>Phishing URL Detection</h3>
                    <p>Detect if a URL is a phishing attempt.</p>
                    <a href="?page=phishing" class="stretched-link"></a>
                </div>
                <div class="card">
                    <h3>Email Spam Detection</h3>
                    <p>Detect if an email is spam.</p>
                    <a href="?page=email_spam" class="stretched-link"></a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    # Determine which page to show based on the query parameter
    query_params = st.query_params
    page = query_params.get("page", ["home"])[0]

    # Navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="CyberShield-AI",
            options=["Home", "Phished URL Detection", "Email Spam Detection"],
            icons=["house", "shield-shaded", "envelope"],
            menu_icon="cast",
            default_index=0 if page == "home" else (1 if page == "phishing" else 2),
        )

    # JavaScript to update the query parameters
    def update_query_params(page):
        st.write(
            f"""
            <script>
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            urlParams.set('page', '{page}');
            const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + urlParams.toString();
            window.history.pushState({page}, '', newUrl);
            </script>
            """,
            unsafe_allow_html=True,
        )

    # Update the query parameter based on the selected page
    if selected == 'Home':
        update_query_params("home")
        home_section()
    elif selected == 'Phished URL Detection':
        update_query_params("phishing")
        phishing_detection_section()
    elif selected == 'Email Spam Detection':
        update_query_params("email_spam")
        email_spam_detection_section()

if __name__ == '__main__':
    main()











# import streamlit as st
# import base64
# import pandas as pd
# import numpy as np
# from streamlit_option_menu import option_menu
# from scrapeit import detect_phishing  # Make sure to have the scrapeit module
# from mongodb_utils import save_to_mongodb  # Make sure to have the mongodb_utils module
#
# def display_result_with_color(result):
#     if result == 'Phished':
#         st.error("Detection Result: Danger ⛔️")
#     elif result == 'Unknown':
#         st.warning("Detection Result: Suspicious ⚠️")
#     elif result == 'Legitimate':
#         st.success("Detection Result: Safe ✅")
#     else:
#         st.error("Invalid detection result")
#
# def phishing_detection_section():
#     st.header('Phishing Website Detection')
#     check_url = st.text_input('Enter the URL for classification:')
#     progress_text = "Operation in progress. Please wait."
#     my_bar = st.progress(0)
#
#     if st.button('Check'):
#         my_bar.text(progress_text)
#         with st.spinner('Detecting...'):
#             # Run the detection process
#             result_dict = detect_phishing(check_url)
#             phishing_label = result_dict['Result']
#             display_result_with_color(phishing_label)
#             save_to_mongodb(result_dict)
#
#         # Close the spinner and complete the progress bar
#         my_bar.empty()
#
# def email_spam_detection_section():
#     st.header('Email Spam Detection')
#     st.write("This section is under construction.")
#
# def home_section():
#     st.header('CyberShield-AI')
#
#     st.write("""
#     CyberShield-AI is your ultimate guardian in the digital world, offering advanced solutions to protect against phishing and spam.
#     Phishing attacks are fraudulent attempts to obtain sensitive information such as usernames, passwords, and credit card details by disguising as a trustworthy entity.
#     Email spam, on the other hand, involves sending unsolicited messages, often commercial in nature, to a large number of recipients.
#     Our platform leverages state-of-the-art machine learning and artificial intelligence techniques to accurately detect and mitigate these threats, ensuring a safer online experience.
#     """)
#
#     # Use markdown to render the rest of the HTML content
#     st.markdown(
#         """
#         <div class="background">
#             <div class="container">
#                 <div class="card">
#                     <h3>Phishing URL Detection</h3>
#                     <p>Detect if a URL is a phishing attempt.</p>
#                     <a href="?page=phishing" class="stretched-link"></a>
#                 </div>
#                 <div class="card">
#                     <h3>Email Spam Detection</h3>
#                     <p>Detect if an email is spam.</p>
#                     <a href="?page=email_spam" class="stretched-link"></a>
#                 </div>
#             </div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#
# def set_background_image(image_url):
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("{image_url}");
#             background-size: cover;
#             background-position: center;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#
# def main():
#     # Set the background image
#     set_background_image("data:image/jpeg;base64,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")
#
#     # Determine which page to show based on the query parameter
#     query_params = st.experimental_get_query_params()
#     page = query_params.get("page", ["home"])[0]
#
#     # Navigation
#     with st.sidebar:
#         selected = option_menu(
#             menu_title="CyberShield-AI",
#             options=["Home", "Phished URL Detection", "Email Spam Detection"],
#             icons=["house", "shield-shaded", "envelope"],
#             menu_icon="cast",
#             default_index=0 if page == "home" else (1 if page == "phishing" else 2),
#         )
#
#     # JavaScript to update the query parameters
#     def update_query_params(page):
#         st.write(
#             f"""
#             <script>
#             const queryString = window.location.search;
#             const urlParams = new URLSearchParams(queryString);
#             urlParams.set('page', '{page}');
#             const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + urlParams.toString();
#             window.history.pushState({page}, '', newUrl);
#             </script>
#             """,
#             unsafe_allow_html=True,
#         )
#
#     # Update the query parameter based on the selected page
#     if selected == 'Home':
#         update_query_params("home")
#         home_section()
#     elif selected == 'Phished URL Detection':
#         update_query_params("phishing")
#         phishing_detection_section()
#     elif selected == 'Email Spam Detection':
#         update_query_params("email_spam")
#         email_spam_detection_section()
#
# if __name__ == '__main__':
#     main()

