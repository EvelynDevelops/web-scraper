import csv
import re
import requests
from bs4 import BeautifulSoup

def extract_emails_from_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)
        return list(set(emails)) 
    except requests.exceptions.RequestException as e:
        print(f"无法访问 {url}: {e}")
        return []

def update_csv_with_emails(input_file, output_file):
    updated_data = []

    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ["email"] 
        for row in reader:
            if row.get("website") and row["website"] != "N/A":
                print(f"正在提取 {row['website']} 的邮箱...")
                emails = extract_emails_from_website(row["website"])
                row["email"] = ", ".join(emails) if emails else "N/A"
            else:
                row["email"] = "N/A"
            updated_data.append(row)

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_data)
    print(f"更新完成，数据已保存到 {output_file}")

input_csv = "company_details.csv"
output_csv = "company_details_with_emails.csv"
update_csv_with_emails(input_csv, output_csv)
