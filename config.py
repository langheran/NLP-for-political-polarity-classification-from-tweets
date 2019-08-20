import random
seed = 100
random.seed(seed)
data_dir = r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\semanas'
pickles_dir = r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\pickles'
output_dir = r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\output'
w2v_model_bin=r"C:\Users\langh\Datasets\sbw_vectors.bin"
images_dir=r'C:\Users\langh\Dropbox\MCC-I Masters\Computational Techniques for Machine Learning\P1\DATA\images'

import os
pos_emoticons_csv=os.path.join(data_dir, "pos_emoticons.csv")
neg_emoticons_csv=os.path.join(data_dir, "neg_emoticons.csv")