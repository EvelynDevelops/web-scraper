# Yellow Pages Company Scraper

This script is a web scraper designed to collect detailed information about companies listed on Yellow Pages Australia. The script searches for companies based on specified keywords and locations, extracts relevant details, and saves the information into a CSV file.

## Features

1. **Search Functionality**: The scraper generates a search URL based on the specified keyword and location.
2. **Pagination Handling**: Automatically navigates through multiple pages of search results.
3. **Data Extraction**: Extracts company name, phone number, address, and website from each company's detail page.
4. **CSV Export**: Saves the scraped data into a CSV file for further use.

---

## Requirements

### Python Packages
The script requires the following Python packages:
- `requests`: For fetching web pages.
- `beautifulsoup4`: For parsing and extracting data from HTML.
- `csv`: For saving the scraped data into a file.

### Installation
To install the required Python packages, run:
```bash
pip install requests beautifulsoup4
```

---

## How to Use

### Step 1: Configure Search Parameters
Edit the following variables in the script to specify the search criteria:
- `keyword`: The keyword for the search (e.g., `"Earthmoving Repair"`).
- `location`: The location to search in (e.g., `"Sydney"`).
- `filename`: The name of the output CSV file (e.g., `"company_details.csv"`).

### Step 2: Run the Script
Run the script using Python:
```bash
python script_name.py
```
Replace `script_name.py` with the filename of the script.

### Step 3: View the Output
After the script completes execution, the results will be saved in the specified CSV file. The CSV will contain the following columns:
- `name`: Company name
- `phone`: Phone number
- `address`: Company address
- `website`: Company website

---

## Code Overview

### Key Functions
1. **fetch_page(url, headers)**
   - Fetches the HTML content of a web page.
   - Handles HTTP errors and exceptions.

2. **extract_links(html)**
   - Extracts links to company detail pages from the search results.

3. **extract_company_details(html)**
   - Extracts detailed information about a company (name, phone, address, website) from its detail page.

4. **construct_url(keyword, location)**
   - Constructs a search URL based on the specified keyword and location.

5. **get_all_company_details(base_url)**
   - Handles pagination, extracts links from all result pages, and collects company details.

6. **save_to_csv(data, filename)**
   - Saves the collected data into a CSV file.

---

## Example Output
If you search for `Earthmoving Repair` with no specific location, the output CSV might look like this:

| name                           | phone        | address                          | website                       |
|--------------------------------|--------------|----------------------------------|-------------------------------|
| Company A                      | 123-456-7890 | 123 Street, City, State          | http://www.company-a.com      |
| Company B                      | 098-765-4321 | 456 Avenue, City, State          | http://www.company-b.com      |

---

## Notes

1. **Pagination**: The script automatically handles multiple pages of search results, as long as the "Next" button is available.
2. **Rate Limiting**: To avoid being blocked, consider adding a delay (e.g., `time.sleep(2)`) between requests.
3. **Incomplete Data**: If some fields (e.g., phone or address) are missing for a company, the script will save "N/A" in those fields.
4. **Website Changes**: The script relies on the current structure of Yellow Pages Australia. If the website structure changes, updates to the script may be required.

---

## License
This script is for personal and educational use only. Scraping websites without permission may violate their terms of service. Use this script responsibly.

