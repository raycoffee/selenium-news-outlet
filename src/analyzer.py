def find_repeated_words(article_titles):
    word_frequency = {}
    
    for title in article_titles:
        for word in title.split():
            cleaned_word = "".join(char for char in word if char.isalnum()).lower()
            

            if cleaned_word:

                word_frequency[cleaned_word] = word_frequency.get(cleaned_word, 0) + 1

    frequent_words = {
        word: count 
        for word, count in word_frequency.items() 
        if count > 2
    }
    
    return frequent_words