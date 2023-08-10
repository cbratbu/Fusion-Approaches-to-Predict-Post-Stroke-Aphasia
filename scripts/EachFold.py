from libraries import * 
from params import * 
from getData import *
from models import *
pd.options.mode.chained_assignment = None


class EachFold:
    def __init__(self, settings):
        self.data = settings["data"]
        self.m = settings["model"]
        self.k = settings["num features"]
        
        self.init()
        
        
    def get_params_(self):
        """returns the combination of different model parameters
        Returns:
            list: combinations of different parameters.
        """
        self.parameters = allParams(self.m)
        self.param_keys = list(self.parameters)
        
        param_list = list(itertools.product(*self.parameters.values()))        
        return param_list

        
    def getData(self, dta):
        
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")]
        # outputs = outputs.reshape(len(outputs),1)
    
        data = {}

        data["DM"] = df["demographic_info"]
    
        featuresFAL = ["fa_avg_ccmaj", "fa_avg_ccmin", "fa_avg_lifof", "fa_avg_lilf", "fa_avg_lslf", "fa_avg_lunc", "fa_avg_larc"]
        featuresFAR = ["fa_avg_rifof", "fa_avg_rilf", "fa_avg_rslf", "fa_avg_runc", "fa_avg_rarc"]

        FA_L = df["average_FA_values"][featuresFAL].fillna(0).values
        FA_R = df["average_FA_values"][featuresFAR].fillna(df["average_FA_values"][featuresFAR].mean()).values
        data["FA"] = np.hstack((FA_L, FA_R))
        data["FA"] = pd.DataFrame(data["FA"], columns = featuresFAL + featuresFAR)
        
        data["PS_W"] = df["percent_spared_in_white_matter"]
        
        data["LS"] = df["lesion_size"]

        data["PS_G"] = df["percent_spared_in_gray_matter"]

        data["RS"] = df["restingstate_bivariate_correlations"]

        return data[dta], outputs
        
        
    def get_model(self, model, params=None):

        m = getModel(model)
        params = allParams(model) if params == None else params

        params = dict(zip(self.param_keys, params))
        return m(**params)



    def reduce(self, data, type, outputs=None, k=None):
        if type == "fit-reduce":
            # print(outputs)
            data["outputs"] = outputs
            # print(data)
            features = data.corr().iloc[-1,:-1]
            features = np.abs(features).sort_values(ascending=False)
            
            if k == None:
                self.top_features = features.index 
                return data.drop(["outputs"], axis = 1) 
            else:
                self.top_features = features.iloc[:k].index 
                return data[self.top_features]
            
        if type == "reduce":
            if k == None:
                return data 
            else:
                return data[self.top_features]
                


        ############################################################################################################################################################
        
        ############################################################################################################################################################
    



    def train_val_fold(self, data, outputs):
        kf = KFold(n_splits=10)
        param_list = self.get_params_()

        best_k = None
        best_model_params = None 
        bestValRMSE = 10000
        best_model_overall = None
        
        for k in tqdm(self.k):
            
            best_params = None
            best_model = None
            model_val_performance = 10000
                        
            for curr_param in param_list:                

                val_RMSE = 0

                curr_param_str = list(curr_param)
                ffileName = "_".join(str(e) for e in curr_param_str)
                
                os.makedirs(self.folder + "/" + str(k) + "-features/", exist_ok=True)
                self.feature_file_ = open(self.folder + "/" + str(k) + "-features/" + ffileName + ".csv", "w")
                self.feature_file = csv.writer(self.feature_file_, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
                
                for i, (train_index, val_index) in enumerate(kf.split(data)):
                    train_data = data.iloc[train_index]
                    train_outputs = outputs.iloc[train_index]

                    val_data = data.iloc[val_index]
                    val_outputs = outputs.iloc[val_index]

                    train_data = self.reduce(train_data, "fit-reduce", train_outputs, k)        
                    val_data = self.reduce(val_data, "reduce", k=k)
                    
                    self.feature_file.writerow(list(self.top_features))
                    
                    self.model = self.get_model(self.m, curr_param)                    
                    self.model.fit(train_data, train_outputs)
                    
                    val_predictions = self.model.predict(val_data)
                                        
                    val_RMSE += mean_squared_error(val_predictions, val_outputs, squared = False)
                    
                self.feature_file_.close()
                val_RMSE = val_RMSE/10
                
                if val_RMSE < model_val_performance:
                    model_val_performance = val_RMSE 
                    best_params = curr_param  # best parameter set for one 'K'
                    best_model = self.model

            if model_val_performance < bestValRMSE: 
                bestValRMSE = model_val_performance 
                best_k = k 
                best_model_params = best_params
                best_model_overall = best_model
        
        return best_model_overall, best_model_params, best_k, bestValRMSE            
        
        
        
        
                
    def train_test_fold(self, data, outputs):
        kf = KFold(n_splits=11)


        self.file_ = open("folds/" + "final.csv", "w", newline = '')
        self.file = csv.writer(self.file_, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
        self.file.writerow(["fold","Num Features", "Kernel", "C", "Epsilon", "tol", "gamma", "validation RMSE", "test RMSE"])
        
        self.featureFile_ = open("folds/" + "finalFeatures.csv","w", newline="")
        self.featureFile = csv.writer(self.featureFile_, delimiter =",", quotechar="|", quoting = csv.QUOTE_MINIMAL)
        self.featureFile.writerow(["Fold", "Features"])
        
        for i, (train_index, test_index) in enumerate(kf.split(data)):
            train_val_data = data.iloc[train_index, :]
            train_val_outputs = outputs.iloc[train_index]
            
            test_data = data.iloc[test_index, :]
            test_outputs = outputs.iloc[test_index]
            
            self.folder = "folds/fold-" + str(i+1)
            os.makedirs(self.folder, exist_ok=True)
            
            bestModel, bestParams, bestNumFeatures, valRMSE = self.train_val_fold(train_val_data, train_val_outputs)
            
            ffileName = "_".join(str(e) for e in bestParams)
            fname = self.folder + "/" + str(bestNumFeatures) + "-features/" + ffileName + '.csv' 
            tempData = pd.read_csv(fname)
            feature_counts = np.unique(tempData.values, return_counts=True)
    
            # Make prediction on test set here
            
            bestFeatureCounts, bestFeatureSet_ = zip(*sorted(zip(feature_counts[1],feature_counts[0] ), reverse=True))
            bestFeatureSet = list(bestFeatureSet_)[:bestNumFeatures]
            
            test_predictions = bestModel.predict(test_data[bestFeatureSet]) 
            testRMSE = mean_squared_error(test_predictions, test_outputs.values, squared=False)
            
            self.file.writerow(["fold-" +str(i),  bestNumFeatures] + list(bestParams) + [valRMSE, testRMSE] )
            self.featureFile.writerow(["fold-" + str(i)] + list(bestFeatureSet_))
            
        self.file_.close()
        self.featureFile_.close()        
    
    def init(self):
        data, outputs = self.getData("RS")  
        self.train_test_fold(data,outputs)
        
        
if __name__ == "__main__":
    
    settings = {
        "data" : "RS",
        "model" : "SVR",
        "num features" : [2,4,8,14,22,30,45,70,90,130,170,210,250,300]
    }
    
    ef = EachFold(settings)
        
        
    







