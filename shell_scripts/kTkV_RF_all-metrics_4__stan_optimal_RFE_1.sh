#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_4__stan_optimal_RFE_1/kTkV_RF_all-metrics_4__stan_optimal_RFE_1.prof scripts/main.py -CV kTkV -model RF -metric all-metrics -f 4 -stratified  -data stan_optimal -features_R RFE -frstep 1
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_4__stan_optimal_RFE_1/kTkV_RF_all-metrics_4__stan_optimal_RFE_1.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_RF_all-metrics_4__stan_optimal_RFE_1/kTkV_RF_all-metrics_4__stan_optimal_RFE_1.svg
