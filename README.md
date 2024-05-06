Web Scraper for Franchise Supplier Network
This Python script is designed to scrape content from the Franchise Supplier Network website. It extracts text content, images, and URLs from various pages of the website and organizes them into folders for further analysis or storage.

Features
Scrapes content from multiple pages of the Franchise Supplier Network website.
Extracts text content, images, and URLs.
Organizes scraped content into folders based on the page endpoint.
Generates a summary report with the number of images and a list of URLs found on each page.
Uploads scraped content to an AWS S3 bucket for storage (optional).
Prerequisites
Before running the script, make sure you have the following installed:

Python 3.x
Required Python packages (requests, beautifulsoup4, boto3)
Installation
Clone the repository to your local machine:
bash
Copy code
git clone https://github.com/your-username/franchise-supplier-scraper.git
Navigate to the project directory:
bash
Copy code
cd franchise-supplier-scraper
Install the required Python packages:
bash
Copy code
pip install -r requirements.txt
Usage
Open the scraper.py file and update the AWS S3 credentials if you intend to upload the scraped content to an S3 bucket.
Run the script:
bash
Copy code
python scrapingsites.py

The script will start scraping content from the specified endpoints listed in the end_point_list. It will create folders for each endpoint and store the scraped content (text files, images, and summary reports) in their respective folders.
Once the scraping is complete, you can find the scraped content organized in the project directory.
Configuration
base_url: The base URL of the Franchise Supplier Network website.
headers: User-Agent header to mimic a web browser.
AWS S3 credentials: If you want to upload the scraped content to an S3 bucket, provide your AWS access key ID, secret access key, and bucket name as environment variables.
Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or create a pull request.
