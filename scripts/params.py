

PATH = "/projectnb/skiran/saurav/Fall-2022/src2/"
PATH_DATA = "/projectnb/skiran/saurav/Fall-2022/RS/time_series"

# SVR_params = {
#     "kernel" : ("linear", "rbf"),
#     "C" :  [1e-3,1e-2,1e-1,1,10], #200,500
#     "epsilon" : [1e-4,1e-3,1e-2,1e-2,1,10],
#     "tol" : [1e-5,1e-4,1e-3,1e-2,1],#1e-3,
#     "gamma" : [1e-6,1e-5,1e-4,1e-3,1e-2,1e-1, 1] #1e-9,1e-8,
# }

SVR_params = {
    "kernel" : ("linear","rbf"),#("linear", "rbf"),
    "C" :  [1,10,50,200,500]
    "epsilon" : [1e-3, 1e-2,1e-1,1],
    "tol" : [1e-2,1,1e-2,1],#1e-3,
    "gamma" : [1e-2, 1e-6, 1e-2,1e-1, 1] #1e-9,1e-8,
}


RFParams = {
    "max_depth" : [7,2,5,10],#[2,5,10,15], #40,50,70,90,100,200,500,700,1000,1500,2100],
    # "criterion" : (\"mse\", \"mae\", \"poisson\"),\n",
    "max_features" : ["sqrt", "log2", 0.8], #[None, "log2", "sqrt", 0.1, 0.2, 0.3],
    "n_estimators" :[150,250,300],#[150,250,300]#[50,100,200,300,500,1000]
    # "min_samples_split\" : [2,3,4,5,7,10,15]\n",
}


# GBParams = {
#     "n_estimators" : [300], #400],#,50,100,150,300],
#     "learning_rate" : [1e-2],# 2e-2, 5e-3],#, 1e-3, 1e-3 * 5, 1e-2, 1e-2 * 5, 1e-2,1,10],
#     "feature_fraction" : [0.4],# 0.6, 0.8],#,0.8,0.7,0.4],
#     "bagging_fraction" : [0.8],# 0.7, 0.9],
#     "min_data_in_leaf" : [2],# 4, 6],
#     # "max_data_in_leaf" : [10],
#     "verbose" : [-1],
#     # "silent" : [True],
#     # "verbose_eval" : [-1],
#     "num_leaves" : [7],
#     "n_jobs" : [5],
#     # "boosting_type" : ("gbdt"),
#     "max_depth" : [4],# 6, 10, 14],#,5,8,13,17,22]
#     "metric" : ("l1")
# }

GBParams = {
    "n_estimators" : [150], #400],#,50,100,150,300],
    "learning_rate" : [1e-2, 2e-2],#, 1e-3, 1e-3 * 5, 1e-2, 1e-2 * 5, 1e-2,1,10],
    "feature_fraction" : [0.4, 0.8],#,0.8,0.7,0.4],
    "bagging_fraction" : [0.7],
    "min_data_in_leaf" : [2, 6],
    # "max_data_in_leaf" : [10],
    "verbose" : [-1],
    # "silent" : [True],
    # "verbose_eval" : [-1],
    "num_leaves" : [7],
    "n_jobs" : [-1],
    # "boosting_type" : ("gbdt"),
    "max_depth" : [4,14],#,5,8,13,17,22]
    "metric" : ("l1")
}


ABParams = {
    "n_estimators" : [20,50,100,150,300,400],
    "learning_rate" : [1e-4, 1e-3, 1e-2, 1e-2,1,10],
    "loss" : ("square", "linear")
}
