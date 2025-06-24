import pandas as pd
from datetime import datetime
import re

def cleaned_data(raw_data):
    # Step 1: Convert to DataFrame
    df = pd.DataFrame(raw_data)

    # Step 2: Strip whitespace and clean strings
    text_cols = ['headline', 'company','round', 'software_category']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

    # Step 3: Convert 'funding_date' to datetime
    def parse_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%B %Y')
        except ValueError:
            return None
        
    df['funding_date'] = df['funding_date'].apply(parse_date)

    #step4 : Ensure full URLs 
    base_url = "https://www.thesaasnews.com"
    df['url'] = df['url'].apply(lambda x: base_url +x if x.startswith('/') else x)

    # Step 5: Categorize articles (based on 'software_category')
    def categorize(row):
        cat = row['software_category'].lower()
        if 'product' in cat:
            return 'Product Updates'
        elif 'saas' in cat:
            return 'SaaS News'
        elif 'ai' in cat or 'machine' in cat:
            return 'AI/ML'
        else:
            return 'Other'

    df['category_group'] = df.apply(categorize, axis=1)

    #   Step 6: Count articles per category (optional summary)
    category_counts = df['category_group'].value_counts().to_dict()
    print("\n🧮 Article Count by Category:")
    for cat, count in category_counts.items():
        print(f"- {cat}: {count}")
    
    return df