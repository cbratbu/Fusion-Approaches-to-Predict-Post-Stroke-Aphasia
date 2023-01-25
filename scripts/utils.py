from libraries import * 
from params import PATH

def createF(path):
    if not os.path.exists( path):
        os.makedirs(path,exist_ok=True)

def create_folder(data, type = None, model = None):
    
    rspath = PATH 
    rsopath = PATH
    rsfpath = PATH
    
    model_path = model if model != None else ""
    
    if data == "stan_optimal":
        # if not os.path.exists(PATH + "results/stan_results/model_performances"):
        #     os.makedirs(PATH + "results/stan_results/model_performances")
        rspath += "results/stan_results/" + model_path + "_predictions" + "/model_performances" 
        rsopath += "results/stan_results/" + model_path + "_predictions" + "/outputs" 
        rsfpath += "results/stan_results/" + model_path + "_predictions" + "/features" 
        
    
    else:
        # if not os.path.exists(PATH + "results/" + data + "_results/model_performances"):
        #     os.makedirs(PATH + "results/" + data + "_results/model_performances")
        rspath += "results/"+ data+ "_results/" + model_path + "_predictions" + "/model_performances" 
        rsopath += "results/" + data + "_results/" + model_path + "_predictions" + "/outputs" 
        rsfpath += "results/" + data + "_results/" + model_path + "_predictions" + "/features" 
    
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
        