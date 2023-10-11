from libraries import * 
from params import PATH

def createF(path):
    if not os.path.exists( path):
        os.makedirs(path,exist_ok=True)

def create_folder(data, type = None, model = None, level=None, approach=None, experiment=None, fold=None):
    
    rspath = PATH 
    rsopath = PATH
    rsfpath = PATH
    
    model_path = model if model != None else ""
    level_path = level if level!=None else ""
    approach_path = approach if approach !=None else ""
    experiment = experiment if experiment != None else ""
    
    if data == "stan_optimal":
        rspath += "results/" + experiment + "/" + approach_path + "/" + model_path + "_predictions" + "/" + level_path + "/" + "stan_results/" + "fold-" + str(fold)    + "/model_performances" 
        rsopath += "results/" + experiment + "/" + approach_path + "/" + model_path + "_predictions"  + "/" + level_path + "/" + "stan_results/" + "fold-" + str(fold)  + "/outputs" 
        rsfpath += "results/" + experiment + "/" + approach_path + "/" + model_path + "_predictions"  + "/" + level_path + "/" + "stan_results/"+ "fold-" + str(fold)   + "/features" 
        
    
    else:
        rspath += "results/" + experiment + "/" + approach_path + "/" + model_path  + "_predictions"  + "/" +  level_path + "/" + data + "_results/" + "fold-" + str(fold)    + "/model_performances" 
        rsopath += "results/" + experiment + "/" + approach_path + "/" + model_path  + "_predictions"  + "/" + level_path + "/" + data + "_results/" + "fold-" + str(fold) + "/outputs" 
        rsfpath += "results/" + experiment + "/" + approach_path + "/" + model_path  + "_predictions"  + "/" + level_path + "/" + data + "_results/" + "fold-" + str(fold) + "/features" 
    
    
    if type == "performance":
        createF(rspath)
        return rspath + "/"
    elif type == "outputs":
        return rsopath
    elif type == "features":
        return rsfpath
        
    return rspath
    
    
# def getBestModalitytFeatureset():
    
        