import os
import csv

import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import scipy.stats as sp

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error

from scripts.make import *
from sklearn.svm import SVR
import itertools
from tqdm import tqdm
import argparse

PATH = "/projectnb/skiran/saurav/Fall-2022/src2/"

# files = os.listdir("results/")
# files = [f for f in listdir(PATH + "results/") if isfile(join(PATH + "results/", f))]

results_folder = PATH + "results/model_performances"
output_file_path = PATH + "results/"
# output_file =  PATH + "results/final.csv"


num_ranks = 3

def writeResults(predictionModel, approaches, level):
    """Writes the top-3 best prediction outputs in each of the top-k feature setting 
    
    """
    # for level in parameters["-level"]:

    for approach in approaches:
        output_file = output_file_path + approach + "/" + predictionModel + "_predictions/" + predictionModel + "_" + level + "_final.csv"
        with open(output_file,"w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["CV type", "model", "metrics", "num features", "reduction method","stratified","data source", "train RMSE", "validate RMSE", "test RMSE",
                                                                            "train RMSE rank", "validate RMSE rank", "test RMSE rank",
                                                                            "train MAE", "validate MAE", "test MAE",
                                                                            "train MAE rank", "validate MAE rank", "test MAE rank", "SupportVectors", "model parameters", "PARAM1", "PARAM2", "PARAM3", "PARAM4"])
                                                                            
            files = os.listdir(PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/")
            dataFolders = [f for f in files if not os.path.isfile(PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/"+ f)] # data sources
            print("data folders = ", dataFolders)
            
            for dataFolder in dataFolders: 
                results_folder = PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/" + dataFolder  + "/model_performances"  # check only if path exists.
                files = [f for f in listdir(results_folder + "/") if isfile(join(results_folder + "/", f))]
                
                for file in files:
                    train_settings = file.split("_")
                    print(train_settings)
                    data = pd.read_csv(results_folder + "/"+file)
            
                    # print(file)
                    param_id = data.columns[-1]
                    # print("paramID = ",param_id)
                    data = data.sort_values(by = "validate rank") if "validate rank" in data.columns else data.sort_values(by = "validate MSE rank") if "validate MSE rank" in data.columns else data.sort_values(by = 'test MSE rank')
                    data_subset = data.iloc[:num_ranks]
            
                    for i in range(num_ranks):
                        train_MSE, train_MSE_rank = data_subset.iloc[i]["train performance RMSE" if "train performance RMSE" in data_subset.columns else "train RMSE"], data_subset.iloc[i]["train rank"if "train rank" in data_subset.columns else "train RMSE rank"]
                        test_MSE, test_MSE_rank = data_subset.iloc[i]["test performance RMSE" if "test performance RMSE" in data_subset.columns else "test RMSE"], data_subset.iloc[i]["test rank" if "test rank" in data_subset.columns else "test RMSE rank"]
                        validate_MSE, validate_MSE_rank = data_subset.iloc[i]["validate performance RMSE"] if "validate performance RMSE" in data_subset.columns else "-", data_subset.iloc[i]["validate rank"] if "validate rank" in data_subset.columns else data_subset.iloc[i]["validate RMSE rank"] if "validate RMSE rank" in data_subset.columns else "-"
            
            
                        train_MAE, train_MAE_rank = data_subset.iloc[i]["train performance MAE" if "train performance MAE" in data_subset.columns else "train MAE"], data_subset.iloc[i]["train MAE rank"if "train MAE rank" in data_subset.columns else "train rank"]
                        test_MAE, test_MAE_rank = data_subset.iloc[i]["test performances MAE" if "test performances MAE" in data_subset.columns else "test MAE" if "test MAE" in data_subset.columns else "test performance MAE"], data_subset.iloc[i]["test MAE rank" if "train MAE rank" in data_subset.columns else "test rank"]
                        validate_MAE, validate_MAE_rank = data_subset.iloc[i]["validate performance MAE"] if "validate performance MAE" in data_subset.columns else "-", data_subset.iloc[i]["validate rank"] if "validate rank" in data_subset.columns else data_subset.iloc[i]["validate MAE rank"] if "validate MAE rank" in data_subset.columns else "-"
                        
                        # print("cols = ", data_subset.columns)
                        support_vectors = str(data_subset.iloc[i]["support vectors"])
                        
                        params = data_subset.iloc[i][param_id]
                        param_dict = dict(zip(param_id.split("|"), params.split(",")))
                        
                        
            
                        if len(train_settings) >= 4:
                            writer.writerow([train_settings[0], train_settings[1], train_settings[2], train_settings[3], train_settings[-1][:-4], train_settings[4],dataFolder, train_MSE, validate_MSE, test_MSE,
                                                                                                                        train_MSE_rank, validate_MSE_rank, test_MSE_rank,
                                                                                                                        train_MAE, validate_MAE, test_MAE,
                                                                                                                        train_MAE_rank, validate_MAE_rank, test_MAE_rank, support_vectors, param_dict])
                        else:
                            writer.writerow([train_settings[0], train_settings[1], train_settings[2], train_settings[3], train_settings[-1][:-4], train_settings[4], dataFolder, train_MSE, validate_MSE, test_MSE,
                                                                                                                        train_MSE_rank, validate_MSE_rank, test_MSE_rank,
                                                                                                                        train_MAE, validate_MAE, test_MAE,
                                                                                                                        train_MAE_rank, validate_MAE_rank, test_MAE_rank,support_vectors, param_dict])
    

def writeFiles(predictionModel, approaches, level):
    for approach in approaches:
        files = os.listdir(PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/")
        # print("path here = ", PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/")
        dataFolders = [f for f in files if not os.path.isfile(PATH + "results/" + approach + "/" + predictionModel + "_predictions" + "/" + level + "/" + f)]    # data sources
        # print("dataFolders here = ", dataFolders)
        # for level in parameters["level"]:
        output_file = output_file_path + approach + "/" + predictionModel + "_predictions/" + predictionModel + "_" + level + "_final.csv"                 # final output file 
        totalData = pd.read_csv(output_file)     
        for source in dataFolders:
            data = totalData[totalData["data source"] == source]
            data = data[data["model"] == predictionModel]
            data.to_csv(PATH+"results/"  + approach + "/"  + predictionModel + "_predictions"+ "/" + level + "/" + source + "/"+ source + "_aggregate.csv")
        
        
def modelWiseUpdate(predictionModels, approaches, level):
    for predictionModel in predictionModels:
        writeResults(predictionModel, approaches, level) # compiles the aggregation of aggregate. 
        writeFiles(predictionModel, approaches, level)  # compiles aggregate performances for each predictor varying with parameter sizes
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter network arguments")
    parser.add_argument("-level", type = str, help = "enter level : [level1, level2] ", default = "level1")
    args = parser.parse_args()
    level = args.level
    
    predictionModels = parameters["-model"]
    approaches = parameters["-approach"]
    # print(Augmentation_settings["approach"])
    # print(Augmentation_settings["level"])
    modelWiseUpdate(predictionModels, approaches, level)
    
    
    
    
    
    
