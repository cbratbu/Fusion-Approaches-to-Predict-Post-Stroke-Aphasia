from libraries import * 
from params import PATH

PATH = os.path.abspath("../") + "/"

def createF(path):
    if not os.path.exists(path):
        os.makedirs(path,exist_ok=True)

def create_folder(data, type = None, model = None):
    
    rspath = PATH
    rsopath = PATH
    rsfpath = PATH
    
    if data == "stan_optimal":
        # if not os.path.exists(PATH + "results/stan_results/model_performances"):
        #     os.makedirs(PATH + "results/stan_results/model_performances")
        rspath += "results/stan_results/model_performances" + "/" + model  if model!=None else ""
        rsopath += "results/stan_results/outputs" + "/" + model if model!=None else ""
        rsfpath += "results/stan_results/features" + "/" + model if model!=None else ""
        
    
    else:
        # if not os.path.exists(PATH + "results/" + data + "_results/model_performances"):
        #     os.makedirs(PATH + "results/" + data + "_results/model_performances")
        rspath += "results/"+ data+ "_results/model_performances" + "/" + model  if model!=None else ""
        rsopath += "results/" + data + "_results/outputs" + "/" + model  if model!=None else ""
        rsfpath += "results/" + data + "_results/features" + "/" + model  if model!=None else ""
    
    # if type == "features":
    #     return rsfpath
    
        
    
    # if data == "RS":
    #     if not os.path.exists(PATH + "results/RS_results/model_performances/"):
    #         os.makedirs(PATH + "results/RS_results/model_performances")
    #     rspath += "results/RS_results/model_performances/"
    #     rsopath += "results/RS_results/outputs"
        
    # elif data == "stan_optimal":
    #     if not os.path.exists(PATH + "results/stan_results/model_performances/"):
    #         os.makedirs(PATH + "results/stan_results/model_performances")
    #     rspath += "results/stan_results/model_performances/"
    #     rsopath += "results/stan_results/outputs"
    
    # elif data == "LS":
    #     if not os.path.exists(PATH + "results/LS_results"):
    #         os.makedirs(PATH + "results/LS_results/model_performances")
    #     rspath += "results/LS_results/model_performances/"
    #     rsopath += "results/LS_results/outputs"
    
    if type == "performance":
        createF(rspath)
        return rspath + "/"
    elif type == "outputs":
        return rsopath
    elif type == "features":
        return rsfpath
        
    return rspath
        