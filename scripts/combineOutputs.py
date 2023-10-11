import pandas as pd
import re
import os 
from make import *
import argparse
from tqdm import tqdm
# from params import *

final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
data_path = "/projectnb/skiran/saurav/Fall-2022/src2/data/"

# files = datasets


def getBestParams(dataSource, predictionModel, level, approach, experiment, fold):
    output_file = final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" + "/" + level  + "/" +  dataSource + "/" + fold + "/" + dataSource + "_aggregate.csv"
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
        # print("param = ", param)
    
        match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        final_list = [float(x) for x in re.findall(match_number, word)]
        
        for i,x in enumerate(final_list):
            if type(x) == int or type(x) == float:
                if x < 0 and x%1 == 0:
                    x = int(x)
                    final_list[i] = x
                    

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



def getBestModel(dataSource, predictionModel, level, approach, experiment, fold):
    best_model = ""
    data = pd.read_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions" +"/" + level + "/" + dataSource + "/" + fold + "/" + dataSource+"_aggregate.csv")
    data = data.sort_values(by = "validate RMSE") # important line
    data = data[data["model"] == predictionModel]
    model_params = data.iloc[0,1:6]
    
    for param in model_params.index:
        best_model += str(model_params[param]) + "_"
    
    best_model = best_model[:-1]
    return best_model



def getOutputFname(dataSources, predictionModel, approach, level, experiment):
    # print("approach = ", approach)
    if approach == "LF":
        os.makedirs(data_path + experiment + "/" + "lateFusionData/" + predictionModel + "/", exist_ok = True)
    elif approach == "EF":
        os.makedirs(data_path + experiment + "/" + "earlyFusionData/" + predictionModel + "/", exist_ok = True)
        
    if len(dataSources) < len(datasets):
        dataSources = sorted(dataSources)
        # fname = ""
        
        fname = []
        for dataSource in dataSources:
            fname.append(dataSource.split("_")[0])
        fname = "_".join(sorted(fname))
            
        # print("dataSource = ",tempds)
        # print("sorted dataSource = ",sorted(tempds))
        # print("fname = ", "_".join(sorted(tempds)))

        # for dataSource in dataSources:
        #     fname += dataSource.split("_")[0] + "_"
        fname += "_ModalityOutputs.xlsx"

        # print("fname = ", fname)
        # print("\n")

        if approach == "LF":
            return data_path + experiment + "/" + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" +  fname
        elif approach == "EF":
            return data_path + experiment + "/" + "earlyFusionData/"+ predictionModel + "/" + predictionModel + "_" +  fname
            
    else:
        
        if approach == "LF":
            return data_path + experiment + "/" + "lateFusionData/"+ predictionModel + "/" + predictionModel + "_" + "allModalityOutputs.xlsx"
        elif approach == "EF":
            return data_path + experiment + "/" + "earlyFusionData/"+ predictionModel + "/" + predictionModel + "_" + "allModalityOutputs.xlsx"




def organizeOutputData(dataPaths, sources, predictionModel, approach, level, experiment):
    allModalityPreds = dict()
    # print("size of dataPaths = ", len(dataPaths))
    # print("sources = ", sources)
    # print("len(dataPaths) = ", len(dataPaths))
    # print(dataPaths)
    for i,bestM in enumerate(dataPaths):
        data = pd.read_csv(bestM)
        # newdata = data.sort_values(by = ["ground truth score"], ascending=True) 
        newdata = data
        ground_truths, predictions = newdata["ground truth score"], newdata["predictions"] #zip(*sorted(zip(newdata["ground truth score"], newdata["predictions"])))
        allModalityPreds[sources[i]] = predictions
    allModalityPreds["ground truth score"] = ground_truths
    allModalityPreds = pd.DataFrame(allModalityPreds)
    outputFname = getOutputFname(sources, predictionModel, approach, level, experiment)
    allModalityPreds.to_excel( outputFname)  # update this path based on what kind of fusion approach you are trying
                                                                                                                # also update if any data combinations you are going to try here.
        
    
    
        
