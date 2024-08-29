import requests
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import logging
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, urlencode
import ipaddress
import whois
import urllib3
from datetime import datetime
from urllib.request import urlopen
import socket
import urllib.error
import dns.resolver
driver = webdriver.Chrome()

class FeatureExtractor:

    @staticmethod
    def extract_features(item, driver):
        features = {}
        features['Have_IP'] = FeatureExtractor.have_ip(item.url)
        features['Have_AT'] = FeatureExtractor.have_at_sign(item.url)
        features['URL_Length'] = len(item.url)
        features['Span_Url'] = FeatureExtractor.get_length(item.url)
        features['Url_Depth'] = FeatureExtractor.get_depth(item.url)
        features['Domain'] = FeatureExtractor.https_domain(item.url)
        features['Domain_Length'] = len(item.url.split('//')[-1].split('/')[0])
        features['Path_Length'] = len(item.url.split('//')[-1].split('/')) - 1
        features['Num_Subdomains'] = item.url.count('.') - 1
        features['Title_Length'] = len(item.title) if item.title else 0
        features['Rawpage_Length'] = len(item.rawpage) if item.rawpage else 0
        features['Num_Redirects'] = FeatureExtractor.redirection(item.url)
        features['Redirection'] = FeatureExtractor.count_redirects(item.url)
        features['HTTPS_Domain'] = FeatureExtractor.https_domain(item.url)
        features['Tiny_URL'] = FeatureExtractor.tiny_url(item.url)
        features['Prefix_Suffix'] = FeatureExtractor.prefix_suffix(item.url)
        features['Domain_Age'] = FeatureExtractor.domain_age(item.url)
        features['Domain_End'] = FeatureExtractor.domain_end(item.url)
        features['Iframe'] = FeatureExtractor.iframe(item.url)
        features['Mouse_Over'] = FeatureExtractor.mouse_over(item.url)
        features['Right_Click'] = FeatureExtractor.right_click(item.url)
        features['Forwarding'] = FeatureExtractor.forwarding(item.url)
        features['Num_Popups'] = FeatureExtractor.count_popups(item.url, driver)
        features['Flag_IlLegitimate_Time'] = FeatureExtractor.flag_illegitimate_time(item.url)
        features['Num_Third_Party_Clicks'] = FeatureExtractor.count_third_party_clicks(item.url)

        return features

    @staticmethod
    def get_dom(url):
        domain = urlparse(url).netloc
        if re.match(r"^www.", domain):
            domain = domain.replace("www.", "")
        return domain

    @staticmethod
    def get_length(url):  # done
        if len(url) < 54:
            length = 0
        else:
            length = 1
        return length

    @staticmethod
    def have_ip(url):
        try:
            ipaddress.ip_address(url)
            return 1
        except ValueError:
            return 0

    @staticmethod
    def have_at_sign(url):
        return 1 if "@" in url else 0

    @staticmethod
    def get_depth(url):
        s = urlparse(url).path.split('/')
        depth = 0
        for j in range(len(s)):
            if len(s[j]) != 0:
                depth = depth + 1
        return depth

    @staticmethod
    def count_redirects(url):
        try:
            response = requests.get(url, allow_redirects=True)
            num_redirects = len(response.history)
            if num_redirects > 3:
                return 1
        except:
            pass
        return 0

    @staticmethod
    def count_third_party_clicks(url):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            with webdriver.Chrome(options=chrome_options) as driver:
                driver.get(url)


                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                clickable_elements = driver.find_elements(By.XPATH, '//a')

                original_domain = urlparse(url).hostname
                third_party_domains = set()
                for element in clickable_elements:
                    href = element.get_attribute('href')
                    if href:
                        parsed_href = urlparse(href)
                        if parsed_href.hostname and parsed_href.hostname != original_domain:
                            third_party_domains.add(parsed_href.hostname)


                if third_party_domains:
                    return 1
                else:
                    return 0
        except Exception as e:

            return 0

    @staticmethod
    def flag_illegitimate_time(url, threshold_seconds=5):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=10)  #  timeout value
            end_time = time.time()
            if end_time - start_time > 3:
                return 1
        except Exception as e:
            pass
        return 0

    @staticmethod
    def count_popups(url, driver):
        try:
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            return 1
        except TimeoutException:
            return 0
        except WebDriverException as e:
            logging.error(f"WebDriverException occurred: {e}")
            return 0
        except NoSuchWindowException as e:
            logging.error(f"NoSuchWindowException occurred: {e}")
            return 0
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return 0

    @staticmethod
    def redirection(url):
        pos = url.find('://')
        if pos != -1:
            after_protocol = url[pos + 3:]
            count_slashes = after_protocol.count('//')
            return count_slashes
        else:
            return 0

    @staticmethod
    def https_domain(url):
        domain = urlparse(url).netloc
        return 1 if 'https' in domain else 0

    @staticmethod
    def tiny_url(url):
        shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                              r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                              r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                              r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                              r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                              r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                              r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                              r"tr\.im|link\.zip\.net"
        match = re.search(shortening_services, url)
        return 1 if match else 0

    @staticmethod
    def prefix_suffix(url):
        return 1 if '-' in urlparse(url).netloc else 0

    # @staticmethod
    # def dns_record(url):
    #     try:
    #         # Perform DNS resolution for the domain
    #         answers = dns.resolver.resolve(url, 'A')
    #         # If there are answers, it indicates the domain has DNS records
    #         if answers:
    #             return 1
    #         else:
    #             return 0
    #     except dns.resolver.NoAnswer:
    #         # If no DNS records are found
    #         return 0
    #     except dns.resolver.NXDOMAIN:
    #         # If the domain does not exist
    #         return 0
    #     except Exception as e:
    #         print(f"Error retrieving DNS record for {url}: {e}")
    #         return None
    #
    # @staticmethod
    # def web_traffic(url):
    #     try:
    #         url_netloc = urlparse(url).netloc
    #         rank = BeautifulSoup(urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url_netloc).read(),
    #                              "xml").find("REACH")['RANK']
    #         rank = int(rank)
    #     except (TypeError, urllib3.exceptions.HTTPError, socket.gaierror):
    #         return 1
    #
    #     if rank < 100000:
    #         return 1
    #     else:
    #         return 0

    @staticmethod
    def domain_age(url):
        try:
            domain = whois.whois(url)
            creation_date = domain.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(creation_date, datetime):
                age = (datetime.now() - creation_date).days
                return age
            else:
                return None
        except Exception as e:
            print(f"Error retrieving domain age: {e}")
            return None

    @staticmethod
    def domain_end(url):
        try:
            domain = whois.whois(url)
            expiration_date = domain.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            if isinstance(expiration_date, datetime):
                today = datetime.now()
                days_until_expiry = (expiration_date - today).days
                if (days_until_expiry / 30) < 6:
                    return 0
                else:
                    return 1
            else:
                return 1
        except Exception as e:
            print(f"Error retrieving domain expiration date: {e}")
            return 1

    @staticmethod
    def iframe(rawpage):
        if not rawpage:
            return 1
        if re.findall(r"<iframe>|<frameBorder>", rawpage):
            return 0
        else:
            return 1

    @staticmethod
    def mouse_over(rawpage):
        if not rawpage:
            return 1
        if re.findall("<script>.+onmouseover.+</script>", rawpage):
            return 1
        else:
            return 0

    @staticmethod
    def right_click(rawpage):
        if not rawpage:
            return 1
        if re.findall(r"event.button ?== ?2", rawpage):
            return 0
        else:
            return 1

    @staticmethod
    def forwarding(rawpage):
        if not rawpage:
            return 1
        if len(rawpage) <= 2:
            return 0
        else:
            return 1

