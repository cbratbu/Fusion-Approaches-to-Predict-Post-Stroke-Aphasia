from libraries import *
from Model import * 
from getData import * 
import argparse
import os
import pathlib
from params import PATH
from utils import *


def save_file(model, Augmentation_settings):

    # result_save_path = PATH + "results/model_performances/"
    model_ = Augmentation_settings["model"]
    result_save_path = create_folder(Augmentation_settings["data"], "performance", model_)
    As = Augmentation_settings

    if As["Cross Validation Type"] == "kTkV" or As["metric"] == "all-metrics":
        cvr = model.cv_results_
    else:
        m = model.model
        cvr = pd.DataFrame(m.cv_results_)
    
    split_type = "same-split" if As["same split"] else "diff-split-cv"
    stratified = "NA" if As["stratified"]!=True else "stratified"
    FeatureElim = As["feature reduction"]
    # order = "" if As["stratified"]!=True else As["order"] 
    # fname = As["Cross Validation Type"] + "_" + As["model"] + "_" + As["metric"] + "_top" + str(As["top_k"]) + "frs_" + split_type + "_" + stratified + "_" + order +  ".csv"
    fname = As["Cross Validation Type"] + "_" + As["model"] + "_" + As["metric"] + "_top" + str(As["top_k"]) + "frs_" + split_type + "_" + stratified  + "_" + FeatureElim + ".csv"
    print("file name = ", fname)
    cvr.to_csv(result_save_path + fname)


if __name__ == "__main__":
    current_dir = pathlib.Path(__file__).parent.resolve()
    # os.chdir(current_dir)
    # print("path = ", current_dir)
    
    parser = argparse.ArgumentParser(description="enter network arguments")
    parser.add_argument("-CV", type = str, help = "available types : [ LOO, LFiveO, 5Fold, kTkV ] ")
    parser.add_argument("-model", type = str, help = "select model, available types : ['SVR', 'RF'] ")
    parser.add_argument("-metric", type = str, nargs = "?", help = "select metric, available types : ['MSE', 'MAE', 'all-metrics'] ", default = "all-metrics")
    parser.add_argument("-f", nargs = "?", type = int, help = "choose number of importance features", default = -1)
    parser.add_argument("-same_split", nargs = "?", type = bool, help = "only for normal CV setting. Same train-test split for different parameter sets", default = True)
    parser.add_argument("-verbose", nargs = "?", type = bool, help = "print cross validation update?", default = False)
    parser.add_argument("-stratified", nargs = "?", type = bool, help = "Stratified sampling [True/False], Default : False", default = False)
    parser.add_argument("-data", nargs = "?", type = str, help = "Choose data to train the models on [RS , WM-GM-CSF spared]", default = "RS")
    parser.add_argument("-features_R", nargs = "?", type = str, help = "feature reduction method [pearson , RFE]")
    parser.add_argument("-frstep", nargs = "?", type = int, help = "number of features reduced per step", default = 1)
    
    # parser.add_argument("-order", nargs = "?", type = str, help = "stratified [ascending/descending] order ", default = None)
    args = parser.parse_args()

                

    # print("args = ", args )
    # if 'top-K_features' not in args:
    #     args.top-K_features = None

    # print("verbose argument = ", args.verbose)
    # print("input metric = ", args.metric)
    # print("features inputed = ", args.f)
    Augmentation_settings = {
        "Cross Validation Type": args.CV,
        "model" : args.model,
        "metric" : args.metric, # not required anymore

        "Augment" : False, # not implemented yet
        # "transform" : True, # need to implement this now. 

        "verbose" : 3 if args.verbose else 0,    # dont change this. Taken care of 
        "top_k" : args.f if 'f' in args else "all",

        "repeat features" : False,
        "same split" :  args.same_split if 'same_split' in args else True, #implement false condition
        
        "stratified" : args.stratified,
        "data" : args.data,
        
        "feature reduction" : args.features_R,
        "features reduced per step" : args.frstep if 'frstep' in args else 1
        # "order" : args.order if 'stratified' in args else None, #implement false condition
    }

    
    # print("vals = ", Augmentation_settings["top_k"])
    
    model = Model(Augmentation_settings)
    save_file(model, Augmentation_settings)

