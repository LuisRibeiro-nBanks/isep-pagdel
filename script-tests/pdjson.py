import pandas as pd
import json


with open('response_1747773009.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


df_alerts = pd.json_normalize(data['alerts'])

df_alerts = df_alerts.explode('comments').reset_index(drop=True)

comments_df = pd.json_normalize(df_alerts['comments'].dropna()).add_prefix('comment_')

df_alerts = df_alerts.drop(columns=['comments'])
df_alerts = df_alerts.join(comments_df, how='left')


if 'location' in df_alerts.columns:
    df_alerts['location'] = df_alerts['location'].apply(lambda x: x if isinstance(x, dict) else {})
    location_df = pd.json_normalize(df_alerts['location']).add_prefix('location_')
    df_alerts = df_alerts.drop(columns=['location']).join(location_df)

print(df_alerts.head())

df_alerts.to_csv('alerts.csv', index=False, encoding='utf-8')
