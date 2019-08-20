import pandas as pd
import codecs
import chardet

xls = pd.ExcelFile(r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\semanas\Week2\17Oct_a_30_Oct_2016\Lopez Obrador.xlsx')
df = xls.parse(skiprows=1, index_col=1, header = 0, na_values=['NA'])
print(df.iloc[0]['text'])
print(chardet.detect(df.iloc[0]['text'].encode()))

print(bytes(df.iloc[0]['text'], 'utf-8').decode('utf-8'))