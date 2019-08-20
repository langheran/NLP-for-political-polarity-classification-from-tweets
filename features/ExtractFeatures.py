import __init__
from features import ExtractBOW as bow
from features import ExtractW2V as w2v
from features import ExtractBIG as big
from features import save

def ExtractFeatures(df, *args):
	for featureExtractor in args:
		df = featureExtractor(df)
	return df, [a.__name__.replace('Extract','') for a in args]

if(__name__=="__main__"):
	import load_dataframe
	df = load_dataframe.getTokenizedDataFrame()
	df = ExtractFeatures(df, bow.ExtractBOW, w2v.ExtractW2V, big.ExtractBIG)
	save.save_all(df, "all")