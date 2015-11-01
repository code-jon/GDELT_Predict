import numpy as np
from pandas import HDFStore,DataFrame
from glmnet import ElasticNet, CVGlmNet

def train_and_test(basename):
    d = np.load("train_test_" + basename + ".npz")
    train_x = d["train_x"]
    train_y = d["train_y"]
    test_x = d["test_x"]
    test_y = d["test_y"]
    countrylist = d["countrylist"]
    numcountries = train_x.shape[1]
    weights = np.zeros((numcountries,numcountries))
    enets = [None]*numcountries
    enet_cvs = [None]*numcountries
    preds = np.zeros(test_y.shape)
    errors = np.zeros(test_y.shape)
    var_ratio = np.zeros((numcountries))
    for i in range(numcountries):
	enets[i] = ElasticNet(alpha=.1)
	enet_cvs[i] = CVGlmNet(enets[i], n_folds=10, n_jobs=10)
	enet_cvs[i].fit(train_x, train_y[:,i])
	bli = enet_cvs[i].best_lambda_idx
	weights[i,:] = enet_cvs[i].base_estimator.get_coefficients_from_lambda_idx(bli)
	preds[:,i] = enet_cvs[i].predict(test_x)
	errors[:,i] = test_y[:,i] - preds[:,i]
	var_truth = np.var(test_y[:,i])
	var_err = np.var(errors[:,i])
	var_ratio[i] = 1 - var_err/var_truth
	print("finished predicting country number %d" % i)
    np.savez("results_" + basename + ".npz", preds = preds, truth=test_y, errors = errors, var_ratio = var_ratio, countrylist = countrylist, weights=weights)
