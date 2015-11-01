# data_incubator

This repository holds proof-of-concept code for predicting the impact of global events based on the known outcomes of previous events.  The predicted value in this case was a general positive or negative impact, but the code is easily adapted to predict more domain-specific quantities.

At this time all training data is obtained from the [GDELT](http://www.gdeltproject.org/) database via Google's BigQuery API.  During my time at the data incubator, I will focus on improving design, flexibility, usability, and incorporating more data sources.

In order to download the data with BigQuery, preprocess it, build a predictive model, and plot results, just execute:
```
python run_all.py
```

But the data download likely won't work unless you have your own BigQuery credentials.  So I have also made the preprocessed data available for download from Amazon S3.  The easiest way to download the files is to install the Amazon Web Services CLI and execute this from the command line:
```
aws s3 sync http://codejonincubator.s3.amazonaws.com/ <destination>
```
You may also download the files individually by adding one of the following file names to the url above:
```
first_6_years_distance_matrix.npy
last_6_years_distance_matrix.npy
results_first_6_years.npz
results_last_6_years.npz
train_test_first_6_years.npz
train_test_last_6_years.npz
```

The generated plots are included in this repository, and they are also hosted on Heroku [here.](https://blooming-brushlands-2390.herokuapp.com/) Please give the page a few seconds to load.

The code should be run in python 2.7 with recent versions of the following packages installed:
```
pandas
numpy
glmnet
matplotlib
geopy
countrycode
```
