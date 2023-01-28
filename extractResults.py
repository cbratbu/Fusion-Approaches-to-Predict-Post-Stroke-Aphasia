# from scripts.libraries import * 
import argparse 
import os 
from scripts.make import *
import csv
import pandas as pd
import re
import scipy.stats as sp
from sklearn.metrics import mean_squared_error, r2_score
# from scripts.combineOutputs import *

final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"

def getBestParams(dataSource, predictionModel, level, approach):
    output_file = final_path + approach + "/" + predictionModel + "_predictions" + "/" + level  + "/" +  dataSource + "/"  + dataSource + "_aggregate.csv"
    # print("output file = ", output_file)
    data = pd.read_csv(output_file,  delimiter=",")
    #
    data = data.sort_values(by = "validate RMSE")
    # print("data shape = ", data.shape)
    # print("data = ", data.iloc[0]["model"])
    model = data.iloc[0]["model"]

    if model == "RF":
        model_params = data.iloc[:,21:24]
    else:
        model_params = data.iloc[:,21:]
    
    fname = ""
    
    # print("cols = ", model_params.columns)
    for parameter in model_params.columns:
        # print("parameters = ", model_params.columns)
        # print("parameter = ", parameter)
        word =  model_params[parameter].iloc[0]
        # print("parameter = ",parameter, " -- word = ", word)
        param = re.findall(r"\b[^\d\W]+\b", word)
    
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        final_list = [float(x) for x in re.findall(match_number, word)]
    
        if len(param) > 1:
            fname += "[" + param[0][0] + "-" + param[1] + "]" + "_"
        else:
            if model == "RF":
                if final_list[0] >= 1:
                    final_list[0] = int(final_list[0])
                if "log" in word:
                    fname += "[" + param[0][0] + "-log" + str(final_list[0]) + "]" + "_"
                else:
                    fname += "[" + param[0][0] + "-" + str(final_list[0]) + "]" + "_"
            else:
                
                if final_list[0] >= 1:
                    final_list[0] = int(final_list[0])
                fname += "[" + param[0][0] + "-" + str(final_list[0]) + "]" + "_"
    fname = fname[:-1] + ".csv"
    return fname


def getBestModel(dataSource, predictionModel, level, approach):
    best_model = ""
    data = pd.read_csv(final_path + approach + "/" + predictionModel + "_predictions" +"/" + level + "/" + dataSource + "/" + dataSource+"_aggregate.csv")
    data = data.sort_values(by = "validate RMSE")
    data = data[data["model"] == predictionModel]
    model_params = data.iloc[0,1:6]
    
    for param in model_params.index:
        best_model += str(model_params[param]) + "_"
    
    bestRMSE = data.iloc[0]["validate RMSE"]
    best_model = best_model[:-1]
    return best_model, bestRMSE


def getSources(approach, model, level):
    dataSourcePath = final_path + approach + "/" + model + "_predictions" + "/" + level + "/"
    dataSourceCombinations = os.listdir(dataSourcePath)
    if "LS_results" in dataSourceCombinations:
        dataSourceCombinations.remove("LS_results") 
    return dataSourceCombinations


def writeFile(approach, model, level, dataSource, writer):
    bestParam = getBestParams(dataSource, model, level, approach)
    bestModel, rmse_val = getBestModel(dataSource, model, level, approach)
    
    bestParamFilePath = final_path + approach + "/" + model + "_predictions/" + level + "/" + dataSource + "/"  + "outputs/" + bestModel + "/" + bestParam
    data = pd.read_csv(bestParamFilePath)
    
    corr = data.corr().values[1,2]
    predictions, groundTruth = data["predictions"], data["ground truth score"]
    rmse_preds, pearsonr = mean_squared_error(predictions, groundTruth, squared = False), sp.pearsonr(predictions, groundTruth)
    
    dataSource = "".join(dataSource.split("_")[:-1])
    writer.writerow([" ".join(dataSource.split("-")), corr, rmse_preds, rmse_val])


def saveDoc(approach, levels, model):
    output_file = final_path + approach + "/" + model + "_predictions" + "/" + "modalityResults.csv"
    with open(output_file,"w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Data Combination", "pearson's r pred", "RMSE pred", "RMSE val"])
        for level in levels:
            dataSources = getSources(approach, model, level) #gets the dataSources in each level
            for dataSource in dataSources:
                writeFile(approach, model, level, dataSource, writer)
        
            # print("mse = ", format(RMSE, ".4f"), " -- pearsonr = ", pearsonr)
            
        
        

if __name__ == "__main__":
    approaches = parameters["-approach"]
    levels = parameters["-level"]
    models = parameters["-model"]
    
    for approach in approaches:
        for model in models:
            saveDoc(approach, levels, model)
    
    
    
    

    