#!/bin/sh
python3 -m cProfile -o /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_20__LS_RFE_1/kTkV_SVR_all-metrics_20__LS_RFE_1.prof scripts/main.py -CV kTkV -model SVR -metric all-metrics -f 20 -stratified  -data LS -features_R RFE -frstep 1
python3 -m flameprof /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_20__LS_RFE_1/kTkV_SVR_all-metrics_20__LS_RFE_1.prof > /projectnb/skiran/saurav/Fall-2022/src2/Profiler/kTkV_SVR_all-metrics_20__LS_RFE_1/kTkV_SVR_all-metrics_20__LS_RFE_1.svg
