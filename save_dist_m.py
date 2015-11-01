#geodesic distance
from geopy.distance import vincenty, great_circle
import pandas as pd
import numpy as np
from pandas import HDFStore,DataFrame

def save_distance_matrix(basename):
    hdf = HDFStore('project_data.h5')
    df = hdf['per_day_preprocessed']
    d = np.load('train_test_' + basename + '.npz')
    countrylist = d["countrylist"]

    country_lats = np.zeros(len(countrylist))
    country_longs = np.zeros(len(countrylist))
    distances = np.zeros((len(countrylist), len(countrylist)))

    for i, c in enumerate(countrylist):
	temp_df = df.query('country == @c')
	country_lats[i] = temp_df["lat"].iloc[0]
	country_longs[i] = temp_df["long"].iloc[0]
	print "finished country %d" % (i+1)
    #calculate geodesic distance matrix
    for i in range(len(countrylist)):
	for j in range(len(countrylist)):
	    v = great_circle((country_lats[i], country_longs[i]), (country_lats[j], country_longs[j]))
	    distances[i,j] = v.km
	    #print("i: %d" % i)
	print("i: %d" % i)
    np.save(basename + "_distance_matrix.npy", distances)

