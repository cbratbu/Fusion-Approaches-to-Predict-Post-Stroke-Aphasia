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
        file.write("#$ -M saurav07@bu.edu" + "\n\n")
        
        file.write("module load python3/3.8.10" + "\n")
        file.write("module load pytorch/1.11.0" + "\n\n")
        
        # file.write("./make.sh" + "\n\n")
    
    if experiment != None: 
        # file.write("./" + "experiment_scripts/" + experiment + "/" + runType + ".sh" + "\n")
        file.write(PATH + "experiment_scripts/" + experiment + "/" + runType + ".sh" + "\n")
        if runType == "runSeperate":
            file.write("wait" + "\n")
        
        
if __name__ == "__main__":

    for experiment in experiments:
        
        rs = PATH + "experiment_scripts/" + experiment + "/" + "runSeperate" +".sh"
        with open(rs, 'r') as file:
            rslines = len(file.readlines())
        
        rsnumfs = int(rslines/20)+2
        
        cs = PATH + "experiment_scripts/" + experiment + "/" + "runCombined" +".sh"
        with open(cs, 'r') as file:
            cslines = len(file.readlines())
        csnumfs = int(cslines/20)+2
        
        
        os.makedirs(PATH + "experiment_jobs", exist_ok=True)
        os.makedirs(PATH + "submit_jobs", exist_ok=True)
        os.makedirs(PATH + "submit_jobs/" + experiment, exist_ok=True)
        
        os.makedirs(PATH + "experiment_jobs/" + experiment + "/" + "seperate_jobs", exist_ok=True)
        os.makedirs(PATH + "experiment_jobs/" + experiment + "/" + "combined_jobs", exist_ok=True)
        
        
        file2 = open(PATH + "submit_jobs/" + experiment + "/" + "seperate_jobs.sh", "w")
        for i in range(1,rsnumfs, 1):
            file = open(PATH + "experiment_jobs/" + experiment + "/" + "seperate_jobs/" + experiment + "_" + str(i) + ".sh", "w")
            writeTestShellFile(file)
            writeTestShellFile(file, experiment, "runSeperate_" + str(i))
            os.system("chmod +x " + PATH + "experiment_jobs/" + experiment + "/" + "seperate_jobs/" + experiment + "_" + str(i) + ".sh")
            
            if i != rsnumfs-1:
                file2.write("qsub " + PATH + "experiment_jobs/" + experiment + "/" + "seperate_jobs/" + experiment + "_" + str(i) + ".sh" + "\n")
            else:
                # file2.write("wait" + "\n")
                file2.write("qsub " + PATH + "experiment_jobs/" + experiment + "/" + "seperate_jobs/" + experiment + "_" + str(i) + ".sh" + "\n")
                
        file2.close()
            
                
            
            
            
        file2 = open(PATH + "submit_jobs/" + experiment + "/" + "combined_jobs.sh", "w")
            
        for i in range(1,csnumfs, 1):
            file = open(PATH + "experiment_jobs/" + experiment + "/" + "combined_jobs/" + experiment + "_" + str(i) + ".sh", "w")
            writeTestShellFile(file)
            writeTestShellFile(file, experiment, "runCombined_" + str(i))
            os.system("chmod +x " + PATH + "experiment_jobs/" + experiment + "/" + "combined_jobs/" + experiment + "_" + str(i) + ".sh")

            
            if i != csnumfs-1:
                file2.write("qsub " + PATH + "experiment_jobs/" + experiment + "/" + "combined_jobs/" + experiment + "_" + str(i) + ".sh" + "\n")
            else:
                # file2.write("wait" + "\n")
                file2.write("qsub " + PATH + "experiment_jobs/" + experiment + "/" + "combined_jobs/" + experiment + "_" + str(i) + ".sh" + "\n")

        file2.close()        
        
        os.system("chmod +x " + PATH + "submit_jobs/" + experiment + "/" + "seperate_jobs.sh")
        
        os.system("chmod +x " + PATH + "submit_jobs/" + experiment + "/" + "combined_jobs.sh")
        
        file3 = open(PATH + experiment + ".sh", "w")
        file3.write("./submit_jobs/" + experiment + "/" + "seperate_jobs.sh" + "\n")
        
        
        
        file3.write("./submit_jobs/" + experiment + "/" + "combined_jobs.sh" + "\n")
        file3.close()
        
        
        

    
