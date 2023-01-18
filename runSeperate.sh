#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_3__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_5__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_7__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_10__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_20__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_25__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_40__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_50__RS_pearson_1.sh &
wait
python3 writeFile.py
python3 scripts/combineOutputs.py