#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_3__MM_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_RF_all-metrics_3__MM_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_AdaBoost_all-metrics_3__MM_pearson_1.sh &
wait
python3 writeFile.py
python3 scripts/combineOutputs.py