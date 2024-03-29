from getData import *
from models import *
from params import *
from utils import *
import sys, pickle
# warnings.filterwarnings('ignore')

class Model:
    def __init__(self, settings):
        self.cv = settings["Cross Validation Type"]
        self.metric = settings["metric"]
        self.repeat_features = settings["repeat features"]
        self.m = settings["model"]
        self.verbose = settings["verbose"]
        if self.cv != "kTkV" and self.metric != "all-metrics":
            print("original model = ", settings["model"], " ---- ")
            self.model = self.get_model(settings["model"])
        self.pca = PCA(n_components=2)
        self.stratified = settings["stratified"]
        # self.order = settings["order"]
        self.same_split = settings["same split"]
        self.num_features = settings["top_k"]
        self.approach = settings["approach"]
        self.level = settings["level"]
        self.experiment = settings["experiment"]
        self.feature_base = settings["feature base"]

        
        self.feature_reduction = settings["feature reduction"]
        self.FR_step = settings["features reduced per step"]
        
        self.source = settings["data"]
        self.init(settings)
        
        

    def save_performance(self):
        
            # result_save_path = PATH + "results/model_performances/"
        model_ = self.m
        level_ = self.level
        approach_ = self.approach
        experiment_ = self.experiment
        result_save_path = create_folder(self.source, "performance", model_, level_, approach_, experiment_, self.fold)
        # As = Augmentation_settings
    
        if self.cv == "kTkV" or self.metric == "all-metrics":
            cvr = self.cv_results_
        else:
            m = model.model
            cvr = pd.DataFrame(self.cv_results_)
        
        split_type = "same-split" if self.same_split else "diff-split-cv"
        stratified = "NA" if self.stratified!=True else "stratified"
        FeatureElim = self.feature_reduction
        # order = "" if As["stratified"]!=True else As["order"] 
        # fname = As["Cross Validation Type"] + "_" + As["model"] + "_" + As["metric"] + "_top" + str(As["top_k"]) + "frs_" + split_type + "_" + stratified + "_" + order +  ".csv"
        fname = self.cv + "_" + self.m + "_" + self.metric + "_top" + str(self.num_features) + "frs_" + split_type + "_" + stratified  + "_" + FeatureElim + ".csv"
        # print("file name = ", fname)
        cvr.to_csv(result_save_path + fname)

    def saveImpCols(self):
        
        if self.feature_reduction == "pearson":
            self.outputs = self.outputs.reshape(self.outputs.shape[0], 1)
            self.data = np.hstack((self.data, self.outputs))
            self.data = pd.DataFrame(self.data)
    
            corrs = self.data.corr().abs()
            corrs = corrs.fillna(0)
            self.importances = corrs.values[-1][:-1]
    
            self.top_columns = np.argpartition(importances, -self.num_features)[-self.num_features:]
    
            important_columns = self.all_features[self.top_columns]
        
        # important columns stored in training loop.
        
        imps = self.importances[self.top_columns]
        
        df = {
            "columns" : important_columns,
            "importances" : imps
        }
        
        df = pd.DataFrame(df)
        self.bfi = df

    def reduce(self):
        self.data = self.data.iloc[:,self.top_columns]
        self.outputs = self.outputs.ravel()
        self.data = self.data.values
        

    def init(self, augmentation_settings): # gets the data to train and test
        GET = getData(augmentation_settings)
        self.all_features, self.data, self.outputs = GET.data()
        self.all_features = pd.Index(self.all_features)
        self.outputs = self.outputs.ravel()

        # print("data source = ", self.source)
        # print("data shape = ", self.data.shape)
        # print("outputs shape = ", self.outputs.shape)
        # print("all features shape here = ", len(self.all_features))
        # print("features", self.num_features)
        
