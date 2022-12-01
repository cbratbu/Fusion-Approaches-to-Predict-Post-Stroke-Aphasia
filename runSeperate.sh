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
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_80__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_100__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_150__RS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_2__stan_optimal_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_4__stan_optimal_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_9__stan_optimal_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_13__stan_optimal_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_17__stan_optimal_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_5__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_10__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_20__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_25__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_40__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_50__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_80__LS_pearson_1.sh &
#!/bin/sh
nohup bash shell_scripts/kTkV_SVR_all-metrics_100__LS_pearson_1.sh &
wait
python3 writeFile.py
python3 scripts/combineOutputs.py