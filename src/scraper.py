import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_el_pais_opinion(limit=5):
    driver = webdriver.Chrome()
  
    driver.get("https://elpais.com/opinion/")
    articles_elements = driver.find_elements(By.CSS_SELECTOR, "article")[:limit]
    articles_data = []


    for article_element in articles_elements:

        title_text, content_text, image_url = "", "", ""

        try:
            title_element = article_element.find_element(By.CSS_SELECTOR, "h2 a")

            title_text = driver.execute_script(
                "return arguments[0].textContent.trim()", 
                title_element
            )

        except:
            pass

        try:
            content_element = article_element.find_element(By.CSS_SELECTOR, "p")
            content_text = driver.execute_script(
                "return arguments[0].textContent.trim()", 
                content_element
            )
        except:
            pass

        try:
            image_url = article_element.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            pass
        articles_data.append({"title": title_text, "content": content_text, "img_url": image_url})

    driver.quit()

    return articles_data


def download_images(articles_data):
    article_index = 1
    for article in articles_data:
        image_url = article.get("img_url", "")
        if image_url:
            try:
                response = requests.get(image_url, timeout=5)
                if response.status_code == 200:
                    with open(f"images/article_{article_index}.jpg", "wb") as image_file:
                        image_file.write(response.content)
            except:
                pass
        article_index += 1
