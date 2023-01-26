

PATH = "/projectnb/skiran/saurav/Fall-2022/src2/"
PATH_DATA = "/projectnb/skiran/saurav/Fall-2022/RS/time_series"

SVR_params = {
    "kernel" : ("linear", "rbf"),
    "C" :  [1e-3,1e-2,1e-1,1,10], #200,500
    "epsilon" : [1e-4,1e-3,1e-2,1e-2,1,10],
    "tol" : [1e-5,1e-4,1e-3,1e-2,1],#1e-3,
    "gamma" : [1e-6,1e-5,1e-4,1e-3,1e-2,1e-1, 1] #1e-9,1e-8,
}

RFParams = {
    "max_depth" : [2,5,10,15,30,40,45], #40,50,70,90,100,200,500,700,1000,1500,2100],
    # "criterion" : (\"mse\", \"mae\", \"poisson\"),\n",
    "max_features" : ["log2", "sqrt", 0.1, 0.2, 0.3],
    "n_estimators" :[50,100, 150,250,300,500]#[50,100,200,300,500,1000]
    # "min_samples_split\" : [2,3,4,5,7,10,15]\n",
}

ABParams = {
    "n_estimators" : [20,50,100,150,300,400],
    "learning_rate" : [1e-4, 1e-3, 1e-2, 1e-2,1,10],
    "loss" : ("square", "linear")
}