##################################################################################################

        # if self.feature_base == "entire-data" or (self.num_features == -1):
        #     self.saveImpCols()
            
        #     if self.num_features != -1:
        #         if self.data.shape[1] != 1:
        #             self.reduce()
        #     else:
        #         self.data = self.data.iloc[:,:-1]
        #         self.data = self.data.values
        #         self.outputs = self.outputs.ravel()
                
            # else:
                
            #     # print("reduction done")
            #     # print("data shape now = ", self.data.shape)
            # if self.stratified == True:
            #     self.data = pd.DataFrame(self.data)
            #     self.data["outputs"] = self.outputs 
            #     # if self.order =="ascending":
            #     self.data = self.data.sort_values(by = "outputs", ascending = True)
            #     # elif self.order == "descending":
            #         # self.data = self.data.sort_values(by = "outputs", ascending = False)
            #     self.outputs = self.data["outputs"].values
            #     self.data = self.data.drop(["outputs"], axis = 1)
            #     self.data = self.data.values
            


        self.forward()


    def CV_(self):
        if self.cv == "LOO":
            return 55
        elif self.cv == "LFiveO":
            return 11
        elif self.cv == "5Fold":
            return 5
        elif self.cv == "kTkV":
            return 10

    def correct_metric(self):
        if self.metric == "MSE":
            self.metric = "neg_mean_squared_error"
        elif self.metric == "MAE":
            self.metric = "neg_mean_absolute_error"
            

    def get_model(self, model, params=None):

        m = getModel(model)
        params = allParams(model) if params == None else params

        if self.cv != "kTkV" and self.metric != "all-metrics":
            self.correct_metric()
            return GridSearchCV( m(), params, cv= self.CV_(), scoring = self.metric , return_train_score = True, verbose = self.verbose)
        else:
            params = dict(zip(self.param_keys, params))
            return m(**params)

# the following functions are not necessary as of now
##################################################################################################################################################################
    # def train(self, data, outputs):
    #     self.model.fit(data, outputs)

    # def predict(self, data):
    #     return self.model.predict(data)

    # def get_score(self,data,outputs, return_ = False): #gives out R2 scores
    #     print("R2 fit score = ", self.model.score(data, outputs), "\n" )
    #     if return_:
    #         return self.model.score(data, outputs)

    # def CrossValResults(self):
    #     print(self.model.cv_results_)
    #     print('\n')

    # def modify_data(self, data):
    #     self.pca.fit(data)
    #     raise NotImplementedError()

    # def get_data(self):
    #     X_train, X_test, y_train, y_test = train_test_split( self.data, self.outputs, test_size=0.09, random_state=42)

    #     if self.cv != "kTkV":
    #         X_train, y_train = self.data, self.outputs

    #     print("train data shape = ", X_train.shape)
    #     print("train labels shape = ", y_train.shape, "\n")

    #     print("test data shape = ", X_test.shape)
    #     print("test labels shape = ", y_test.shape, "\n")

    #     return X_train, X_test, y_train, y_test

    # def oneMetric_cv(self):
    #     X_train, X_test, y_train, y_test = self.get_data()
    #     self.train(X_train, y_train)

    #     print("training performance")
    #     self.get_score(X_train, y_train)
    #     self.train_predictions_ = self.predict(X_train)
    #     # self.test_predictions_ = self.predict(X_test)
