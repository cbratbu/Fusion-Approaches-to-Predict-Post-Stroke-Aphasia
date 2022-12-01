import pandas as pd
import re
import os 
# from params import *

final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
data_path = "/projectnb/skiran/saurav/Fall-2022/src2/data/"

def getBestParams(dataSource):
    output_file = final_path + dataSource + "/" + dataSource + "_aggregate.csv"
    data = pd.read_csv(output_file,  delimiter=",")
    #
    data = data.sort_values(by = "validate MSE")
    model = data.iloc[0]["model"]

    if model == "RF":
        model_params = data.iloc[:,19:22]
    else:
        model_params = data.iloc[:,19:]
    
    fname = ""
    
    for parameter in model_params.columns:
        word =  model_params[parameter].iloc[0]
        # print("word = ", word)
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

def getBestModel(dataSource):
    best_model = ""
    data = pd.read_csv(final_path + dataSource + "/" + dataSource+"_aggregate.csv")
    data = data.sort_values(by = "validate MSE")
    model_params = data.iloc[0,1:5]
    
    for param in model_params.index:
        best_model += str(model_params[param]) + "_"
    
    best_model = best_model[:-1]
    return best_model


def organizeOutputData(dataPaths, sources):
    allModalityPreds = dict()
    for i,bestM in enumerate(dataPaths):
        data = pd.read_csv(bestM)
        
        newdata = data.sort_values(by = ["ground truth score"], ascending=True)
        ground_truths, predictions = zip(*sorted(zip(newdata["ground truth score"], newdata["predictions"])))
        allModalityPreds[sources[i]] = predictions
    allModalityPreds["ground truth score"] = ground_truths
    allModalityPreds = pd.DataFrame(allModalityPreds)
    allModalityPreds.to_csv(data_path + "allModalityOutputs.csv")
        
        

if __name__ == "__main__":

    files = os.listdir(final_path)
    dataSources = [f for f in files if not os.path.isfile(final_path + f)]    
    # print("sources = ", dataSources)
    dataPaths = []
    for source in dataSources:
        bestParams = getBestParams(source)
        bestModel = getBestModel(source)
        dataPaths.append( final_path + source + "/outputs/" + bestModel + "/" + bestParams)
    organizeOutputData(dataPaths, dataSources)
    
    
    
    
    
    
    