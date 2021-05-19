import pandas as pd
import csv

new_df = pd.DataFrame(columns=['idx', 'URL', 'star', 'content'])
# 저장 파일 open
for i in range(1, 8):
    df = pd.read_csv('./reviews/test_shuffle' + str(i) + '.csv', encoding='utf-8')
    del df['Unnamed: 0']
    df = df.sample(frac=1).reset_index(drop=True)
    df = df[:100]
    new_df = new_df.append(df, ignore_index=True)

new_df.to_csv('./reviews/last_shuffle.csv', encoding='utf-8')