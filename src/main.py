from scraper import scrape_el_pais_opinion, download_images
from translator import translate_titles
from analyzer import find_repeated_words

def main():

    articles_data = scrape_el_pais_opinion(5)


    #Title, Content, Image URL generated
    article_number = 1

    for article_info in articles_data:

        print(f"\nArticle #{article_number}")
        print(f"Title (ES): {article_info['title']}")
        print(f"Content (ES): {article_info['content']}")
        article_number += 1


    download_images(articles_data)
    #Images download and saved in images/[article_x].jpg

    translated_titles = translate_titles(articles_data)

    article_number = 1
    for translated_title in translated_titles:
        print(f"\nArticle #{article_number} Title (EN): {translated_title}")
        article_number += 1

    repeated_words = find_repeated_words(translated_titles)
    for word, occurrences in repeated_words.items():
        print(f"'{word}' 👉 {occurrences} occurrences")



if __name__ == "__main__":
    main()
