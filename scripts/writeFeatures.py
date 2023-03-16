import pandas as pd
import re
import os 
from make import *
import argparse
import collections
# from params import *

final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
data_path = "/projectnb/skiran/saurav/Fall-2022/src2/data/"

# files = datasets


def getBestParams(dataSource, predictionModel, level, approach, experiment):
    output_file = final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" + "/" + level  + "/" +  dataSource + "/"  + dataSource + "_aggregate.csv"
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



def getBestModel(dataSource, predictionModel, level, approach, experiment):
    best_model = ""
    data = pd.read_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" +"/" + level + "/" + dataSource + "/" + dataSource+"_aggregate.csv")
    data = data.sort_values(by = "validate RMSE")
    data = data[data["model"] == predictionModel]
    model_params = data.iloc[0,1:6]
    
    for param in model_params.index:
        best_model += str(model_params[param]) + "_"
    
    best_model = best_model[:-1]
    return best_model



def getOutputFname(dataSources, predictionModel, approach, level, experiment):
    print("approach = ", approach)
    if approach == "LF":
        os.makedirs(data_path + experiment + "/" + "lateFusionData/" + predictionModel + "/", exist_ok = True)
    elif approach == "EF":
        os.makedirs(data_path + experiment + "/" + "earlyFusionData/" + predictionModel + "/", exist_ok = True)
        
    if len(dataSources) < len(datasets):
        dataSources = sorted(dataSources)
        fname = ""
        for dataSource in dataSources:
            fname += dataSource.split("_")[0] + "_"
        fname += "ModalityOutputs.xlsx"
        if approach == "LF":
            return data_path + experiment + "/" + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" +  fname
        elif approach == "EF":
            return data_path + experiment + "/" + "earlyFusionData/"+ predictionModel + "/" + predictionModel + "_" +  fname
            
    else:
        
        if approach == "LF":
            return data_path + experiment + "/" + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" + "allModalityOutputs.xlsx"
        elif approach == "EF":
            return data_path + experiment + "/" + "earlyFusionData/"+ predictionModel + "/" + predictionModel + "_" + "allModalityOutputs.xlsx"




def organizeOutputData(datapath, path_, bestModel):

    data = pd.read_csv(datapath, sep = " ", header = None)
    temp = data.values.flatten()
    temp = dict(collections.Counter(temp).most_common())
    df = pd.DataFrame(list(temp.keys()), columns = ["features"])
    df["frequency"] = list(temp.values())
    
    match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
    num_features = int(re.findall(match_number, bestModel)[0])
    
    df.to_csv(path_ + "bestFeatureSet-all.csv")
    df = df.iloc[:num_features, :]
    df.to_csv(path_ + "bestFeatureSet.csv")
    
    # print("bestmodel = ", bestModel + " -- num frs = ", num_features,  "\n")
    

    
    
    
        
def saveBestFiles(predictionModel, dataSources, level, experiment):
    approaches = parameters["-approach"]
    for approach in approaches:
        for source in dataSources:
            bestParams = getBestParams(source, predictionModel, level, approach, experiment) # gets you the best training parameters for a dataSource with certain prediction model
            bestModel = getBestModel(source, predictionModel, level, approach, experiment) # need to update what this does. 
            
            featureSavePath =  final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/" 
            path_ = final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/"  + "features/" + bestModel + "/" 
            datapath = path_ + bestParams
            organizeOutputData(datapath, featureSavePath, bestModel)
            
    
    
    
    
        
def saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level, experiment):  # saves outputs combinations for different data source combinations
    dataSourcesCombinations = []
    # print("this even happening?")
    if level=="level1":
        for i in range(1,len(dataSources)+1):
            dataSourcesCombinations += list(map(list,list(itertools.combinations(dataSources, i))))
    
    elif level=="level2":
        # print("we should be here right?")
        for i in range(2,len(dataSources)+1):
            dataSourcesCombinations += list(map(list,list(itertools.combinations(dataSources, i))))
            
    # print(dataSourcesCombinations)
        
    for dataSources in dataSourcesCombinations:
        for predictionModel in predictionModels:
            # print("this executing??")
            if level == "level1":
                saveBestFiles(predictionModel, dataSources, level, experiment)
            elif level == "level2":
                dataSources = sorted([x.split("_")[0] for x in dataSources])
                # if len(dataSources) != len(datasets) and ("EXP-without-stans-features" not in experiment):
                dataSources = ["-".join(dataSources)  + "_results"] 
                saveBestFiles(predictionModel, dataSources, level, experiment)
                    




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter combineOutputs Arguments")
    parser.add_argument("-level", type = str, help = "levels : [ level1, level2 ] ", default = "level1")
    parser.add_argument("-experiment", type = str, help = "experiment to run : [ EXP-with-stans-features ] ", default = "EXP-with-stans-features")
    args = parser.parse_args()
    
    level = args.level
    experiment = args.experiment
    
    approaches = parameters["-approach"]

    files = datasets
    
    # print("anythings happening??")
    
    if "without-stans-features" in experiment or "noStan" in experiment: #experiment == "EXP-without-stans-features" or experiment == "EXP-without-stans-features-noFeatureReduction":
        files.remove("stan_optimal")
    
    dataSources = [f.split("_")[0] + "_results" for f in files if not os.path.isfile(final_path + f)] 
    predictionModels = parameters["-model"]
    
    if "all-data-stacked" in experiment:
        files = ["combined_features"]
        dataSources = ["combined_features_results"]

    if "SVR" in experiment:
        predictionModels = ["SVR"]
    elif "RF" in experiment:
        predictionModels = ["RF"]
    # print("we here yet???")
    # for predictionModel in predictionModels:
    #     saveBestFiles(predictionModel, dataSources)
        
    saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level, experiment)
    
    
    
    
    
    
    