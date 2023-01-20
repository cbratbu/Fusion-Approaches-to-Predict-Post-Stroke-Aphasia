from libraries import *
from params import *

# Integrate this with the main model

def getModel(model):
    if model == "SVR":
        # print("model called = SVR")
        return SVR
    elif model == "RF":
        # print("model called = RF")
        return RandomForestRegressor
    elif model == "AdaBoost":
        return AdaBoostRegressor


def allParams(model):
    if model == "SVR":
        return SVR_params
    elif model == "RF":
        return RFParams
    elif model == "AdaBoost":
        return ABParams

    