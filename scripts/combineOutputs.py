import pandas as pd
import re
import os 
from make import *
import argparse
# from params import *

final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
data_path = "/projectnb/skiran/saurav/Fall-2022/src2/data/"

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
        model_params = data.iloc[:,21:23]
    else:
        model_params = data.iloc[:,21:]
    
    fname = ""
    
    # print("cols = ", model_params.columns)
    for parameter in model_params.columns:
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
    
    best_model = best_model[:-1]
    return best_model


def getOutputFname(dataSources, predictionModel, approach, level):
    if approach == "LF":
        os.makedirs(data_path + "lateFusionData/" + predictionModel + "/", exist_ok = True)
    elif approach == "EF":
        os.makedirs(data_path + "earlyFusionData/" + predictionModel + "/", exist_ok = True)
        
    if len(dataSources) < len(datasets):
        dataSources = sorted(dataSources)
        fname = ""
        for dataSource in dataSources:
            fname += dataSource.split("_")[0] + "_"
        fname += "ModalityOutputs.xlsx"
        return data_path + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" +  fname
            
    else:
        return data_path + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" + "allModalityOutputs.xlsx"
            

def organizeOutputData(dataPaths, sources, predictionModel, approach, level):
    allModalityPreds = dict()
    # print("size of dataPaths = ", len(dataPaths))
    for i,bestM in enumerate(dataPaths):
        data = pd.read_csv(bestM)
        newdata = data.sort_values(by = ["ground truth score"], ascending=True)
        ground_truths, predictions = zip(*sorted(zip(newdata["ground truth score"], newdata["predictions"])))
        allModalityPreds[sources[i]] = predictions
    allModalityPreds["ground truth score"] = ground_truths
    allModalityPreds = pd.DataFrame(allModalityPreds)
    outputFname = getOutputFname(sources, predictionModel, approach, level)
    allModalityPreds.to_excel( outputFname)  # update this path based on what kind of fusion approach you are trying
                                                                                                                # also update if any data combinations you are going to try here.
        
        
def saveBestFiles(predictionModel, dataSources, level):
    datapaths = []
    approaches = parameters["-approach"]
    for approach in approaches:
        for source in dataSources:
            bestParams = getBestParams(source, predictionModel, level, approach) # gets you the best training parameters for a dataSource with certain prediction model
            bestModel = getBestModel(source, predictionModel, level, approach) # need to update what this does. 
            datapaths.append(final_path + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/"  + "outputs/" + bestModel + "/" + bestParams)
    organizeOutputData(datapaths, dataSources, predictionModel, approach, level)
    
        
def saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level):  # saves outputs combinations for different data source combinations
    dataSourcesCombinations = []
    for i in range(1,len(dataSources)+1):
        dataSourcesCombinations += list(map(list,list(itertools.combinations(dataSources, i))))
        
    for dataSources in dataSourcesCombinations:
        for predictionModel in predictionModels:
            saveBestFiles(predictionModel, dataSources, level)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter combineOutputs Arguments")
    parser.add_argument("-level", type = str, help = "levels : [ level1, level2 ] ", default = "level1")
    # parser.add_argument("-o", type = str, help = "Enter output file name")
    args = parser.parse_args()
    level = args.level
    approaches = parameters["-approach"]

    files = datasets
    dataSources = [f.split("_")[0] + "_results" for f in files if not os.path.isfile(final_path + f)] 
    predictionModels = parameters["-model"]

    # for predictionModel in predictionModels:
    #     saveBestFiles(predictionModel, dataSources)
        
    saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level)
    
    
    
    
    
    
    