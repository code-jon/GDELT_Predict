import pandas as pd
from countrycode import countrycode

def normalize_by_event_count():
    dates = pd.unique(df.date)
    events_per_day = [0]*len(dates)
    df["worldwide_event_count"] = [0]*len(df)
    for d in dates:
	temp = sum(df.loc[df.date==d, "event_count"])
	df.loc[df.date==d, "worldwide_event_count"] = temp
	print "finished %d" % d
    df["fraction_world_news"] = df["event_count"] / df["worldwide_event_count"]
    df["weighted_mean_goldstein_x_tone"] = df["mean_goldstein_x_tone"]*df["fraction_world_news"]

def get_country_lookup(df):
    countrycodes = pd.unique(df.country)
    countries = countrycode(codes=list(countrycodes), origin="fips104", target='country_name')
    for i, c in enumerate(countries):
	if c is None:
	    countries[i] = countrycodes[i]
    keys = countrycodes
    values = countries
    countrydict = dict(zip(keys, values))
    return countrydict