from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from openpyxl import Workbook, load_workbook

# url can be added on information to take you to another site
url = 'https://empresite.eleconomista.es/Actividad/ALL-/PgNum-{}/'

# variable to list the urls of all the companies listed in the site
all_company_sites = []

# creating a session object
session = HTMLSession()

# defining a SoupStrainer which will allow BeautifulSoup to parse only the specified HTML tags and attributes
link_filter = SoupStrainer('span', {'class': 'email'})
link_selector = 'span.email'

# HTTP headers that are used to provide additional information to the server about the client making the request.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

def checking_if_site_has_email(url):
    # sending the request
    reply = session.get(url, headers=headers)

    soup = BeautifulSoup(reply.content, 'html.parser', parse_only=link_filter)

    email_tags = soup.select(link_selector)
    # Check if there are any email tags on the page
    if len(email_tags) == 0:
        return None
    else:
        emails = email_tags[0].text
        return emails

def input_data_into_excel(companies_name_and_link):
     # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Company details'
    # Add headings to the worksheet
    headings = ['Company name', 'Company site link', 'Company email']
    ws.append(headings)
    # Add company data to the worksheet
    for info in companies_name_and_link:
        data_input = [info[0], info[1], info[2]]
        ws.append(data_input)

    wb.save('Company_details.xlsx')


for i in range(0, 3):
    #scraping each of the company's 3 pages
    response = session.get(url.format(quote_plus(str(i+1))), headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    company_sites = soup.find_all('a', {'itemprop': 'url'})

    all_company_sites.append(company_sites)

number_of_companies_per_pages_entered = 0
company_name = []
links_to_sites = []
company_emails = []
company_with_email = []
number_of_companies_with_emails = 0
company_name_link = []
for lists in all_company_sites:
    number_of_companies_per_pages_entered += len(lists)
    for company in lists:
        company_name.append(company.text)
        links_to_sites.append(company['href'])
        one_company_email = checking_if_site_has_email(company['href'])
        company_name_link.append([company.text, company['href'], one_company_email])
   
with ThreadPoolExecutor() as executor:
    # Create a list of URLs to scrape
    urls = links_to_sites
    # Send requests and scrape links for each URL
    results = executor.map(checking_if_site_has_email, urls)
    
#call function to input data into excel spreadsheet
input_data_into_excel(company_name_link)

results = [r for r in results if r is not None]
all_emails = [email for page_emails in results for email in page_emails]

number_of_companies_with_emails = 0
for emails in all_emails:
    if emails:
        
        print(emails)
        number_of_companies_with_emails += 1
