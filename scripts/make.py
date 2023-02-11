import numpy as np
import itertools 
import os 
import argparse
import pathlib


PATH =  "/projectnb/skiran/saurav/Fall-2022/src2/"

datasets = ["RS", "FA", "PSW", "PSG", "DM", "stan_optimal"] # "LS",
experiments = ["EXP-normal-all-data-imposter" ] # EXP-normal-all-data #"EXP-with-stans-features","EXP-without-stans-features", "EXP-without-stans-features-noFeatureReduction",  "all-data-stacked-TrainData", "EXP-stans-features", "EXP-all-data-stacked-F", "EXP-noStan-resting-state-reduce-SVR-A", "EXP-noStan-RS-PSW-PSG-reduce-RF-A"
# experiments = ["with_stans_features", "without_stans_features"]

parameters = {
                "-CV" : ["kTkV"], #["LOO", "LFiveO", "kTkV"],
                "-model" : ["RF", "SVR"], #, "SVR"],# "SVR"],#"SVR",["RF"],#,"RF","AdaBoost"],#,"SVR"],#["RF", "SVR"], #["RF","SVR"], #["RF", "SVR"],
                "-metric" : ["all-metrics"],
                "-f" :  None,#[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127], #[10],#,20,25,40,60,80,105], #[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127]
                "-stratified":  [''],
                "-data" : None, #["RS"],#, "stan_optimal", "LS"],#, "stan_optimal", "LS"],#["RS", "stan_optimal", "LS"]
                "-features_R" : ["pearson"], #["pearson", "RFE"],
                "-frstep" : [1],
                "-approach" : [ "EF", "LF"], # "LF"],# "LF"],# "EF"],# "EF"],# "EF",, "LF"],#, "EF"],#["LF"], #, "EF"]   # early fusion not implemented yet.
                "-level" : ["level1", "level2"],# "level2"],
                "-experiment" : None,
                "-feature_base" : ["entire-data"] #entire-data
                # "-experiment" : None
                #['True', ''], # [True, ''],
                # "-same_split": ['True', ''], #[True, ''],
                # "-order": ["ascending", "descending"] #["ascending", "descending"]
}

features = {
            "stan_optimal" : [20],#,20],
            "RS" : [10,20,25,40,50,80,100,150,200,250,275],#,320,370,400,500],#,600,800,1000],
            "LS" : [1],#[5,10,20,25,40,50,80,100],
            "MM" : [len(datasets)],
            
            "FA" : [2,4,6,8,10,12],
            "PSW" : [2,4,8,12,16,20,25,32,36],
            "PSG" : [2,4,8,16,25,32,40,48,55,69],
            # "LS" : [1], # taking long time to run with SVR. Check later
            "DM" : [1,2,3],
            
            "combined_features": [1290,1310,1330,1345]#[1160,1190,1220,1250,1270] #[920,970,1010,1050,1090,1120,1140]#[590,610,670,720,750,790,830,880]#[210,240,270,290,320,315,340,380,450,490,530,560] #[10,20,30,40,50,70,90,110,130,160,190] #,]
            }
            
def get_dataset_combinations():
    all_combinations = []
    for i in range(2,len(datasets)+1):
        temp = list( map(list, list(itertools.combinations(datasets, i))))
        all_combinations += temp 

    for i in range(len(all_combinations)):
        all_combinations[i] = "-".join(sorted(all_combinations[i]))
        
    len(all_combinations)
    # all_combinations.append("stan_optimal")
    return all_combinations
    

def get_different_combinations():
    total_combs = []
    for source in parameters["-data"]:
        parameters["-data"] = [source] 
        parameters["-f"] = features[source] if source in list(features) else [-1]
        combinations = list(itertools.product(*parameters.values()))
        total_combs += combinations
    return total_combs 
    

def write_scripts(args, level, f2, experiment):
    
        if "EXP-all-data-stacked" not in experiment:
            if level == "level_1":
                parameters["-data"] = datasets 
                
    
            elif level == "level_2":
                combinations_datasets = get_dataset_combinations()
                parameters["-data"] = combinations_datasets

        else:
            if level == "level_1":
                parameters["-data"] = ["combined_features"]
                
    
            elif level == "level_2":
                # combinations_datasets = get_dataset_combinations()
                parameters["-data"] = ["combined_features"]
            

        # if args.d == "runCombined":
        #     parameters["-data"] = ["MM"]
            
            
        combinations = get_different_combinations()

        # runFname = args.d
        # f2 = open(PATH + runFname +".sh", "w")
        
        param_ids = list(parameters)
        
        ######################################################################################################################################################
        # update from here.
        
        for i,c in enumerate(combinations):
            # print("c = ", c)
            # print(c[0], c[1], c[2], c[3])
            path =  PATH + "shell_scripts/" + experiment + "/"
            fname = ""
            for j,p in enumerate(c):
                if j != len(c)-1:
                    fname += str(c[j]) + "_"
                else:
                    fname += str(c[j]) + ".sh"
            
            print("file name = ", fname, "\n")

            if level == "level_1":
                pathlib.Path(path + "seperate-datasets/").mkdir(parents=True, exist_ok=True)
                f = open(path + "seperate-datasets/" + fname, "w")
            elif level == "level_2":
                pathlib.Path(path + "dataset-combinations/").mkdir(parents=True, exist_ok=True)
                f = open(path + "dataset-combinations/" + fname, "w")

            f.write("#!/bin/sh" + "\n")
            f2.write("#!/bin/sh" + "\n")
            
            if not os.path.exists(PATH + "Profiler/" + fname[:-3]):
                os.makedirs(PATH + "Profiler/" + fname[:-3])
                
            str_ = "python3 " + "-m cProfile -o " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".prof " + PATH + "scripts/main.py" 
            # str_ = "python3 " + "scripts/main.py"
            for j,p in enumerate(c):
                str_ += " " + param_ids[j] + " " + str(c[j])
              
            f.write(str_) 
            str_ = "\n" + "python3 -m flameprof " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".prof > " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".svg" + "\n"
            f.write(str_)

            str_ = "nohup bash " + PATH + "shell_scripts/" + experiment + "/" + "seperate-datasets/" if level == "level_1" else "nohup bash " +  PATH + "shell_scripts/" +  experiment + "/" + "dataset-combinations/"             
            
            if i != len(combinations)-1:
                    f2.write(str_ + fname + " &" + "\n")
            else:
                    f2.write(str_ + fname + " &" + "\n")

            f.close()
            
            if level == "level_1":
                os.system("chmod +x " + path + "seperate-datasets/" + fname)
            elif level == "level_2":
                os.system("chmod +x " + path + "dataset-combinations/" + fname)

        # os.system("chmod +x " + PATH + runFname +".sh")
        


