import pandas as pd
import os.path
import os

working_dir = r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\semanas'  # semanas path

excel_file_list = []
for root, dirs, files in os.walk(working_dir):
	for filename in files:
		if filename.endswith('.xlsx'):
			excel_file_list.append(os.path.join(root, filename))

csv_file_list = []
for root, dirs, files in os.walk(working_dir):
	for filename in files:
		if filename.endswith('.csv'):
			csv_file_list.append(os.path.join(root, filename))

final = []
excel_df_list = [pd.ExcelFile(file).parse(skiprows=1, index_col=1, header=0, na_values=['NA']) for file in excel_file_list]
# excel_df_list = [pd.read_excel(file, index=False) for file in excel_file_list]
csv_df_list = [pd.read_csv(file, encoding='latin1', engine='python') for file in csv_file_list]
if excel_df_list:
	final.append(excel_df_list)
if csv_df_list:
	final.append(csv_df_list)

final_df = pd.concat(final)
writer = pd.ExcelWriter(os.path.join(working_dir, "Final.xlsx"))
final_df.to_excel(writer,'Sheet1')
writer.save()
writer.close()

# final_df.to_csv(os.path.join(working_dir, "Final.csv"))
