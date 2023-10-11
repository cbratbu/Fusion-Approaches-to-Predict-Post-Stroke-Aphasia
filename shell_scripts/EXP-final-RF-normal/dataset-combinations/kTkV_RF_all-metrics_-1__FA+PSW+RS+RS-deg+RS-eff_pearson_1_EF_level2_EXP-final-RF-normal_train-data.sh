#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data.prof /projectnb/skiran/saurav/Fall-2022/src2/scripts/main.py -CV kTkV -model RF -metric all-metrics -f -1 -stratified  -data FA+PSW+RS+RS-deg+RS-eff -features_R pearson -frstep 1 -approach EF -level level2 -experiment EXP-final-RF-normal -feature_base train-data
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data/kTkV_RF_all-metrics_-1__FA+PSW+RS+RS-deg+RS-eff_pearson_1_EF_level2_EXP-final-RF-normal_train-data.svg
