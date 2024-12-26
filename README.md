# 📰 El País Opinion Scraper 

A robust web scraper that extracts and translates opinion articles from El País! 🇪🇸 ➡️ 🇬🇧

## ✨ Features

- Scrapes latest opinion articles from [El País](https://elpais.com/opinion/)
- Extracts article titles, content snippets, and images
- Translates Spanish titles to English automatically
- Analyzes word frequency in translated titles

## 🚀 Sample Output

```
Article #1
Title (ES): Felipe VI: la exigencia del bien común
Content (ES): El discurso del Rey homenajea a los afectados por la dana...

Article #2
Title (ES): El año de Sánchez
Content (ES): La buena marcha de la Economía compite en España...

[...]

Translated Titles (EN):
- Felipe VI: the demand for the common good
- The year of Sánchez
- Syria and the buts
- The government of the millionaires
- 'The three borders'

Most frequent words:
'the' → 7 occurrences
```

## 💻 Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/el-pais-scraper.git
cd el-pais-scraper
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Requirements

- Python 3.x
- Selenium
- Chrome WebDriver
- Internet connection

## 🚀 Usage

Run the scraper:
```bash
python src/main.py
```