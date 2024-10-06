import datetime
import json

date_from_last_month = (datetime.date.today() - datetime.timedelta(days=31)).strftime("%Y/%m/%d")
response = requestNews(date_from_last_month)
top_100_most_popular_articles = None
if response['status'] == 'ok':
  print(response['totalResults'])
  top_100_most_popular_articles = response['articles']

with open('./data/_raw_data/apple-recent-news.json', 'w', encoding='utf-8') as file:
    json.dump(top_100_most_popular_articles, file, ensure_ascii=False, indent=4)