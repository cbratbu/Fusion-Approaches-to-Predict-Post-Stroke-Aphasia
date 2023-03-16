from make import *
import os 

def writeTestShellFile(file, experiment=None, runType=None):

    if experiment == None:    
        file.write("#!/bin/bash -l" + "\n\n")
        
    
        file.write("# Set SCC project" + "\n")
        file.write("$ -P projectnb/skiran/saurav/Fall-2022/src2/" + "\n\n")
        
        file.write("# Request 28 CPUs" + "\n")
        file.write("#$ -pe omp 28" + "\n")
        file.write("#$ -l mem_per_core=1.2G" + "\n\n")
        
        file.write("#$ -l h_rt=70:00:00" + "\n")
        file.write("#$ -m beas" + "\n\n")
        
        file.write("module load python3/3.8.10" + "\n")
        file.write("module load pytorch/1.11.0" + "\n\n")
        
        # file.write("./make.sh" + "\n\n")
    
    if experiment != None: 
        file.write("./" + "experiment_scripts/" + experiment + "/" + runType + ".sh" + "\n")
        if runType == "runSeperate":
            file.write("wait" + "\n")
        
        
if __name__ == "__main__":

    for experiment in experiments:
        file = open(PATH + experiment + ".sh", "w")
        
        writeTestShellFile(file)
        writeTestShellFile(file, experiment, "runSeperate")
        writeTestShellFile(file, experiment, "runCombined")
        
        os.system("chmod +x " + PATH + experiment + ".sh")
        
        
        

    