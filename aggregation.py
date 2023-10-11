import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="enter experiment")
    parser.add_argument("-exp", type = str)
    parser.add_argument("-lev", type = int)
    args = parser.parse_args()
    
    experiment = args.exp
    level = args.lev
    
    if level == 1:
        os.system("python3 writeFile.py -level level1 -experiment " + experiment)
        os.system("wait")
        os.system("python3 scripts/combineOutputs.py -level level1 -experiment " + experiment)
        os.system("wait")
        os.system("python3 scripts/writeFeatures.py -level level1 -experiment " + experiment)
    
    if level == 2:
        os.system("python3 writeFile.py -level level2 -experiment " + experiment)
        os.system("wait")
        os.system("python3 scripts/combineOutputs.py -level level2 -experiment " + experiment)
        os.system("wait")
        os.system("python3 extractResults.py -experiment " + experiment)
            