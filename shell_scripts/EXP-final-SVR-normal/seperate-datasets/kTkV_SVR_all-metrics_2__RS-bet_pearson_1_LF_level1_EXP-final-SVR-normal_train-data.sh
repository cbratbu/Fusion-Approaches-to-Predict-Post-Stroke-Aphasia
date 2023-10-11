#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model SVR -metric all-metrics -f 2 -stratified  -data RS-bet -features_R pearson -frstep 1 -approach LF -level level1 -experiment EXP-final-SVR-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data/kTkV_SVR_all-metrics_2__RS-bet_pearson_1_LF_level1_EXP-final-SVR-normal_train-data.svg
