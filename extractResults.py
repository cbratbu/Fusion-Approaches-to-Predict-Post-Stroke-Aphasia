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

def getBestParams(dataSource, predictionModel, level, approach, experiment):
    output_file = final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" + "/" + level  + "/" +  dataSource + "/"  + dataSource + "_aggregate.csv"
    # print("output file = ", output_file)
    data = pd.read_csv(output_file,  delimiter=",")
    #
    data = data.sort_values(by = "test RMSE")
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


def getBestModel(dataSource, predictionModel, level, approach, experiment):
    best_model = ""
    data = pd.read_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" +"/" + level + "/" + dataSource + "/" + dataSource+"_aggregate.csv")
    data = data.sort_values(by = "validate RMSE")
    data = data[data["model"] == predictionModel]
    model_params = data.iloc[0,1:6]
    
    for param in model_params.index:
        best_model += str(model_params[param]) + "_"
    
    bestRMSE = data.iloc[0]["validate RMSE"]
    best_model = best_model[:-1]
    return best_model, bestRMSE


def getSources(approach, model, level, experiment):
    dataSourcePath = final_path + experiment + "/" + approach + "/" + model + "_predictions" + "/" + level + "/"
    dataSourceCombinations = os.listdir(dataSourcePath)
    # print("dataSourceCombinations = ", dataSourceCombinations)
    if "LS_results" in dataSourceCombinations:
        dataSourceCombinations.remove("LS_results") 
    return dataSourceCombinations



def get_stds(predictions, ground_truths, experiment):

    pearsonrs = []
    rmses = []


    addm = 5 if "normal" in experiment else 1
    # print(ground_truths)
    for i in range(0,len(predictions), addm):
        # temp_predictions = predictions[:i] + predictions[i+addm:]
        # temp_ground_truths = ground_truths[:i] + ground_truths[i+addm:]

        temp_predictions = predictions[i:i+addm]
        temp_ground_truths = ground_truths[i:i+addm]

        rmse_preds, pearsonr = mean_squared_error(temp_predictions, temp_ground_truths, squared = False), sp.pearsonr(temp_predictions, temp_ground_truths)[0]
        pearsonrs.append(pearsonr)
        rmses.append(rmse_preds)

    return pearsonrs, rmses




def writeFile(approach, model, level, dataSource, writer, experiment):
    # bestParam = getBestParams(dataSource, model, level, approach, experiment)
    # bestModel, rmse_val = getBestModel(dataSource, model, level, approach, experiment)
    
    # bestParamFilePath = final_path + experiment + "/" + approach + "/" + model + "_predictions/" + level + "/" + dataSource + "/"  + "outputs/" + bestModel + "/" + bestParam
    bestParamFilePath = final_path + experiment + "/" + approach + "/" + model + "_predictions/" + level + "/" + dataSource + "/" + "best_outputs.csv"
    data = pd.read_csv(bestParamFilePath)
    
    corr = data.corr().values[1,2]
    predictions, groundTruth = data["predictions"], data["ground truth score"]
    predictions = list(predictions)
    groundTruth = list(groundTruth)
    rmse_preds = mean_squared_error(predictions, groundTruth, squared = False)
    pearsonr, pval = sp.pearsonr(predictions,groundTruth)

    pearsonrs, rmses = get_stds(predictions,groundTruth, experiment)
    pr_std = np.std(pearsonrs)
    rmse_std = np.std(rmses)

    print(pearsonrs)

    
    # dataSource = "".join(dataSource.split("_")[:-1])
    # writer.writerow([" ".join(dataSource.split("-")), corr, rmse_preds, rmse_val])
    # writer.writerow([" ".join(dataSource.split("_")), corr, rmse_preds, rmse_val])
    
    if level == "level1":
        #dataSource = " ".join(dataSource.split("_")[:-1])
        dataSource = "".join(dataSource.split("_")[0])
    else:
        #dataSource = " ".join(dataSource.split("+")[:-1])
        dataSource = "".join(dataSource.split("_")[0])
        dataSource = " ".join(dataSource.split("+"))
        
    # print("dataSource here = ", dataSource)
    # writer.writerow([" ".join(dataSource.split("_")), corr, rmse_preds, pr_std, np.mean(pearsonrs),rmse_std, np.mean(rmses)])
    # writer.writerow([" ".join(dataSource.split("_")), pearsonr, rmse_preds, pr_std, np.mean(pearsonrs),rmse_std, np.mean(rmses)])
    writer.writerow([" ".join(dataSource.split("_")), np.mean(rmses), np.std(rmses), np.mean(pearsonrs), np.std(pearsonrs),rmse_preds, pearsonr])


def saveDoc(approach, levels, model, experiment):
    output_file = final_path + experiment + "/" + approach + "/" + model + "_predictions" + "/" + "modalityResults.csv"
    with open(output_file,"w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # writer.writerow(["Data Combination", "pearson's r pred", "RMSE pred", "RMSE val"])
        # writer.writerow(["Data Combination", "r Corr Coef", "RMSE pred", "std-r", "mean-r", "std-rmse", "mean-rmse"])
        writer.writerow(["Data Combination", "Mean-RMSE", "Std-RMSE", "Mean r-value", "Std r-value", "RMSE - Population", "r-value Population"])
        for level in levels:
            dataSources = getSources(approach, model, level, experiment) #gets the dataSources in each level
            # print("dataSources = ", dataSources)
            for dataSource in dataSources:
                writeFile(approach, model, level, dataSource, writer, experiment)
        
            # print("mse = ", format(RMSE, ".4f"), " -- pearsonr = ", pearsonr)
            
        
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="enter makeFile Arguments")
    parser.add_argument("-experiment", type = str, help = "which experiment : [ 'EXP-with-stans-features','EXP-without-stans-features', 'EXP-without-stans-features-noFeatureReduction',  'all-data-stacked-TrainData' ] ", default = "EXP-with-stans-features")
    args = parser.parse_args()
    experiment = args.experiment

    approaches = parameters["-approach"]
    # levels = parameters["-level"]
    levels = ["level1", "level2"]
    models = parameters["-model"]
    
    if "all-data-stacked" in experiment:
        levels = ["level1"]
        
    if "SVR" in experiment:
        models = ["SVR"]
    elif "RF" in experiment:
        models = ["RF"]
    # print("dataSources = ", )
    
    for approach in approaches:
        for model in models:
            saveDoc(approach, levels, model, experiment)
    
    
    
    

    
