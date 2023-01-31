import numpy as np
import itertools 
import os 
import argparse
import pathlib

"""make scripts that run in parallel. Makes it faster to do the work.

Returns: shell scripts
    _type_: .sh files in ../shell_scripts
"""


PATH =  "/Users/saurav/Desktop/Margrit/Fall-22/WAB-prediction/"

datasets = ["RS", "FA", "PSW", "PSG", "LS", "DM", "stan_optimal"]

parameters = {
                "-CV" : ["kTkV"], #["LOO", "LFiveO", "kTkV"],
                "-model" : ["SVR", "RF"],#["RF", "SVR"], #["RF","SVR"], #["RF", "SVR"],
                "-metric" : ["all-metrics"],
                "-f" :  None,#[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127], #[10],#,20,25,40,60,80,105], #[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127]
                "-stratified":  [''],
                "-data" : None, #[ "RS", "stan_optimal", "LS"],
                "-features_R" : ["pearson"],#["pearson", "RFE"],
                "-frstep" : [1]
                #['True', ''], # [True, ''],
                # "-same_split": ['True', ''], #[True, ''],
                # "-order": ["ascending", "descending"] #["ascending", "descending"]
}



features = {
            "stan_optimal" : [2,4,9,13,17],#,20],
            "RS" : [10,20,25,40,50,80,100,150],#,200,250,275,320,370,400,500,600,800,1000],
            "LS" : [5,10,20,25,40,50,80,100],
            "MM" : [3],
            
            "FA" : [2,4,6,8,10,12],
            "PSW" : [2,4,8,12,16,20,25,32,36],
            "PSG" : [2,4,8,16,25,32,40,48,55,69],
            "LS" : [1],
            "DM" : [1,2,3]
            }

def get_dataset_combinations():
    all_combinations = []
    for i in range(2,len(datasets)+1):
        temp = list( map(list, list(itertools.combinations(datasets, i))))
        all_combinations += temp 

    for i in range(len(all_combinations)):
        all_combinations[i] = "-".join(all_combinations[i])
        
    len(all_combinations)
    all_combinations.append("stan_optimal")
    return all_combinations


def get_different_combinations():
    total_combs = []
    for source in parameters["-data"]:
        parameters["-data"] = [source] 
        if source in features:
            parameters["-f"] = features[source]
        else:
            parameters["-f"] = [-1]
        combinations = list(itertools.product(*parameters.values()))
        total_combs += combinations
    return total_combs 


        
def write_scripts(args, level, f2):
    

        if level == "level_1":
            parameters["-data"] = datasets 

        elif level == "level_2":
            combinations_datasets = get_dataset_combinations()
            parameters["-data"] = combinations_datasets

        if args.d == "runCombined":
            parameters["-data"] = ["MM"]

        combinations = get_different_combinations()
            
        # pathlib.Path(PATH ).mkdir(parents=True, exist_ok=True)
    
        param_ids = list(parameters)
        
        for i,c in enumerate(combinations):
            # print("c = ", c)
            # print(c[0], c[1], c[2], c[3])
            path =  PATH + "shell_scripts/" 
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            fname = ""
            for j,p in enumerate(c):
                if j != len(c)-1:
                    fname += str(c[j]) + "_"
                else:
                    fname += str(c[j]) + ".sh"
            
            print("file name = ", fname, "\n")
            # fname =  c[0] + "_" + c[1] + "_" + c[2] + "_" + str(c[3]) + ".sh"
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

            # f.write("python3 " + "scripts/main.py -CV "+ str(c[0]) + " -model " + str(c[1]) 
            #         + " -metric " + str(c[2]) + " -f" + str(c[3]) +
            #         " -same_split False")
            str_ = "nohup bash shell_scripts/" + "seperate-datasets/" if level == "level_1" else "nohup bash shell_scripts/" + "dataset-combinations/"             

            if i != len(combinations)-1:
                    f2.write(str_ + fname + " &" + "\n")
            else:
                    f2.write(str_ + fname + " &" + "\n")
                    # f2.write("wait" + "\n")

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

    write_scripts(args, "level_1", f2)  # creates scripts for seperate dataset modalities to run in "shell_scripts/seperate-datasets"
    # write_scripts(args, "level_2", f2)

    if args.d != "MM": 
        f2.write("python3 " + "writeFile.py" + "\n")
        f2.write("python3 " + "scripts/combineOutputs.py")
    else:
        f2.write("python3 " + "writeFile.py")

    f2.close()

    os.system("chmod +x " + PATH + runFname +".sh")


     
