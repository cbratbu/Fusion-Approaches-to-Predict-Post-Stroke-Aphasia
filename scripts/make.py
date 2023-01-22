import numpy as np
import itertools 
import os 
import argparse


PATH =  "/projectnb/skiran/saurav/Fall-2022/src2/"
parameters = {
                "-CV" : ["kTkV"], #["LOO", "LFiveO", "kTkV"],
                "-model" : ["SVR","RF","AdaBoost"],#,"SVR"],#["RF", "SVR"], #["RF","SVR"], #["RF", "SVR"],
                "-metric" : ["all-metrics"],
                "-f" :  None,#[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127], #[10],#,20,25,40,60,80,105], #[5, 10,20,25,40,50,80,100,150,200,250,275,320,370,400,500,600,800,1000,1127]
                "-stratified":  [''],
                "-data" : ["RS", "stan_optimal", "LS"],#, "stan_optimal", "LS"],#["RS", "stan_optimal", "LS"]
                "-features_R" : ["pearson"],#["pearson", "RFE"],
                "-frstep" : [1]
                #['True', ''], # [True, ''],
                # "-same_split": ['True', ''], #[True, ''],
                # "-order": ["ascending", "descending"] #["ascending", "descending"]
}


features = {
            "stan_optimal" : [20],#,20],
            "RS" : [10,20,25,40,50,80,100,150,200,250,275,320],#,370,400,500,600,800,1000],
            "LS" : [5,10,20,25,40,50,80,100],
            "MM" : [3],
            }

def get_different_combinations():
    total_combs = []
    for source in parameters["-data"]:
        parameters["-data"] = [source] 
        parameters["-f"] = features[source]
        combinations = list(itertools.product(*parameters.values()))
        total_combs += combinations
    return total_combs 
    

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="enter makeFile Arguments")
        parser.add_argument("-d", type = str, help = "Modality : [ runSeperate, runCombined ] ")
        # parser.add_argument("-o", type = str, help = "Enter output file name")
        args = parser.parse_args()
    
        if args.d == "runCombined":
            parameters["-data"] = ["MM"]
            
        combinations = get_different_combinations()

        runFname = args.d
        f2 = open(PATH + runFname +".sh", "w")
        
        param_ids = list(parameters)
        
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
            # fname =  c[0] + "_" + c[1] + "_" + c[2] + "_" + str(c[3]) + ".sh"
            f = open(path + fname, "w")
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
            
            if i != len(combinations)-1:
                    f2.write("nohup bash shell_scripts/" + fname + " &" + "\n")
            else:
                    f2.write("nohup bash shell_scripts/" + fname + " &" + "\n")
                    f2.write("wait" + "\n")

            f.close()

            os.system("chmod +x " + path + fname)
            #  os.system("./" + fname)
        
        os.system("chmod +x " + PATH + runFname +".sh")
        
        #  write both below lines in second script 
        if args.d != "MM":
            
            f2.write("python3 " + "writeFile.py" + "\n")
            f2.write("python3 " + "scripts/combineOutputs.py")
        else:
            f2.write("python3 " + "writeFile.py")
        f2.close()
        
      