def adjustParams(experiment):
    if "EXP-without-stans-features" in experiment or "noStan" in experiment:
        if "stan_optimal" in datasets:
            datasets.remove("stan_optimal")
    
    # if experiment == "EXP-without-stans-features-noFeatureReduction":
    #     if "stan_optimal" in datasets:
    #         datasets.remove("stan_optimal")
        # if experiment != "EXP-without-stans-features-imposter": # or experiment != "EXP-without-stans-features-imposter":
        #     features["stan_optimal"] = [20]
        #     features["RS"] = [1225]
        #     features["LS"] = [1]
        #     features["MM"] = [len(datasets)]
        #     features["FA"] = [12]
        #     features["PSW"] = [36]
        #     features["PSG"] = [69]
        #     features["DM"] = [3]
        
    parameters["-experiment"] = [experiment]
    
    if "EXP-all-data-stacked" in experiment:
        parameters["-data"] = ["combined_features"]
    
    if "resting-state-reduce" in experiment:
        
        features["RS"] = [1225]
        features["LS"] = [1]
        features["MM"] = [len(datasets)]
        features["FA"] = [12]
        features["PSW"] = [36]
        features["PSG"] = [69]
        features["DM"] = [3]
        features["stan_optimal"] = [20]
        
        if "SVR" in experiment:
            parameters["-model"] = ["SVR"]
            features["RS"] = [10,15,20,25,30,35,40,45,50,55,60,65,70] #[225,230,235,240,245,250,255,260,265,270,275,280] # #,
        if "RF" in experiment:
            parameters["-model"] = ["RF"]
            features["RS"] = [225,230,235,240,245,250,255,260,265,270,275,280] #[35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65]#,]
        
        
        
    if "RS-PSW-PSG" in experiment:

        features["RS"] = [1225]
        features["LS"] = [1]
        features["MM"] = [len(datasets)]
        features["FA"] = [12]
        features["PSW"] = [13,14,15,16,17,18,19]
        features["PSG"] = [13,14,15,16,17,18,19, 37,38,39,40,41,42,43,44]
        features["DM"] = [3]
        features["stan_optimal"] = [20]
        
        if "SVR" in experiment:
            parameters["-model"] = ["SVR"]
            features["RS"] = [225,230,235,240,245,250,255,260,265,270,275,280] #[10,15,20,25,30,35,40,45,50,55,60,65,70] # # #,
        if "RF" in experiment:
            parameters["-model"] = ["RF"]
            features["RS"] = [35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65] #[225,230,235,240,245,250,255,260,265,270,275,280] ##,]
        
    
    

      
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter makeFile Arguments")
    parser.add_argument("-d", type = str, help = "Modality : [ runSeperate, runCombined ] ")
    # parser.add_argument("-o", type = str, help = "Enter output file name")
    args = parser.parse_args()

    runFname = args.d

    for experiment in experiments:
        adjustParams(experiment)
        os.makedirs(PATH + "experiment_scripts/" + experiment + "/", exist_ok = True)
        f2 = open(PATH + "experiment_scripts/" + experiment + "/" + runFname +".sh", "w")
        
        if args.d != "runCombined":
            parameters["-level"] = ["level1"]
            # parameters["-experiments"] = [""]
            write_scripts(args, "level_1", f2, experiment)  # creates scripts for seperate dataset modalities to run in "shell_scripts/seperate-datasets"
        else:
            parameters["-level"] = ["level2"]
            # parameters["-"]
            write_scripts(args, "level_2", f2, experiment)
    # write_scripts(args, "level_2", f2)
    
        if args.d == "runSeperate": 
            f2.write("wait" + "\n")
            f2.write("python3 " + "writeFile.py" + " -level " + "level1" + " -experiment " + experiment + "\n")
            f2.write("wait" + "\n")
            f2.write("python3 " + "scripts/combineOutputs.py" + " -level " + "level1" + " -experiment " + experiment + "\n" )
            f2.write("wait" + "\n")
            f2.write("python3 " + "scripts/writeFeatures.py" + " -level " + "level1" + " -experiment " + experiment )
            
        else:
            f2.write("wait" + "\n")
            f2.write("python3 " + "writeFile.py" + " -level " + "level2" + " -experiment " + experiment + "\n")
            f2.write("wait" + "\n")
            f2.write("python3 " + "writeFeatures.py" + " -level " + "level2" + " -experiment " + experiment)
    
        f2.close()
        os.system("chmod +x " + PATH + "experiment_scripts/" + experiment + "/" + runFname +".sh")
        

    
