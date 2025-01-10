from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def parse_listing_selenium(keyword, location):
    """
    使用 Selenium 爬取 Yellow Pages Australia 的公司信息
    :param keyword: 搜索关键词
    :param location: 地点
    :return: 列表，包含公司信息字典
    """
    url = f"https://www.yellowpages.com.au/search/listings?clue={keyword}&location={location}"

    # 设置 Selenium 的 Chrome 浏览器选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/local/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(5) 

    scraped_results = []
    try:
        while True:
            listings = driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiPaper-root')]")
            if not listings:
                logging.warning("No listings found on this page.")
                break

            for listing in listings:
                try:
                    # 
                    business_name = listing.find_element(By.XPATH, ".//h3[contains(@class, 'MuiTypography-h3')]").text.strip()
                    
                    # more info buton (dynamic datas)
                    try:
                        more_info_button = listing.find_element(By.XPATH, ".//div[contains(@class, 'jGiCKf')]")
                        ActionChains(driver).move_to_element(more_info_button).click(more_info_button).perform()
                        time.sleep(2)  
                    except Exception:
                        logging.info("No 'More info' button for this listing.")

                    # 提取电话号码
                    try:
                        phone = listing.find_element(By.XPATH, ".//button[contains(@class, 'MuiButton-root')]//span[contains(@class, 'MuiButton-label') and text()]").text.strip()
                    except Exception:
                        phone = "N/A"

                    # 提取公司网站
                    try:
                        website = listing.find_element(By.XPATH, ".//a[contains(@class, 'MuiButton-root') and contains(@class, 'ButtonWebsite')]").get_attribute("href").strip()
                    except Exception:
                        website = "N/A"

                        
                    # 提取地址
                    try:
                        # 动态地址
                        dynamic_address = None
                        try:
                            dynamic_address = listing.find_element(By.XPATH, ".//div[contains(@class, 'jIlXXZ')]//p[contains(@class, 'MuiTypography-body2')]").text.strip()
                        except Exception:
                            dynamic_address = "N/A"

                        # 静态地址
                        static_address = None
                        try:
                            static_address = listing.find_element(By.XPATH, ".//div[contains(@class, 'bvRSwt')]//p[contains(@class, 'MuiTypography-body2')]").text.strip()
                        except Exception:
                            static_address = "N/A"

                        # 优先动态地址
                        address = dynamic_address if dynamic_address != "N/A" else static_address

                        logging.info(f"Extracted Address: {address}")
                    except Exception as e:
                        logging.warning(f"Error extracting address: {e}")
                        address = "N/A"



                    # 补充完整网址
                    if website and not website.startswith("http"):
                        website = f"https://www.yellowpages.com.au{website}"

                    scraped_results.append({
                        "business_name": business_name,
                        "phone": phone,
                        "website": website,
                        "address": address
                    })
                    logging.info(f"Extracted: {business_name}, {phone}, {website}, {address}")

                except Exception as e:
                    logging.warning(f"Error extracting listing: {e}")

            # 查找下一页按钮
            try:
                next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'pagination-next')]")
                next_button.click()
                time.sleep(3)  # 等待下一页加载
            except Exception:
                logging.info("No more pages.")
                break
    finally:
        driver.quit()

    return scraped_results

if __name__ == "__main__":
    keyword = "Earthmoving Repair"
    location = "Sydney"

    scraped_data = parse_listing_selenium(keyword, location)

    if scraped_data:
        # 保存数据到 CSV 文件
        filename = f"{keyword.replace(' ', '_')}-{location.replace(' ', '_')}-yellowpages.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['business_name', 'phone', 'website', 'address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
        logging.info(f"Data saved to {filename}")
    else:
        logging.warning("No data scraped.")