##################################################################################################################################################################    



    def important_columns(self, data, outputs): 
        """This function finds the names of important features in the data, either based on two factors
            - Pearson Correlation with WAB scores 
            - Recurrent Feature Elimination (RFE)

        Args:
            data (numpy array): Input data without output column
            outputs (numpy array): 1D array of WAB scores / any other output

        Returns:
            numpy array : finds the column index numbers and returns it 
        """
        
        if self.feature_reduction == "pearson":

            outputs = outputs.reshape(outputs.shape[0], 1)
            data = np.hstack((data, outputs))
            data = pd.DataFrame(data)
    
            corrs = data.corr().abs()
            corrs = corrs.fillna(0)
            importances = corrs.values[-1][:-1]
    
            top_columns = np.argpartition(importances, -self.num_features)[-self.num_features:]
            return top_columns
            
        elif self.feature_reduction == "RFE":

            self.rfe = RFE(self.model, n_features_to_select = self.num_features, step=2)#self.FR_step)
            self.rfe = self.rfe.fit(data, outputs)
            features = np.arange(data.shape[1])
            features = features[self.rfe.ranking_==1]
            return features

    def reduce_data(self, data):
        """filter important columns from the input data

        Args:
            data (numpy array): Input data without output columns

        Returns:
            numpy array: Input data with selected top features
        """
        
        data = pd.DataFrame(data)
        if self.feature_reduction == "pearson":
            data = data.iloc[:,self.top_columns]
        elif self.feature_reduction == "shap":
            data = data[self.top_columns]
        return data.values
        
        
    def get_KFfname(self):
        """create a csv file name based on model parameter setting

        Returns:
            string: csv file name based on the model parameters 
        """
        
        fname = ""
        for i,param in enumerate(self.param_keys):
            fname += "[" + param[0] + "-" + str(self.curr_param[i]) + "]_" 
        fname = fname[:-1] + ".csv"
        return fname
        
            
    def get_folder_name(self, fname):
        """creates a folder with the training setting in the results folder

        Args:
            fname (string): csv file name to store model parameter-wise outputs

        Returns:
            string: folder_name + file_name to save model parameter-wise outputs. 
        """
        
        # print("experiment = ", self.experiment)
        
        path = create_folder(self.source, fname, self.m, self.level, self.approach, self.experiment, self.fold)
        stratified = "" if self.stratified!=True else "stratified"
        fname = self.cv + "_" + self.m + "_" + self.metric + "_top" + str(self.num_features) + "frs_" + self.feature_reduction + "_"
        return path + "/" + fname[:-1]
    
    
    def features_init(self):
        """creates a folder to save outputs of important features

            Initiate the csv writer to write the features in a file during cross validation

        """
        folder = self.get_folder_name("features")
        if not os.path.exists(folder):
            os.makedirs(folder,exist_ok=True)
        file = self.get_KFfname()

        if self.feature_base == "entire-data":
            self.bfi.to_csv( folder + "/" + "important_features.csv")
        self.writerfile = open( folder + "/" + file , 'w', newline='')
        self.feature_writer = csv.writer(self.writerfile, delimiter=' ',  quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        
    def save_features(self):
        """writes the important features to a csv file using the csv-writer
        
        """
        
        if self.feature_reduction == "pearson":
            features = self.all_features[self.top_columns]
            self.feature_writer.writerow(list(features.values))
                
        elif self.feature_reduction == "shap":
            # features = self.top_columns
            self.feature_writer.writerow(self.top_columns)
            
        
    
    def feature_close(self):
        """Closes the csv-writer to complete writing important features to a file
        """
        self.writerfile.close()


    def save_file(self, cumulative_validate_predictions, cumulative_ground_truths):
        """saves the predictions and ground truth values for each model setting for each training setting.

        Args:
            cumulative_validate_predictions (list[float]): list of predictions for each patient
            cumulative_ground_truths (list[float]): list of ground truth scores for each patient
        """
        
        cumulative_validate_predictions = list(cumulative_validate_predictions)
        cumulative_ground_truths = list(cumulative_ground_truths)
        
        # cumulative_validate_predictions = list(itertools.chain(*cumulative_validate_predictions))
        # cumulative_ground_truths = list(itertools.chain(*cumulative_ground_truths))
        
        predictions = {
            "predictions" : cumulative_validate_predictions,
            "ground truth score": cumulative_ground_truths,
        }
        folder_name = self.get_folder_name("outputs")
        
        if not os.path.exists(folder_name ):
            os.makedirs(folder_name,exist_ok=True)
        
        predictions = pd.DataFrame(predictions)
        self.kFfname = self.get_KFfname()

        predictions.to_csv(folder_name + "/" + self.kFfname)   
        


    def get_class_labels(self, splits, outputs):
        """Helper function. Used in stratifold setting. Not important for regular setting. 

        Args:
            splits (int): number of buckets in training data during k-Fold CV
            outputs (array[float]): WAB scores of each patient. 

        Returns:
            array[float]: labels of each training example before splitting the data.
        """
        x = np.ones(len(outputs))
        
        counter = 0
        counter_update = int(len(outputs)/splits)
        adder = 0
        
        while(counter < len(outputs)):
            x[counter:counter + counter_update] += adder 
            adder += 1
            counter += counter_update 
            
        return x 
            


    def validate(self, data, outputs, kf2 = None):
        """Does Cross valiation for kTkV training setting, Training for other settings

        Args:
            data (numpy array): input data
            outputs (numpy array): WAB scores / output values
            kf2 (cross validation setting, optional): kFold CV object as input. If not given, creates 10-Fold CV. Defaults to None.

        Returns:
            float, float, float, float, object: train MSE mean, Validate MSE mean, train MAE mean, validate MAE mean, Best validate model
        """

        ##################################################################################################################################################################
        # Do not disturb the following few lines on k-fold setting
        if kf2 != None: 
            if self.stratified:
                class_labels = self.get_class_labels(splits = 5, outputs = outputs)
            else:
                class_labels = outputs
        else:
            if self.stratified != True: 
                if self.cv != "LOO":
                    # kf2 = KFold(n_splits=self.CV_(), shuffle = False) ## Change Here
                    if "normal" in self.experiment:
                        kf2 = KFold(n_splits=self.CV_(), shuffle=False)
                    else:
                        kf2 = KFold(n_splits = len(data), shuffle=False)
                    class_labels = outputs
            else:
                
                kf2 = StratifiedKFold(n_splits=self.CV_(), shuffle = False)
                class_labels = self.get_class_labels(splits = 5, outputs = outputs)

            if self.cv == "LOO":
                kf2 = KFold(n_splits=self.CV_(), shuffle=False) ## Change Here
                class_labels = outputs
                
        ##################################################################################################################################################################
        train_performance = []
        train_performance_MAE = []

        validate_performance = []
        validate_performance_MAE = []

        models = []

        mean_train_MSE = []
        mean_validate_MSE = []
        mean_test_MSE = []
        
        cumulative_validate_predictions = []
        cumulative_ground_truths = []

        maxLoss = 1000 # some arbitrary max loss value for RMSE
        self.best_features = None #to keep track of best features
        best_features = []

        # nanvalues = data.isna().sum().sum()
        # print("nan value count = ", nanvalues)
        
        for train_index, validate_index in kf2.split(data, class_labels):

            X_train, X_validate = data.iloc[train_index], data.iloc[validate_index]
            y_train, y_validate = outputs[train_index], outputs[validate_index]

            # print("X_train shape = ", X_train.shape)
            # print("X_validate shape = ", X_validate.shape)

            self.model = self.get_model(self.m, self.curr_param) # gets the model initialization of "m" type and "curr_param" parameters
            
            if self.level == "level1":
                if self.feature_base == "train-data":        
                    if self.num_features!=-1:
                        if self.feature_reduction != "shap": 
                            self.top_columns = self.important_columns(X_train,y_train)
                        elif self.feature_reduction == "shap":
                            shapModel = self.get_model(self.m, self.curr_param)
                            shapModel.fit(X_train, y_train)
                            if self.m == "SVR":
                                if self.curr_param[0] == "linear":                                    
                                    #explainer = shap.LinearExplainer(shapModel, X_train, feature_perturbation = "independent")
                                    explainer = shap.Explainer(shapModel, X_train, algorithm="linear", feature_perturbation="interventional")
                                    shap_values = explainer.shap_values(X_validate)
                                elif self.curr_param[0] == "rbf":                                                                
                                    explainer = shap.KernelExplainer(shapModel.predict, shap.sample(X_train, 20))
                                    shap_values = explainer.shap_values(X_validate)
                            elif self.m == "RF":
                                explainer = shap.Explainer(shapModel, X_train)
                                shap_values = explainer.shap_values(X_validate, check_additivity=False)

                            op = pd.DataFrame((zip(X_train.columns[np.argsort(np.abs(shap_values).mean(0))], np.abs(shap_values).mean(0))), columns = ["feature", "importance"]).sort_values(by="importance", ascending=False)
                            self.top_columns = op.iloc[:self.num_features]["feature"].values 
                            # print("top columns = ", self.top_columns)
                            self.bfi = op
                        X_train = self.reduce_data(X_train)
                        X_validate = self.reduce_data(X_validate)
    
                self.save_features() # saving features for each validation fold
                best_features.append(self.top_columns)
    
            if self.m == "GradBoost":
                self.model.fit(X_train, y_train, 
                                eval_set = [(X_validate, y_validate)],
                                eval_metric = "l1",
                                # verbose=False,
                                # early_stopping_rounds = 150
                                callbacks = [lgb.early_stopping(150, verbose=-1), lgb.log_evaluation(period=-1)]
                                )
            else:
                self.model.fit(X_train, y_train)
                
            train_predictions = self.model.predict(X_train)
            validate_predictions = self.model.predict(X_validate)
            
            if self.cv != "kTkV":
                cumulative_validate_predictions.append(validate_predictions)
                cumulative_ground_truths.append(y_validate)

            models.append(self.model)

            

            # if mean_squared_error(validate_predictions,y_validate,squared=False) < maxLoss:
            #     maxLoss = mean_squared_error(validate_predictions,y_validate,squared=False)
            #     self.best_features = self.top_columns 
                
            train_performance.append(mean_squared_error(train_predictions, y_train, squared=False))
            validate_performance.append(mean_squared_error(validate_predictions,y_validate,squared=False))

            train_performance_MAE.append(mean_absolute_error(train_predictions, y_train))
            validate_performance_MAE.append(mean_absolute_error(validate_predictions,y_validate))


        # model = models[np.argmin(validate_performance)]
        # self.top_columns = self.best_features

        return np.mean(train_performance), np.mean(validate_performance), np.mean(train_performance_MAE), np.mean(validate_performance_MAE), models, best_features


    def train_kTkV(self):
        """Training loop for kTkV setting. Initiates Training set and Testing set here. Sends training data to validate function.

        Returns:
            float, float, float, float, float, float, object: trainMSE, testMSE, valMSE, trainMAE, valMAE, testMAE, best test model.
        """
        
        
        if self.stratified!=True:
            if "normal" in self.experiment:
                kf = KFold(n_splits=11, shuffle = False) ## Change Here
            else:
                kf = KFold(n_splits=len(self.data), shuffle = False)
            class_labels = self.outputs
        else:
            kf = StratifiedKFold(n_splits=11, shuffle = False)
            class_labels = self.get_class_labels(splits=5, outputs = self.outputs)

        
        

        count = 1
        for train_index, test_index in kf.split(self.data, class_labels):

            train_performances = []
            train_performances_MAE = []
    
            validate_performances = []
            validate_performances_MAE = []
    
            test_performances = []
            test_performances_MAE = []
            
            cumulative_test_predictions = []
            cumulative_test_truths = []
    
            models = []
            
            self.fold = count 
            count+=1

            param_list = self.get_params_()
            
            for self.curr_param in tqdm(param_list, "params", postfix = self.source + "  --  " + str(self.num_features)):
                self.features_init()
            
                X_train, X_test = self.data.iloc[train_index], self.data.iloc[test_index]
                y_train, y_test = self.outputs[train_index], self.outputs[test_index]
                
                dataColumns = list(X_train.columns)

                # scaler = StandardScaler()
                # X_train = scaler.fit_transform(X_train)
                # X_test = scaler.transform(X_test)

                X_train = pd.DataFrame(X_train, columns = dataColumns)
                X_test = pd.DataFrame(X_test, columns = dataColumns)

                if self.approach == "EF" and self.level == "level2":
                    X_train = X_train[self.all_features[self.fold -1]]
                    X_test = X_test[self.all_features[self.fold -1]]

                # X_test = scaler.transform(X_test) 


                train_performance, validate_performance, train_performance_MAE, validate_performance_MAE, model, bestFeatures = self.validate(X_train, y_train)
    
                if self.level == "level1":
                    self.feature_close()

                # depths = 0
                # svecs = 0
    
                ####################################################################################################################
                ftest_predictions = []
                for i,valModel in enumerate(model):
                    
                    # if self.m == "RF":
                    #     depths += np.mean([estimator.tree_.max_depth for estimator in valModel.estimators_])
                        
                    # if self.m == "SVR":
                    #     svecs += len(valModel.support_vectors_)
                    
                    if self.level == "level1":                        
                        self.top_columns = bestFeatures[i]
                        
                        if self.feature_base == "train-data":
                            if self.num_features != -1:
                                X_test_ = self.reduce_data(X_test)
                            
                        test_predictions = valModel.predict(X_test_)
                    else:
                        test_predictions = valModel.predict(X_test)
                    
                    if len(ftest_predictions) == 0:
                        ftest_predictions = test_predictions
                    else:
                        ftest_predictions += test_predictions 
    
                # ftest_predictions = ftest_predictions/10
                # test_predictions = ftest_predictions
                ####################################################################################################################
                
                cumulative_test_predictions = test_predictions
                cumulative_test_truths = y_test
    
                test_performance = mean_squared_error(test_predictions, y_test, squared=False)
                test_performance_MAE = mean_absolute_error(test_predictions, y_test)

                test_performances.append(test_performance)
                test_performances_MAE.append(test_performance_MAE)
    
                train_performances.append(train_performance)
                train_performances_MAE.append(train_performance_MAE)
    
                validate_performances.append(validate_performance)
                validate_performances_MAE.append(validate_performance_MAE)
    
                self.save_file(cumulative_test_predictions, cumulative_test_truths)
            
            train_performance_ranking = sp.rankdata(train_performances)
            val_performance_ranking = sp.rankdata(validate_performances)
            test_performance_ranking = sp.rankdata(test_performances)
    
            
    
            self.dataframe = {
    
                "train performance RMSE" : train_performances,
                "test performance RMSE" : test_performances,
                "validate performance RMSE" : validate_performances,
    
                "train performance MAE" : train_performances_MAE,
                "validate performance MAE" : validate_performances_MAE,
                "test performance MAE" : test_performances_MAE,
    
                "train rank" : train_performance_ranking,
                "validate rank" : val_performance_ranking,
                "test rank" : test_performance_ranking,
                
                "avg depth" : '', # if self.m != "RF" else depths/10,
                "support vectors" : '', # if self.m != "SVR" else str(svecs/10)
    
            }
            self.dataframe["'|'".join(list(self.parameters))] = param_list
            self.cv_results_ = pd.DataFrame.from_dict(self.dataframe)
            
            self.save_performance()

    

    def get_params_(self):
        """returns the combination of different model parameters

        Returns:
            list: combinations of different parameters.
        """
        self.parameters = allParams(self.m)
        self.param_keys = list(self.parameters)
        
        param_list = list(itertools.product(*self.parameters.values()))        
        return param_list


    def kTkV(self):
        """initiaties the kTkV training setting. Selects a model parameters, then sends the data to train_kTkV to start the training process.
        """

        # validate_performances = []
        # validate_performances_MAE = []

        # test_performances = []
        # test_performances_MAE = []

        # train_performances = []
        # train_performances_MAE = []

        # models = []


            # self.model = self.get_model(self.m, self.curr_param)

        self.train_kTkV()

            # train_performances.append(train_performance)
            # train_performances_MAE.append(train_performance_MAE)

            # validate_performances.append(validate_performance)
            # validate_performances_MAE.append(validate_performance_MAE)

            # test_performances.append(test_performance)
            # test_performances_MAE.append(test_performance_MAE)
            
            # models.append(model)

        # train_performance_ranking = sp.rankdata(train_performances)
        # val_performance_ranking = sp.rankdata(validate_performances)
        # test_performance_ranking = sp.rankdata(test_performances)


        # self.dataframe = {

        #     "train performance RMSE" : train_performances,
        #     "test performance RMSE" : test_performances,
        #     "validate performance RMSE" : validate_performances,

        #     "train performance MAE" : train_performances_MAE,
        #     "validate performance MAE" : validate_performances_MAE,
        #     "test performance MAE" : test_performances_MAE,

        #     "train rank" : train_performance_ranking,
        #     "validate rank" : val_performance_ranking,
        #     "test rank" : test_performance_ranking,
            
        #     "max depth" : '' if self.m != "RF" else max([estimator.tree_.max_depth for estimator in model.estimators_]),
        #     "support vectors" : '' if self.m != "SVR" else str(len(model.support_vectors_))
            


        # }
        # self.dataframe["'|'".join(list(self.parameters))] = param_list
        # self.cv_results_ = pd.DataFrame.from_dict(self.dataframe)


    def normal_CV(self):
        """Initiates the training setting for normal Cross Validation. Uses validate_kTkV for training.
        """

        train_performances = []
        test_performances = []

        train_performances_MAE = []
        test_performances_MAE = []

        param_list = self.get_params_()

        def train_loop():
            for self.curr_param in tqdm(param_list, desc = "params"):
                train_performance_MSE, test_performance_MSE, train_performance_MAE, test_performance_MAE, model  = self.validate(self.data, self.outputs, kf)
                train_performances.append(train_performance_MSE)
                test_performances.append(test_performance_MSE)

                train_performances_MAE.append(train_performance_MAE)
                test_performances_MAE.append(test_performance_MAE)

        
            train_performance_rankings_MSE = sp.rankdata(train_performances)
            test_performance_rankings_MSE = sp.rankdata(test_performances)

            train_performance_rankings_MAE = sp.rankdata(train_performances_MAE)
            test_performance_rankings_MAE = sp.rankdata(test_performances_MAE)


            self.dataframe = {
                "train RMSE" : train_performances,
                "train RMSE rank" : train_performance_rankings_MSE,

                "test RMSE" : test_performances,
                "test RMSE rank" : test_performance_rankings_MSE,

                "train MAE" : train_performances_MAE,
                "train MAE rank" : train_performance_rankings_MAE,

                "test MAE" : test_performances_MAE,
                "test MAE rank" : test_performance_rankings_MAE,
                
                "max depth" : '' if self.m != "RF" else max([estimator.tree_.max_depth for estimator in model.estimators_]),
                "support vectors" : '' if self.m != "SVR" else str(len(model.support_vectors_))
            }

            self.dataframe["'|'".join(list(self.parameters))] = param_list
            self.cv_results_ = pd.DataFrame.from_dict(self.dataframe)

        if self.same_split:
            if self.stratified != True:
                kf = KFold(n_splits=self.CV_(), shuffle = False)
            else:
                kf = StratifiedKFold(n_splits=self.CV_(), shuffle = False)
                if self.cv == "LOO":
                    kf = KFold(n_splits=self.CV_(), shuffle=False) #change this later

        else:
            kf = None
            
        train_loop()


    def forward(self):
        """Based on training setting, this redirects training to one of the initializers.
        """

        if self.cv != "kTkV":
            if self.metric != "all-metrics":
                self.oneMetric_cv()
            elif self.metric == "all-metrics":
                self.normal_CV()
    
        else:   
            self.kTkV()

