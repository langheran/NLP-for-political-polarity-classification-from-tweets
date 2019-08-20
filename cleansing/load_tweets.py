import __init__
import config as conf
import pandas as pd
import os.path
import os
import chardet
import time
import numpy as np

# debug=True
debug=False

def decodeText(x):
	try:
		return bytes(x, 'CP1252').decode('utf-8')
	except UnicodeEncodeError:
		return None

def convertToFloat(x):
	try:
		return float(x)
	except ValueError:
		return 0

def byHDF(dfs):
	if (os.path.isfile('df_all.h5')):
		os.remove('df_all.h5')
	store = pd.HDFStore('df_all.h5')
	for df in dfs:
		# if (debug):
		# 	print(df.iloc[0]['filename'])
		concat_df = df[(df['text'] != None) & (df['text'] != "none")]
		# if(debug):
		# 	print(concat_df.columns)
		# 	print(concat_df.head())

		columns=['id', 'filename', 'posted_by', 'in_rply_to_screenname', 'created_at', 'retweet_count', 'text',
							   'agresivo', 'proactivo', 'provoto', 'reactivo',
							   'agresivo.1', 'proactivo.1', 'provoto.1', 'reactivo.1',
							   'agresivo.2', 'proactivo.2', 'provoto.2', 'reactivo.2']
		stringColumns = ['posted_by', 'in_rply_to_screenname']

		floatColumns = ['retweet_count',
				   'agresivo', 'proactivo', 'provoto', 'reactivo',
				   'agresivo.1', 'proactivo.1', 'provoto.1', 'reactivo.1',
				   'agresivo.2', 'proactivo.2', 'provoto.2', 'reactivo.2']

		for col in columns:
			if(col not in concat_df.columns):
				concat_df[col]=0

		for col in floatColumns:
			concat_df[col] = concat_df[col].apply(lambda x: convertToFloat(x))
			concat_df[[col]] = concat_df[[col]].fillna(0).astype(float)

		concat_df[['id']] = concat_df[['id']].fillna(0).astype(float)
		concat_df[['filename']] = concat_df[['filename']].astype(str)
		concat_df[['retweet_count']] = concat_df[['retweet_count']].fillna(0).astype(float)
		concat_df[['text']] = concat_df[['text']].astype(str)
		concat_df[['posted_by']] = concat_df[['posted_by']].astype(str)
		concat_df[['in_rply_to_screenname']] = concat_df[['in_rply_to_screenname']].astype(str)

		concat_df[['created_at']] = concat_df[['created_at']].astype(str)
		def convertToDate(row):
			try:
				if((row["created_at"]=="") or (row["created_at"]==0)):
					row["created_at"] = time.gmtime(0)
				else:
					row["created_at"] = pd.to_datetime(row["created_at"], infer_datetime_format=True)
			except:
				print(row["created_at"])
				raise
			return row
		concat_df = concat_df.apply(convertToDate, axis=1)
		concat_df = concat_df[columns]

		# concat_df[['id']] = concat_df[['id']].astype('int64')
		# concat_df.set_index(['id'], inplace=True)
		# with pd.option_context('display.max_colwidth', 255):
		if (debug):
			print(concat_df.columns)
			# print(concat_df.head())
		store.append('df', concat_df, data_columns=['text'], min_itemsize=250, nan_rep='nan', index=False)
	df = store.select('df')
	store.close()
	os.remove('df_all.h5')
	df['id'] = df['id'].astype(np.int64)
	df.set_index("id", inplace=True, drop=False)
	df = df.loc[~df.index.duplicated(keep='first')]
	return df


excel_file_list = []
for root, dirs, files in os.walk(conf.data_dir):
	for filename in files:
		if filename.endswith('.xlsx'):
			excel_file_list.append(os.path.join(root, filename))

excel_df_list = []
for excel_file in excel_file_list:
	# print(excel_file)
	df = pd.ExcelFile(excel_file).parse(skiprows=1, header=0, na_values=['NA'])
	while (df.iloc[0]['id'] == 'id'):
		df.drop(df.index[0], axis=0, inplace=True)
	df['text'] = df['text'].apply(lambda x: decodeText(x))
	df['filename'] = excel_file
	excel_df_list.append(df)

print("concat")
concat_df = byHDF(excel_df_list)
concat_df.to_pickle(os.path.join(conf.pickles_dir, "final.pickle"))
