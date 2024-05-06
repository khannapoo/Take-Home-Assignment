import requests
from bs4 import BeautifulSoup
import time
import os
import boto3
from botocore.exceptions import NoCredentialsError


class WebScraper:
    def __init__(self):
        self.base_url = "https://franchisesuppliernetwork.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.soup = None
        self.url = None
        self.end_point = None

    def _send_request(self):
        self.url = self.base_url + self.end_point + "/"
        print(self.url)
        response = self.session.get(self.url, headers=self.headers)
        # Add a delay between requests to avoid being flagged as a bot
        time.sleep(2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            self.soup = soup
        else:
            print("{status code:}".format(response.status_code))

    def _upload_aws_s3(self, folder_path):
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_KEY"))
        get_folder_files = os.listdir(folder_path)
        for file in get_folder_files:
            try:
                source_path = "{0}/{1}".format(folder_path, file)
                destination_path = '{0}/{1}'.format(folder_path, file)
                s3.upload_file(source_path, os.environ.get("BUCKET_NAME"), destination_path)
                print('Uploaded files')
            except NoCredentialsError:
                print("Credentials not available")

    def parse_content(self, end_point):
        self.end_point = end_point
        self._send_request()
        if self.soup:
            elements = self.soup.find_all(class_="contentside")
            images = self.soup.find_all('img')
            urls = [a['href'] for a in self.soup.find_all('a', href=True)]
            last_url_word = end_point.split("/")[-1]
            text_content = ""
            for element in elements:
                text_content += element.text.strip() + "\n"
            folder_path = os.path.join(os.getcwd(), last_url_word)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)  # Create folder if it doesn't exist

            if images:
                for img in images:
                    img_url = img['src']
                    img_name = os.path.basename(img_url)
                    img_path = os.path.join(folder_path, img_name)
                    try:
                        with open(img_path, 'wb') as img_file:
                            img_response = self.session.get(img_url, headers=self.headers)
                            time.sleep(2)
                            img_file.write(img_response.content)
                    except FileNotFoundError as e:
                        print("Error:", e)
                        continue

            text_file_path = os.path.join(folder_path, last_url_word + ".txt")
            if not os.path.exists(os.path.dirname(text_file_path)):
                os.makedirs(os.path.dirname(text_file_path))  # Create folder if it doesn't exist
            with open(text_file_path, "w", encoding="utf-8") as file:
                file.write(text_content)

            self._generate_summary(folder_path, images, urls)
            self._upload_aws_s3(folder_path)
        else:
            print("content not found for {}".format(self.url))

    def _generate_summary(self, folder_path, images, urls):
        summary_file_path = os.path.join(folder_path, "summary.txt")
        with open(summary_file_path, "w", encoding="utf-8") as summary_file:
            summary_file.write("Number of Images: {}\n".format(len(images)))
            summary_file.write("List of URLs:\n")
            for url in urls:
                summary_file.write("{}\n".format(url))
    

if __name__ == "__main__":
    end_point_list =[
        "assessment",
        "fsn-suppliers",
        "fsn-suppliers/financial-services",
        "fsn-suppliers/human-resources-services",
        "fsn-suppliers/marketing-services",
        "fsn-suppliers/operation-services",
        "fsn-suppliers/real-estate-services",
        "fsn-suppliers/legal-services",
        "supplier-memberships",
        "resources",
        "about",
        "contact",
        "supplier-memberships",
        "assessment",
        "featured-supplier/one-click-contractor",
        "featured-supplier/discover-my-franchise",
        "featured-supplier/pandologic",
        "featured-supplier/franfund",
        "featured-supplier/lineup-ai",
        "featured-supplier/profitkeeper",
        "featured-supplier/david-energy",
        "featured-supplier/small-software",
        "featured-supplier/integrated-digital-strategies",
        "featured-supplier/scorpion",
        "featured-supplier/proposify",
        "featured-supplier/careertopia-franchise-executive-search",
        "featured-supplier/thryv",
        "featured-supplier/two-ladders",
        "featured-supplier/map-ranks",
        "featured-supplier/answerconnect",
        "featured-supplier/showmaker-productions",
        "featured-supplier/clienttether",
        "featured-supplier/1huddle",
        "featured-supplier/elysium-marketing-group",
        "featured-supplier/specialized-accounting-services",
        "featured-supplier/franchisely",
        "featured-supplier/mfv-expositions",
        "featured-supplier/northeast-color",
        "featured-supplier/altus-commerce",
        "featured-supplier/bann-business-solutions",
        "featured-supplier/suttle-straus",
        "featured-supplier/frannet",
        "featured-supplier/rikor",
        "featured-supplier/seamless-health",
        "featured-supplier/orchatect",
        "featured-supplier/upfront",
        "featured-supplier/consumer-fusion",
        "featured-supplier/clicktecs",
        "featured-supplier/delightree",
        "featured-supplier/choice-local",
        "featured-supplier/location3",
        "featured-supplier/entrepreneur-magazine",
        "featured-supplier/fisher-zucker",
        "featured-supplier/franchise-elevator-pr",
        "featured-supplier/fishman-public-relations",
        "featured-supplier/nocap-sports",
        "featured-supplier/serviceminder",
        "featured-supplier/onaroll",
        "featured-supplier/leasecake",
        "featured-supplier/rallio",
        "#assessment-survey",
        "#ideation-session",
        "#supplier-audit-deep-dive",
        "assessment",
        "about",
        "contact",
        "fsn-members"
    ]
    scraper = WebScraper()
    for end_point in end_point_list:
        scraper.parse_content(end_point)
