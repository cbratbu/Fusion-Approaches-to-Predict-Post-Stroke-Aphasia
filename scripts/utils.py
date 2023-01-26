from libraries import * 
from params import PATH

def createF(path):
    if not os.path.exists( path):
        os.makedirs(path,exist_ok=True)

def create_folder(data, type = None, model = None, level=None, approach=None):
    
    rspath = PATH 
    rsopath = PATH
    rsfpath = PATH
    
    model_path = model if model != None else ""
    level_path = level if level!=None else ""
    approach_path = approach if approach !=None else ""
    
    if data == "stan_optimal":
        rspath += "results/" + approach_path + "/" + model_path + "_predictions" + "/"  + level_path + "/" + "stan_results/"   + "/model_performances" 
        rsopath += "results/" + approach_path + "/" + model_path + "_predictions" + "/"  + level_path + "/" + "stan_results/"  + "/outputs" 
        rsfpath += "results/" + approach_path + "/" + model_path + "_predictions" + "/"  + level_path + "/" + "stan_results/"  + "/features" 
        
    
    else:
        rspath += "results/"+ approach_path + "/" + model_path  + "_predictions" + "/" + level_path + "/" + data + "_results/"  + "/model_performances" 
        rsopath += "results/" + approach_path + "/" + model_path  + "_predictions" + "/" + level_path + "/" + data + "_results/" + "/outputs" 
        rsfpath += "results/" + approach_path + "/" + model_path  + "_predictions" + "/" + level_path + "/" + data + "_results/" + "/features" 
    
    
    if type == "performance":
        createF(rspath)
        return rspath + "/"
    elif type == "outputs":
        return rsopath
    elif type == "features":
        return rsfpath
        
    return rspath
    
    
# def getBestModalitytFeatureset():
    
        