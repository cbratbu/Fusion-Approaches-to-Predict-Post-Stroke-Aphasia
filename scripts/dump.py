from libraries import *
from getData import *
from models import *
from params import *
from utils import * 
class Model:
    def __init__(self, settings):
        self.cv = settings["Cross Validation Type"]
        self.metric = settings["metric"]
        self.repeat_features = settings["repeat features"]
        self.m = settings["model"]
        self.verbose = settings["verbose"]
        if self.cv != "kTkV" and self.metric != "all-metrics":
            self.model = self.get_model(settings["model"])
        self.pca = PCA(n_components=2)
        self.stratified = settings["stratified"]
        # self.order = settings["order"]
        self.same_split = settings["same split"]
        self.num_features = settings["top_k"]
        self.init(settings)

    def reduce(self):
        self.outputs = self.outputs.reshape(self.outputs.shape[0], 1)
        self.data = np.hstack((self.data, self.outputs))
        self.data = pd.DataFrame(self.data)

        corrs = self.data.corr().abs()
        importances = corrs.values[-1][:-1]

        top_columns = np.argpartition(importances, -self.num_features)[-self.num_features:]

        # print("top k columns = ", top_columns)
        self.data = self.data.iloc[:,top_columns]
        self.outputs = self.outputs.ravel()
        self.data = self.data.values
        # print("data shape = ", self.data.shape)


    def init(self, augmentation_settings): # gets the data to train and test
        GET = getData(augmentation_settings)
        self.data, self.outputs = GET.data()
        self.column_names = self.data.columns
        print("data shape = ", self.data.shape)
        print("outputs shape = ", self.outputs.shape)
        # print("features", self.num_features)
        if self.num_features != -1:
            self.reduce()
            
            # print("reduction done")
            # print("data shape now = ", self.data.shape)
        if self.stratified == True:
            self.data = pd.DataFrame(self.data)
            self.data["outputs"] = self.outputs 
            # if self.order =="ascending":
            self.data = self.data.sort_values(by = "outputs", ascending = True)
            # elif self.order == "descending":
                # self.data = self.data.sort_values(by = "outputs", ascending = False)
            self.outputs = self.data["outputs"].values
            self.data = self.data.drop(["outputs"], axis = 1)
            self.data = self.data.values
            
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
        # print("model is ", model)
        # print("params here are ", params)
        params = allParams(model) if params == None else params

        # print("parameters = ", self.parameters)

        if self.cv != "kTkV" and self.metric != "all-metrics":
            self.correct_metric()
            # print("we got here bros")
            return GridSearchCV( m(), params, cv= self.CV_(), scoring = self.metric , return_train_score = True, verbose = self.verbose)
        else:
            params = dict(zip(self.param_keys, params))
            # print("params here = ", params)
            return m(**params)

    def train(self, data, outputs):
        self.model.fit(data, outputs)

    def predict(self, data):
        return self.model.predict(data)

    def get_score(self,data,outputs, return_ = False): #gives out R2 scores
        print("R2 fit score = ", self.model.score(data, outputs), "\n" )

    def CrossValResults(self):
        print(self.model.cv_results_)
        print('\n')

    def modify_data(self, data):
        self.pca.fit(data)
        raise NotImplementedError()

    def get_data(self):
        X_train, X_test, y_train, y_test = train_test_split( self.data, self.outputs, test_size=0.09, random_state=42)

        if self.cv != "kTkV":
            X_train, y_train = self.data, self.outputs

        print("train data shape = ", X_train.shape)
        print("train labels shape = ", y_train.shape, "\n")

        print("test data shape = ", X_test.shape)
        print("test labels shape = ", y_test.shape, "\n")

        return X_train, X_test, y_train, y_test

    def oneMetric_cv(self):
        X_train, X_test, y_train, y_test = self.get_data()
        self.train(X_train, y_train)

        print("training performance")
        self.get_score(X_train, y_train)

        # print("test data performance")
        # self.get_score(X_test, y_test)

        self.train_predictions_ = self.predict(X_train)
        # self.test_predictions_ = self.predict(X_test)
    
    def important_columns(self, data, outputs):
        # outputs = np.array(outputs )
        # print("outputs = ",outputs)
        outputs = outputs.reshape(outputs.shape[0], 1)
        data = np.hstack((data, outputs))
        data = pd.DataFrame(data)

        corrs = data.corr().abs()
        importances = corrs.values[-1][:-1]

        top_columns = np.argpartition(importances, -self.num_features)[-self.num_features:]
        self.save_features(list(self.all_features[top_columns]))
        return top_columns

    def reduce_data(self, data):
        data = pd.DataFrame(data)
        data = data.iloc[:,self.top_columns]
        # outputs = outputs.ravel()
        return data.values
    
    def get_KFfname(self):
        fname = ""
        
        for i,param in enumerate(self.param_keys):
            fname += "[" + param[0] + "-" + str(self.curr_param[i]) + "]_" 
        
        fname = fname[:-1] + ".csv"
        return fname
        
            
    def get_folder_name(self):
        # path =  PATH + "results/outputs"
        path = create_folder(self.source, "outputs")
        stratified = "" if self.stratified!=True else "stratified"
        fname = self.cv + "_" + self.m + "_" + self.metric + "_top" + str(self.num_features) + "frs_" + stratified 
        return path + "/" + fname[:-1]


    def save_features(self, features):
        folder_path = self.get_folder_name("features")
        
        


    def validate(self, data, outputs, kf2 = None):
        
        # print("data shape - ", data.shape)
        # print("outptus shape = ", len(outputs))
        if kf2 == None:
            if self.stratified != True: 
                if self.cv != "LOO":
                    kf2 = KFold(n_splits=self.CV_(), shuffle = True)
                    class_labels = outputs
                
            else:
                # print("this should not at all happen")
                kf2 = StratifiedKFold(n_splits=self.CV_(), shuffle = False)
                class_labels = self.get_class_labels(splits = 5, outputs = outputs)
                # print("class labels = ", class_labels)
                # kf2 = KFold(n_splits=10, shuffle = False)
            if self.cv == "LOO":
                kf2 = KFold(n_splits=self.CV_(), shuffle=True) #change this later
                class_labels = outputs
        else:
            if self.stratified:
                class_labels = self.get_class_labels(splits = 5, outputs = outputs)
            else:
                class_labels = outputs            

        train_performance = []
        train_performance_MAE = []

        validate_performance = []
        validate_performance_MAE = []

        models = []

        mean_train_MSE = []
        mean_validate_MSE = []
        mean_test_MSE = []
        
        

        cumulative_validate_predictions = []
        cumulative_validate_truths = []
        
        for train_index, validate_index in kf2.split(data, class_labels):

            # print("train length = ", len(train_index), " -- test length = ", len(validate_index))
            # print(train_index)
            # print("train_data shape = ", len(train_index))
            # print("validate data shape = ", len(validate_index))
            
            self.model = self.get_model(self.m, self.curr_param)
            X_train, X_validate = data[train_index], data[validate_index]
            y_train, y_validate = outputs[train_index], outputs[validate_index]
            
            # print("train data shape = ", X_train.shape, " -- val data shape = ", X_validate.shape)
            if self.num_features!=-1 and self.cv!="kTkV":
                self.top_columns = self.important_columns(data,outputs)
                X_train = self.reduce_data(X_train)
                X_validate = self.reduce_data(X_validate)
            

            self.model.fit(X_train, y_train)
            train_predictions = self.model.predict(X_train)
            self.train_mean = np.mean(y_train)
            
            validate_predictions = self.model.predict(X_validate)


            if self.cv != "kTkV":
                cumulative_validate_predictions.append(validate_predictions)
                cumulative_validate_truths.append(y_validate)
            
            models.append(self.model)

            # if self.metric == "MSE":
            train_performance.append(mean_squared_error(train_predictions, y_train))
            validate_performance.append(mean_squared_error(validate_predictions,y_validate))
            # elif self.metric == "MAE":
            train_performance_MAE.append(mean_absolute_error(train_predictions, y_train))
            validate_performance_MAE.append(mean_absolute_error(validate_predictions,y_validate))


        if self.cv!="kTkV":
            cumulative_validate_predictions = list(itertools.chain(*cumulative_validate_predictions))
            cumulative_validate_truths = list(itertools.chain(*cumulative_validate_truths))
            predictions = {
                "predictions" : cumulative_validate_predictions,
                "ground truth score": cumulative_validate_truths,
            }
            folder_name = self.get_folder_name("output_files")
            
            if not os.path.exists(folder_name ):
                os.makedirs(folder_name)

            
            predictions = pd.DataFrame(predictions)
            self.kFfname = self.get_KFfname()

            predictions.to_csv(folder_name + "/" + self.kFfname)

        model = models[np.argmin(validate_performance)]
        return np.mean(train_performance), np.mean(validate_performance), np.mean(train_performance_MAE), np.mean(validate_performance_MAE), model


    def get_class_labels(self, splits, outputs):
        x = np.ones(len(outputs))
        
        counter = 0
        counter_update = int(len(outputs)/splits)
        adder = 0
        
        while(counter < len(outputs)):
            x[counter:counter + counter_update] += adder 
            adder += 1
            counter += counter_update 
            
        return x 
            

    def train_kTkV(self):
        if self.stratified!=True:
            kf = KFold(n_splits=11, shuffle = True)
            class_labels = self.outputs
        else:
            # kf = KFold(n_splits=11, shuffle = False)
            # print("stratified kfold happened")
            kf = StratifiedKFold(n_splits=11, shuffle = False)
            class_labels = self.get_class_labels(splits=5, outputs = self.outputs)
            # print("class labels = ", class_labels)
            # print("outputs = ", self.outputs)
            # label_encoder = LabelEncoder()
            
            # temp_outputs = label_encoder.fit_transform(np.array(self.outputs))
            # print("temp outputs shape = ", temp_outputs.shape)
        
        train_performances = []
        train_performances_MAE = []

        validate_performances = []
        validate_performances_MAE = []

        test_performances = []
        test_performances_MAE = []

        models = []
        
        cumulative_test_predictions = []
        cumulative_ground_truths = []

        # if self.stratified==True:
        # print("data shape = ", self.data.shape)
        # outputs = class_labels if self.stratified else self.outputs
        # print("outputs shape = ", self.outputs.shape)
        for train_index, test_index in kf.split(self.data, class_labels):
            # print("train length = ", len(train_index), " -- test length = ", len(test_index))
            X_train, X_test = self.data[train_index], self.data[test_index]
            y_train, y_test = self.outputs[train_index], self.outputs[test_index]

            # print("test split shape = ", len(test_index))
            
            if self.num_features!=-1:
                # print("num features = ", self.num_features)
                # print("this should happen")
                # print("this is not supposed to happen")
                self.top_columns = self.important_columns(X_train,y_train)
                X_train = self.reduce_data(X_train)
                X_test = self.reduce_data(X_test)


            self.train_mean = np.median(y_train)

            # ones_train = np.ones(len(y_train))*self.train_mean
            # ones_test = np.ones(len(y_test))*self.train_mean


            train_performance, validate_performance, train_performance_MAE, validate_performance_MAE, model = self.validate(X_train, y_train)

            models.append(model)

            # test_ones = np.ones(len(y_test))*self.train_mean
            # X_test = self.reduce_data(X_test)
            test_predictions = model.predict(X_test)
            cumulative_test_predictions.append(test_predictions)
            cumulative_ground_truths.append(y_test)
            # test_performance = mean_squared_error(test_ones, y_test)
            # if self.metric == "MSE":
            test_performance = mean_squared_error(test_predictions, y_test)
            # elif self.metric == "MAE":
            test_performance_MAE = mean_absolute_error(test_predictions, y_test)


            # train_performance = mean_absolute_error(ones_train, y_train)
            # test_performance = mean_absolute_error(ones_test, y_test)

            train_performances.append(train_performance)
            train_performances_MAE.append(train_performance_MAE)

            validate_performances.append(validate_performance)
            validate_performances_MAE.append(validate_performance_MAE)

            test_performances.append(test_performance)
            test_performances_MAE.append(test_performance_MAE)

        folder_name = self.get_folder_name("output_files")
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        cumulative_test_predictions = list(itertools.chain(*cumulative_test_predictions))
        cumulative_ground_truths = list(itertools.chain(*cumulative_ground_truths))
        
        predictions = {
            "predictions" : cumulative_test_predictions,
            "ground truth score": cumulative_ground_truths,
        }

        self.kFfname = self.get_KFfname()
        
        predictions = pd.DataFrame(predictions)
        predictions.to_csv(folder_name + "/" + self.kFfname)
        
        
        model = models[np.argmin(test_performances)]
        return np.mean(train_performances), np.mean(validate_performances), np.mean(test_performances), np.mean(train_performances_MAE), np.mean(validate_performances_MAE), np.mean(test_performances_MAE), model

    def get_params_(self):
        self.parameters = allParams(self.m)
        self.param_keys = list(self.parameters)
        
        param_list = list(itertools.product(*self.parameters.values()))        
        return param_list


    def kTkV(self):

        validate_performances = []
        validate_performances_MAE = []

        test_performances = []
        test_performances_MAE = []

        train_performances = []
        train_performances_MAE = []

        models = []

        param_list = self.get_params_()


        for self.curr_param in tqdm(param_list, "params"):
            # self.model = self.get_model(self.m, param)
            
            train_performance, validate_performance, test_performance, train_performance_MAE, validate_performance_MAE, test_performance_MAE, model = self.train_kTkV()

            train_performances.append(train_performance)
            train_performances_MAE.append(train_performance_MAE)

            validate_performances.append(validate_performance)
            validate_performances_MAE.append(validate_performance_MAE)

            test_performances.append(test_performance)
            test_performances_MAE.append(test_performance_MAE)

            models.append(model)

        train_performance_ranking = sp.rankdata(train_performances)
        val_performance_ranking = sp.rankdata(validate_performances)
        test_performance_ranking = sp.rankdata(test_performances)


        self.dataframe = {

            "train performance MSE" : train_performances,
            "test performance MSE" : test_performances,
            "validate performance MSE" : validate_performances,

            "train performance MAE" : train_performances_MAE,
            "validate performance MAE" : validate_performances_MAE,
            "test performance MAE" : test_performances_MAE,

            "train rank" : train_performance_ranking,
            "validate rank" : val_performance_ranking,
            "test rank" : test_performance_ranking,

            # "params" : param_list
        }
        self.dataframe["'|'".join(list(self.parameters))] = param_list

        self.cv_results_ = pd.DataFrame.from_dict(self.dataframe)

    def normal_CV(self):

        train_performances = []
        test_performances = []

        train_performances_MAE = []
        test_performances_MAE = []
        
        param_list = self.get_params_()

        # Creating a folder to save KFold CV outputs at different times. 
        
        # print("fname = ", folder_name)

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
                "train MSE" : train_performances,
                "train MSE rank" : train_performance_rankings_MSE,

                "test MSE" : test_performances,
                "test MSE rank" : test_performance_rankings_MSE,

                "train MAE" : train_performances_MAE,
                "train MAE rank" : train_performance_rankings_MAE,

                "test MAE" : test_performances_MAE,
                "test MAE rank" : test_performance_rankings_MAE,
            }

            self.dataframe["'|'".join(list(self.parameters))] = param_list
            self.cv_results_ = pd.DataFrame.from_dict(self.dataframe)

        if self.same_split:
            # print("CV type = ", self.CV_)
            if self.stratified != True:
                kf = KFold(n_splits=self.CV_(), shuffle = False)
            else:
                                # print("this should not at all happen")
                kf = StratifiedKFold(n_splits=self.CV_(), shuffle = False)
                # print("class labels = ", class_labels)
                # kf2 = KFold(n_splits=10, shuffle = False)
                if self.cv == "LOO":
                    kf = KFold(n_splits=self.CV_(), shuffle=True) #change this later
                    class_labels = self.outputs

                
        else:
            kf = None
                 
        train_loop()


    def forward(self):

        if self.cv != "kTkV":
            if self.metric != "all-metrics":
                self.oneMetric_cv()
            elif self.metric == "all-metrics":
                self.normal_CV()
    
        else:   
            self.kTkV()

