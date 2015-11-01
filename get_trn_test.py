import pandas
import numpy as np

def get_train_test(df, train_start, train_years, test_years):
    min_time = df['date'].min()
    max_time = df['date'].max()
    train_increment = train_years * 10000
    train_end = train_start + train_increment #hoping we don't land on feb. 29th in a leap year
    train_frame = df.iloc[np.logical_and((df['date'] >= train_start).ravel(), (df['date'] < train_end).ravel())]
    test_start = train_end
    test_increment = test_years * 10000
    test_end = test_start + test_increment
    test_frame = df.iloc[np.logical_and((df['date'] >= test_start).ravel(), (df['date'] < test_end).ravel())]
    traindays = list(np.unique(train_frame["date"])) #returns a sorted array in ascending order
    testdays = list(np.unique(test_frame["date"]))
    unq1 = np.unique(train_frame.country)
    unq2 = np.unique(test_frame.country)
    persistent_countries = np.intersect1d(unq1,unq2)
    train_frame = train_frame.query('country in @persistent_countries')
    test_frame = test_frame.query('country in @persistent_countries')
    numtraindays = len(traindays) 
    numtestdays = len(testdays)
    numcountries = len(persistent_countries)
    train_x = np.zeros((numtraindays-1, numcountries))
    train_y = np.zeros((numtraindays-1, numcountries))
    test_x = np.zeros((numtestdays-1, numcountries))
    test_y = np.zeros((numtestdays-1, numcountries))
    for i, c in enumerate(persistent_countries):
	temp_df = train_frame.query('country == @c')
	temp_dates = list(temp_df["date"])
	for d in temp_dates:  
	    train_x_idx = traindays.index(d)
	    train_y_idx = train_x_idx - 1
	    if not(train_x_idx == len(traindays)-1):
		train_x[train_x_idx,i] = temp_df['weighted_mean_goldstein_x_tone'][temp_df['date']==d]
	    if train_y_idx >= 0:
		train_y[train_y_idx,i] = temp_df['weighted_mean_goldstein_x_tone'][temp_df['date']==d]
	temp_df = test_frame.query('country == @c')
	temp_dates = list(temp_df["date"])
	for d in temp_dates:  
	    test_x_idx = testdays.index(d)
	    test_y_idx = test_x_idx - 1
	    if not(test_x_idx == len(testdays)-1):
		test_x[test_x_idx,i] = temp_df['weighted_mean_goldstein_x_tone'][temp_df['date']==d]
	    if test_y_idx >= 0:
		test_y[test_y_idx,i] = temp_df['weighted_mean_goldstein_x_tone'][temp_df['date']==d]
    return (train_x, train_y), (test_x, test_y), persistent_countries