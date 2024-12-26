import requests

def translate_html(html_text, source_lang="es", target_lang="en"):

    url = "https://google-translate113.p.rapidapi.com/api/v1/translator/html"

    headers = {
        "x-rapidapi-key": "24df69d9cdmsh5a9886acb0395d7p16d662jsn67348d36ccc9",
        "x-rapidapi-host": "google-translate113.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    payload = {
        "from": source_lang,
        "to": target_lang,
        "html": html_text
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        return response.json()
    except:
        return None

def translate_text(text, source_lang="es", target_lang="en"):

    result = translate_html(text, source_lang, target_lang)

    if result:
        return result["trans"]
    return text

def translate_titles(articles_data):
    translated_titles = []

    for article in articles_data:
        article_title = article.get("title", "")

        translated_result = translate_text(article_title, "es", "en")
        translated_titles.append(translated_result)
    return translated_titles