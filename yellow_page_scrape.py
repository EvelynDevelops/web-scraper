import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_page(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"requests failure: {e}")
        return None

def extract_links(html):
    """Extract company detail page links from the search results page."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a.MuiLink-root.MuiLink-underlineNone")  
    links = [f"https://www.yellowpages.com.au{card['href']}" for card in cards]
    return links

def extract_company_details(html):
    """Extract detailed company information from the company detail page."""
    soup = BeautifulSoup(html, "html.parser")
    
    name = soup.select_one("a.listing-name").get_text(strip=True) if soup.select_one("a.listing-name") else "N/A"
    
    phone_div = soup.select_one("div.desktop-display-value")
    phone = phone_div.get_text(strip=True) if phone_div else "N/A"
    
    address_div = soup.select_one("div.listing-address.mappable-address.mappable-address-with-poi")
    address = address_div.get_text(strip=True) if address_div else "N/A"

    website = soup.select_one("a.contact-url")["href"] if soup.select_one("a.contact-url") else "N/A"
    
    return {"name": name, "phone": phone, "address": address, "website": website}


def construct_url(keyword, location):
    """Generate the search page URL based on the keyword and location."""
    base_url = f"https://www.yellowpages.com.au/search/listings?clue={keyword.replace(' ', '+')}&locationClue={location.replace(' ', '+')}"
    return base_url


def get_all_company_details(base_url):
    """Scrape company information across all pages."""
    all_company_details = []

    while base_url:
        # Fetch the current page HTML
        html = fetch_page(base_url, HEADERS)
        if not html:
            break

        # Extract all company detail page links on the current page
        company_links = extract_links(html)

        # Visit each company detail page and extract information
        for link in company_links:
            detail_html = fetch_page(link, HEADERS)
            if not detail_html:
                continue
            details = extract_company_details(detail_html)
            all_company_details.append(details)

        # Find the link to the next page
        soup = BeautifulSoup(html, "html.parser")
        next_page = None
        buttons = soup.select("a.MuiButtonBase-root.MuiButton-root.MuiButton-outlined.MuiButton-fullWidth[href]")

        # Filter out the button with the text "Next"
        for button in buttons:
            button_text = button.select_one("span.MuiButton-label").get_text(strip=True) if button.select_one("span.MuiButton-label") else ""
            if button_text == "Next":
                next_page = button
                break  # Exit the loop as soon as the "Next" button is found

        # Update base_url
        if next_page:
            base_url = f"https://www.yellowpages.com.au{next_page['href']}"
            print(f"Next page URL: {base_url}")
        else:
            base_url = None
            print("No 'Next' button found")

    return all_company_details



def save_to_csv(data, filename):
    """Save data to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "phone", "address", "website"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Data has been saved to {filename}")

# Set the keyword and location
keyword = "Earthmoving Repair"  # Search keyword
location = " "  # Search location
filename = "company_details.csv"  # CSV file name to save the data

# Construct the base_url
base_url = construct_url(keyword, location)

# Call the scraping function
company_data = get_all_company_details(base_url)

# Save the data to a CSV file
save_to_csv(company_data, filename)

print(f"Scraping completed. A total of {len(company_data)} company records have been scraped and saved to {filename}")
