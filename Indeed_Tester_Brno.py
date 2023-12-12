from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os

driver_path = r"C:\DriversSel\chromedriver-win64\chromedriver.exe"

# Create a Service instance with the specified driver path
service = Service(executable_path=driver_path)

# Create ChromeOptions instance
chrome_options = Options()

# Create the Chrome webdriver instance with options and the Service instance
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(15)
driver.get("https://cz.indeed.com/")

# Wait for the cookie consent button to be clickable
cookie_accept = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//button[@id='onetrust-accept-btn-handler']")))

# Click the cookie consent button
cookie_accept.click()

# Making sure the search button exists
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "text-input-what")))
time.sleep(2)

# Inserting job position
job_position = "Tester"
search_box = driver.find_element(By.ID, "text-input-what")
search_box.send_keys(job_position)

# Inserting job location
job_location = "Brno"  # "Česko"
location_box = driver.find_element(By.ID, "text-input-where")
location_box.send_keys(job_location)

# Clicking Enter
act = ActionChains(driver)
act.send_keys(Keys.ENTER).perform()

df = pd.DataFrame(columns=['Job title', 'Location', 'Company', 'Posting date', 'Salary', 'URL'])

while True:

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.css-5lfssm.eu4oa1w0')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    jobs = soup.find_all('li', class_='css-5lfssm eu4oa1w0')

    for job in jobs:
        try:
            job_title = job.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').find('span').text.strip()
            location = job.find('div', {'data-testid': "text-location"}).text.strip()
            company_name = job.find('span', {'data-testid': "company-name"}).text.strip()
            posting_date = job.find('span', class_='date').text.strip()
            days_list = re.findall(r'\d+', posting_date)
            days = days_list[0] if days_list else 'Unknown'
            if days == '1':
                posting_days = f"{days} den"
            else:
                posting_days = f"{days} dny"
            link = 'https://cz.indeed.com' + job.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
            salary = job.find('div', class_='metadata salary-snippet-container').text.strip() if job.find('div', class_='metadata salary-snippet-container') else 'Not specified'

            new_row = pd.DataFrame([[job_title, location, company_name, posting_days, salary, link]],
                                   columns=['Job title', 'Location', 'Company', 'Posting date', 'Salary', 'URL'])
            df = pd.concat([df, new_row], ignore_index=True)
        except:
            pass

    # Handling pagination
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next Page']")))
        next_button.click()
        WebDriverWait(driver, 10).until(
            EC.staleness_of(next_button))  # Wait for the old button to go stale after clicking

    except (NoSuchElementException, TimeoutException):
        print("No more pages to process.")
        break

# Sorting the dataframe by posting date
df['Posting date'] = df['Posting date'].apply(lambda x: x[:2].strip())


def integer(x):
    try:
        return int(x)
    except:
        return x


df['Posting date2'] = df['Posting date'].apply(integer)
df.sort_values(by=['Posting date2'], inplace=True)

df = df[['Job title', 'Location', 'Company', 'Posting date', 'Salary', 'URL']]

file_path = 'C:/Users/kasia/OneDrive/Documents/Webscraping_exercise/jobs_Brno2.csv'  # Can be adjusted by the user
df.to_csv(file_path, index=False)

##################################################################################

# Sending email from Python with the attachment created in the above part of code

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Sender email and password retrieved from the Environment Variable
email = 'kasia.studying.python@gmail.com'
password = os.environ.get('gmail_16digits_password')

# Recipient email
send_to_email = 'kasia.studying.python@gmail.com'

# Setup the MIME
message = MIMEMultipart()
message['From'] = email
message['To'] = send_to_email
message['Subject'] = 'New Testers Jobs on Indeed'

# Attach the body with the msg instance
message.attach(MIMEText('The newest job offers for Brno attached', 'plain'))

# Open the file as binary mode
binary_file = open(file_path, 'rb')
payload = MIMEBase('application', 'octet-stream', Name=file_path)
payload.set_payload((binary_file).read())

# Encode the payload using encode_base64
encoders.encode_base64(payload)

# Add header with the file name
payload.add_header('Content-Disposition', 'attachment', filename=file_path)
message.attach(payload)

# Start SMTP session
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Log in to the server using email and app password
server.login(message['From'], password)

# Send the email
server.sendmail(message['From'], message['To'], message.as_string())

# Terminate the SMTP session
server.quit()

print("Email sent successfully!")

