import numpy as np
import itertools 
import os 
import argparse
import pathlib


PATH =  "/projectnb/skiran/saurav/Fall-2022/src2/"

datasets = ["RS", "FA", "PSW", "PSG", "DM", "LS", "stan_optimal"]

parameters = {
                "-CV" : ["kTkV"], #["LOO", "LFiveO", "kTkV"],
                "-model" : ["SVR", "RF"],#,"RF","AdaBoost"],#,"SVR"],#["RF", "SVR"], #["RF","SVR"], #["RF", "SVR"],
                "-metric" : ["all-metrics"],
                "-f" :  None,#[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127], #[10],#,20,25,40,60,80,105], #[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127]
                "-stratified":  [''],
                "-data" : None, #["RS"],#, "stan_optimal", "LS"],#, "stan_optimal", "LS"],#["RS", "stan_optimal", "LS"]
                "-features_R" : ["pearson"],#["pearson", "RFE"],
                "-frstep" : [1],
                "-approach" : ["EF"],#["LF"], #, "EF"]   # early fusion not implemented yet.
                "-level" : ["level1", "level2"]
                #['True', ''], # [True, ''],
                # "-same_split": ['True', ''], #[True, ''],
                # "-order": ["ascending", "descending"] #["ascending", "descending"]
}

features = {
            "stan_optimal" : [2,4,9,13,17],#,20],
            "RS" : [10,20,25,40,50,80,100,150,200,250,275,320,370,400,500],#,600,800,1000],
            "LS" : [1],#[5,10,20,25,40,50,80,100],
            "MM" : [len(datasets)],
            
            "FA" : [2,4,6,8,10,12],
            "PSW" : [2,4,8,12,16,20,25,32,36],
            "PSG" : [2,4,8,16,25,32,40,48,55,69],
            # "LS" : [1], # taking long time to run with SVR. Check later
            "DM" : [1,2,3]
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
    

def write_scripts(args, level, f2):
    
        
        if level == "level_1":
            parameters["-data"] = datasets 

        elif level == "level_2":
            combinations_datasets = get_dataset_combinations()
            # combinations_datasets.append("MM")
            parameters["-data"] = combinations_datasets

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
            path =  PATH + "shell_scripts/" 
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
                
            str_ = "python3 " + "-m cProfile -o " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".prof" + " scripts/main.py" 
            # str_ = "python3 " + "scripts/main.py"
            for j,p in enumerate(c):
                str_ += " " + param_ids[j] + " " + str(c[j])
              
            f.write(str_) 
            str_ = "\n" + "python3 -m flameprof " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".prof > " + PATH + "Profiler/" + fname[:-3] +"/" + fname[:-3] + ".svg" + "\n"
            f.write(str_)

            str_ = "nohup bash shell_scripts/" + "seperate-datasets/" if level == "level_1" else "nohup bash shell_scripts/" + "dataset-combinations/"             
            
            if i != len(combinations)-1:
                    f2.write(str_ + fname + " &" + "\n")
            else:
                    f2.write(str_ + fname + " &" + "\n")

            f.close()
            
            if level == "level_1":
                os.system("chmod +x " + path + "seperate-datasets/" + fname)
            elif level == "level_2":
                os.system("chmod +x " + path + "dataset-combinations/" + fname)

        os.system("chmod +x " + PATH + runFname +".sh")
        

      
      
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter makeFile Arguments")
    parser.add_argument("-d", type = str, help = "Modality : [ runSeperate, runCombined ] ")
    # parser.add_argument("-o", type = str, help = "Enter output file name")
    args = parser.parse_args()

    runFname = args.d

    f2 = open(PATH + runFname +".sh", "w")
    
    if args.d != "runCombined":
        parameters["-level"] = ["level1"]
        write_scripts(args, "level_1", f2)  # creates scripts for seperate dataset modalities to run in "shell_scripts/seperate-datasets"
    else:
        parameters["-level"] = ["level2"]
        write_scripts(args, "level_2", f2)
    # write_scripts(args, "level_2", f2)

    if args.d == "runSeperate": 
        f2.write("wait" + "\n")
        f2.write("python3 " + "writeFile.py" + " -level " + "level1" + "\n")
        f2.write("wait" + "\n")
        f2.write("python3 " + "scripts/combineOutputs.py" + " -level " + "level1")
    else:
        f2.write("wait" + "\n")
        f2.write("python3 " + "writeFile.py" + " -level " + "level2")

    f2.close()

    os.system("chmod +x " + PATH + runFname +".sh")

