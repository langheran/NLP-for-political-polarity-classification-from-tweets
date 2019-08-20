import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

working_dir = r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\semanas'
df = pd.read_pickle(os.path.join(working_dir, "final.pickle"))

dfMartha = pd.melt(df, id_vars=['id'], var_name="attitude", value_name="rank", value_vars=['proactivo', 'agresivo', 'provoto', 'reactivo'])

data = [dfMartha["rank"].values]
# multiple box plots on one figure
plt.figure()
# plt.boxplot(data)
plt.hist(data, bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.show()