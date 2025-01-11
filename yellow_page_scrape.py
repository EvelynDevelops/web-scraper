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
        print(f"请求失败: {e}")
        return None

def extract_links(html):
    """从搜索结果页面提取公司详情页链接"""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("a.MuiLink-root.MuiLink-underlineNone")  
    links = [f"https://www.yellowpages.com.au{card['href']}" for card in cards]
    return links

def extract_company_details(html):
    """从公司详情页提取公司详细信息"""
    soup = BeautifulSoup(html, "html.parser")
    
    name = soup.select_one("a.listing-name").get_text(strip=True) if soup.select_one("a.listing-name") else "N/A"
    
    phone_div = soup.select_one("div.desktop-display-value")
    phone = phone_div.get_text(strip=True) if phone_div else "N/A"
    
    address_div = soup.select_one("div.listing-address.mappable-address.mappable-address-with-poi")
    address = address_div.get_text(strip=True) if address_div else "N/A"

    website = soup.select_one("a.contact-url")["href"] if soup.select_one("a.contact-url") else "N/A"
    return {"name": name, "phone": phone, "address": address, "website": website}

def get_company_details(clue, location):
    """根据关键词和地域提取公司详细信息"""
    base_url = f"https://www.yellowpages.com.au/search/listings?clue={clue}&locationClue={location}"
    company_data = []

    while base_url:
        html = fetch_page(base_url, HEADERS)
        if not html:
            break

        # 提取当前页面的公司链接
        company_links = extract_links(html)

        # 访问每个公司详情页，提取信息
        for link in company_links:
            detail_html = fetch_page(link, HEADERS)
            if not detail_html:
                continue
            details = extract_company_details(detail_html)
            company_data.append(details)

        # 查找下一页链接
        soup = BeautifulSoup(html, "html.parser")
        next_page = soup.select_one(".pagination-next a")
        base_url = f"https://www.yellowpages.com.au{next_page['href']}" if next_page else None

    return company_data

def save_to_csv(data, filename):
    """将数据保存到 CSV 文件"""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "phone", "address", "website"])
        writer.writeheader()
        writer.writerows(data)
    print(f"数据已保存到 {filename}")

# set the keyword and location to search.
keyword = "Earthmoving Repair"
location = " "
filename = "company_details.csv"

company_data = get_company_details(keyword, location)
save_to_csv(company_data, filename)