def saveBestFiles(predictionModel, dataSources, level, experiment):
    approaches = parameters["-approach"]
    # experiments = parameters["-experiments"]
    
    # for experiment in experiments:
    for approach in approaches:
        datapaths = []
        for source in dataSources:
            print("dataSource = ", dataSources)
            print("source = ", source)
            if "+" not in source:
                level = "level1"
            else:
                level = "level2"
                
                
            totalPreds = []
            
            nfolds = None
            
            if "normal" in experiment:
                nfolds = 12
            else:
                nfolds = 56
            
            for fold in range(1,nfolds,1):
                bestParams = getBestParams(source, predictionModel, level, approach, experiment, "fold-"+str(fold)) # gets you the best training parameters for a dataSource with certain prediction model
                bestModel = getBestModel(source, predictionModel, level, approach, experiment, "fold-"+str(fold)) # need to update what this does. 
                if len(totalPreds) == 0:
                    totalPreds = pd.read_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/" + "fold-" + str(fold) + "/"  + "outputs/" + bestModel + "/" + bestParams).iloc[:,1:]
                else:
                    tdf = pd.read_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/" + "fold-" + str(fold) + "/"  + "outputs/" + bestModel + "/" + bestParams).iloc[:,1:]
                    totalPreds = pd.concat([totalPreds, tdf])
                    
            totalPreds.to_csv(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/" + "best_outputs.csv")
            datapaths.append(final_path + experiment + "/" + approach + "/" + predictionModel + "_predictions/" + level + "/" + source + "/" + "best_outputs.csv")
                
            
    # print(datapaths)
    if level == "level1":
        organizeOutputData(datapaths, dataSources, predictionModel, approach, level, experiment)
    
    
    
        
def saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level, experiment):  # saves outputs combinations for different data source combinations
    dataSourcesCombinations = []
    print("total dataSources = ", len(dataSources))
    
    if level == "level1":
        for i in range(1,len(dataSources)+1):
            dataSourcesCombinations += list(map(list,list(itertools.combinations(dataSources, i))))
    elif level == "level2":
        dataSourcesCombinations = dataSources
        
    for predictionModel in predictionModels:
        for dataSources in tqdm(dataSourcesCombinations):
            saveBestFiles(predictionModel, dataSources, level, experiment)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter combineOutputs Arguments")
    parser.add_argument("-level", type = str, help = "levels : [ level1, level2 ] ", default = "level1")
    # parser.add_argument("-model", type = str, help = "model : [ RF, SVR, GB ] ", default = "RF")
    parser.add_argument("-experiment", type = str, help = "experiment to run : [ EXP-with-stans-features ] ", default = "EXP-with-stans-features")
    # parser.add_argument("-o", type = str, help = "Enter output file name")
    args = parser.parse_args()
    level = args.level
    experiment = args.experiment
    approaches = parameters["-approach"]
    # model = args.model
    # experiments = parameters["-experiment"]

    
    files = datasets

    if level == "level2":
        files = []
        for i in range(1,len(datasets)+1):
            files += sorted(list(map(list,list(itertools.combinations(datasets, i)))))
            
        tempfiles = []        
        for dataSource in files:
            fname = "+".join(sorted(dataSource))
            tempfiles.append([fname + "_results"])
        dataSources = tempfiles
    
    # files = tempfiles
            

    # print("files = ", files)

    if "without-stans-features" in experiment or "noStan" in experiment: # experiment == "EXP-without-stans-features" or experiment == "EXP-without-stans-features-noFeatureReduction":
        files.remove("stan_optimal")
        
    
    # print("path = ", final_path )
    # print("",files[0].split("+")[0])

    if level=="level1":
        dataSources = [f.split("+")[0] + "_results" for f in files if not os.path.isfile(final_path + f)] 
        print("dataSources = ", dataSources)

    predictionModels = parameters["-model"]
    if "all-data-stacked" in experiment:
        files = ["combined_features"]
        dataSources = ["combined_features_results"]
    

    if "SVR" in experiment:
        predictionModels = ["SVR"]
    elif "RF" in experiment:
        predictionModels = ["RF"]
    elif "GB" in experiment:
        predictionModels = ["GradBoost"]
    # for predictionModel in predictionModels:
    #     saveBestFiles(predictionModel, dataSources)
    
    # print("datasources = ", dataSources)    
    saveBestOutputs_dataSourceCombinations(dataSources, predictionModels, level, experiment)
    
    
    
    
    
    
    