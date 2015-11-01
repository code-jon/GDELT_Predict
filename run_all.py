#library imports
import pandas as pd
#from countrycode import countrycode
import numpy as np
from pandas import HDFStore,DataFrame
#from glmnet import ElasticNet, CVGlmNet
#import matplotlib
#import matplotlib.pyplot as plt

#local imports
import get_data_bigquery as gdb
import preprocess
import get_trn_test as gtt
import save_dist_m
import traintest as tt
import plot_results

df = gdb.get_current_data()
df.to_csv("per_day_from_pandas.csv")
#df = pd.read_csv("per_day_from_pandas.csv")

preprocess.normalize_by_event_count(df)

#hdf5 doesn't like unicode
df['country'] = df['country'].apply(lambda x: x.encode('ascii', 'ignore'))
countrydict = preprocess.get_country_lookup(df)
hdf = HDFStore('project_data.h5')
hdf.put('per_day_preprocessed', df, format='table', data_columns=True)
hdf.get_storer('per_day_preprocessed').attrs.country_lookup = countrydict

##END PREPROCESSING
train_years = 5
test_years = 1
hdf = HDFStore('project_data.h5')
df = hdf['per_day_preprocessed']
basename_out = "last_6_years"
train_start = 20091030
trainxy, testxy, countrylist = gtt.get_train_test(df, train_start, train_years, test_years)
train_x = trainxy[0]
train_y = trainxy[1]
test_x = testxy[0]
test_y = testxy[1]
np.savez("train_test_" + basename_out + ".npz", train_x = train_x, train_y = train_y, test_x = test_x, test_y = test_y, countrylist=countrylist)

basename_out = "first_6_years"
train_start = 19790101
trainxy, testxy, persistent_countries = gtt.get_train_test(df, train_start, train_years, test_years)
countrylist = persistent_countries
train_x = trainxy[0]
train_y = trainxy[1]
test_x = testxy[0]
test_y = testxy[1]
np.savez("train_test_" + basename_out + ".npz", train_x = train_x, train_y = train_y, test_x = test_x, test_y = test_y, countrylist=countrylist)
print("Finished extracting and saving train and test datasets...\n")

##now train and test on the data
tt.train_and_test("first_6_years")
tt.train_and_test("last_6_years")

##NOW WE HAVE PREDICTIONS.  MAKE PLOTS
#calculate and save distance matrices, used in plots
save_dist_m.save_distance_matrix("first_6_years")
save_dist_m.save_distance_matrix("last_6_years")
plot_results.pred_by_distance("first_6_years", "last_6_years")
plot_results.var_explained("first_6_years", "last_6_years")