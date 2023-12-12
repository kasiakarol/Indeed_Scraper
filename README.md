# Indeed_Scraper
The Indeed Job Scraper is a tool built with Python, Selenium, and Beautiful Soup. It automates the process of scraping job listings for Tester positions in Brno from Indeed.com. Every day, the program processes the data into a DataFrame, exports it to a CSV file, and sends this file via email. This project showcases automated web scraping, data handling, and scheduling using Windows Task Scheduler.

# Features
> Automated scraping of Indeed.com for specific job listings.
> Data parsing and organization into a structured DataFrame.
> CSV file generation for easy data review.
> Daily automated email dispatch with the latest job listings.

# Technologies Used
> Python
> Selenium
> Beautiful Soup
> Pandas
> SMTP for email sending

# Scheduling Information
This script is configured to run daily using Windows Task Scheduler. You can replicate this setup by following these steps:

> Open Task Scheduler in Windows.
> Create a new task and set the trigger to run daily at your preferred time.
> Set the action to execute the Python script.

# Handling Your 16-Digit Password:
To encrypt and securely store my 16-digit password required for Gmail, I created an environment variable. This variable is accessed in PyCharm using os or through a separate configuration file. 
