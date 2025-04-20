from flask import Flask, render_template, request
from newsapi import NewsApiClient

app = Flask(__name__)
newsapi = NewsApiClient(api_key="dec2bc59018b454389d9448f1990ab7c")

@app.route('/', methods=['GET'])
def index():
    selected_category = request.args.get('category', '')
    selected_source = 'bbc-news'  # Default source when no category is selected

    if selected_category:
        # ✅ Don't use 'sources' with 'category' to avoid the ValueError
        headlines = newsapi.get_top_headlines(category=selected_category, country='us', page_size=100)
    else:
        headlines = newsapi.get_top_headlines(sources=selected_source, page_size=100)

    articles = headlines['articles']

    news_data = [
        {
            'title': article['title'],
            'desc': article['description'],
            'img': article['urlToImage']
        }
        for article in articles if article['urlToImage']  # Skip if image is missing
    ]

    # 👇 Categories for dropdown menu
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

    return render_template('index.html', news_data=news_data, categories=categories, selected_category=selected_category)

if __name__ == "__main__":
    from os import environ
    app.run(debug=False, host='0.0.0.0', port=int(environ.get("PORT", 5000)))