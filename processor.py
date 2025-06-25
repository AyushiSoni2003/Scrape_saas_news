import pandas as pd
from datetime import datetime
from textblob import TextBlob

class DataProcessor:
    def __init__(self):
        self.base_url = "https://www.thesaasnews.com"

    def analyze_sentiment(self, text):
        if not text:
            return "neutral"
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "positive"
        elif polarity < -0.2:
            return "negative"
        else:
            return "neutral"

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%B %Y')
        except ValueError:
            return None

    def categorize(self, cat_text):
        cat = cat_text.lower()
        if 'product' in cat:
            return 'Product Updates'
        elif 'saas' in cat:
            return 'SaaS News'
        elif 'ai' in cat or 'machine' in cat:
            return 'AI/ML'
        else:
            return 'Other'

    def clean_data(self, raw_data):
        df = pd.DataFrame(raw_data)

        # Step 1: Strip whitespace and clean strings
        text_cols = ['headline', 'company', 'round', 'software_category']
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

        # Step 2: Parse funding date
        df['funding_date'] = df['funding_date'].apply(self.parse_date)

        # Step 3: Fix incomplete URLs
        df['url'] = df['url'].apply(lambda x: self.base_url + x if x.startswith('/') else x)

        # Step 4: Categorize software category
        df['category_group'] = df['software_category'].apply(self.categorize)

        # Step 5: Show summary
        category_counts = df['category_group'].value_counts().to_dict()
        print("\nArticle Count by Category:")
        for cat, count in category_counts.items():
            print(f"- {cat}: {count}")

        return df
