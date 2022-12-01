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


def allParams(model):
    if model == "SVR":
        return SVR_params
    elif model == "RF":
        return RFParams

    