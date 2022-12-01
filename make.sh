#!/bin/sh 

python3 scripts/make.py -d runSeperate 
# python3 writeFile.py
# python3 combineOutputs.py

python3 scripts/make.py -d runCombined 
# python3 writeFile.py
# python3 combineOutputs.py
