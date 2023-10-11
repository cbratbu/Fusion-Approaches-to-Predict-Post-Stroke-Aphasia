from libraries import *
from params import * 
from utils import *
from make import *
import re

class getData:
    def __init__(self, settings):
        self.path = PATH_DATA
        self.augment = settings["Augment"]
        self.model = settings["model"]
        self.repeat_features = settings["repeat features"]
        self.approach = settings["approach"]
        self.level = settings["level"]
        self.all_features = []
        self.experiment = settings["experiment"]
        self.feature_base = settings["feature base"]
        
        dta = settings["data"]
        
        
        if dta == "RS": # Done
            print("loading resting state data")
            self.init()

        # elif dta == "stan_optimal": 
        #     print("loading stan's data")
        #     self.stan_optimal()
            
        # elif dta == "combined_features":
        #     self.combined_data()
            
        else:
            self.dta = dta
            self.init3()
        

    def readRSData(self):
        self.init()
        self.correlation_data = pd.DataFrame(self.correlation_data, columns = list(self.all_features))
        return self.correlation_data
        
    
    def read_data(self):
        
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")].values
        outputs = outputs.reshape(len(outputs),1)
        self.participants_ = list(df[("participant", "participant")].values)


        data = {}

        # AQ - Aphasia Quotient
        data["AQ"] = pd.DataFrame(df[('behavioral', "wab_aq_bd")].values, columns = ["wab_aq_bd"]) 
        # data["AQ"].index = participants

        # DM - Demographics
        data["DM"] = df["demographic_info"]
        # data["DM"].index = participants
        # data["DM"] = data["DM"].drop(["level_0"], axis = 1)
        
        # print("demographic data shape = ", data["DM"].shape)

        # FA - Fractional Anisotropy
        featuresFAL = ["fa_avg_ccmaj", "fa_avg_ccmin", "fa_avg_lifof", "fa_avg_lilf", "fa_avg_lslf", "fa_avg_lunc", "fa_avg_larc"]
        featuresFAR = ["fa_avg_rifof", "fa_avg_rilf", "fa_avg_rslf", "fa_avg_runc", "fa_avg_rarc"]
        FA_L = df["average_FA_values"][featuresFAL].fillna(0).values
        FA_R = df["average_FA_values"][featuresFAR].fillna(df["average_FA_values"][featuresFAR].mean()).values
        data["FA"] = pd.DataFrame(np.hstack((FA_L, FA_R)), columns = featuresFAL+featuresFAR)
        # data["FA"].index = participants
        # data["FA"] = data["FA"].drop(["level_0"], axis = 1)

        # PS_G - percent grey matter per region  
        data["PSG"] = df["percent_spared_in_gray_matter"]
        # data["PSG"].index = participants
        # data["PSG"] = data["PSG"].drop(["level_0"], axis = 1)

        # PS_W - percent white matter per region  
        data["PSW"] = df["percent_spared_in_white_matter"]
        # data["PSW"].index = participants
        # data["PSW"] = data["PSW"].drop(["level_0"], axis = 1)

        # LS - Lesion size as a single metric 
        data["LS"] = pd.DataFrame(df[("lesion_size", "lesion_size_ls")].values, columns = ["lesion_size_ls"])
        # data["LS"].index = participants
        # data["LS"] = data["LS"].drop(["level_0"], axis = 1)

        # RS - Resting state data
        data["RS"] = self.readRSData()
        # data["RS"].index = participants
        # data["RS"] = data["RS"].drop(["level_0"], axis = 1)

        RS_between = pd.read_csv("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "betweenness.csv")
        # RS_between.index = participants#RS_between.iloc[:,0]
        RS_between = RS_between.iloc[:,1:]
        data["RS-bet"] = RS_between
        # data["RS-bet"] = data["RS-bet"].drop(["level_0"], axis = 1)

        RS_degree = pd.read_csv("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "degree.csv")
        # RS_degree.index = participants#RS_degree.iloc[:,0]
        RS_degree = RS_degree.iloc[:,1:]
        data["RS-deg"] = RS_degree
        # data["RS-deg"] = data["RS-deg"].drop(["level_0"], axis = 1)

        RS_eff = pd.read_csv("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "local_efficiency.csv")
        # RS_eff.index = participants#RS_eff.iloc[:,0]
        RS_eff = RS_eff.iloc[:,1:]
        data["RS-eff"] = RS_eff
        # data["RS-eff"] = data["RS-eff"].drop(["level_0"], axis = 1)

        RS_trans = pd.read_csv("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "local_transitivity.csv")
        # RS_trans.index = participants#RS_trans.iloc[:,0]
        RS_trans = RS_trans.iloc[:,1:]
        data["RS-trans"] = RS_trans
        # data["RS-trans"] = data["RS-trans"].drop(["level_0"], axis = 1)

        self.datadict = data 
        self.outputs = outputs

    
    
    # def combined_data(self):
    #     self.read_data()
    #     corr_data = []
    #     self.all_features = []
    #     for i,dataSource in enumerate(list(self.datadict)):
    #         # print("dataSource now = ", dataSource)
    #         # print("data shape = ", self.datadict[dataSource].shape)
    #         if dataSource in datasets:
    #             # print("dataSource added = ", dataSource)
    #             if len(corr_data) == 0:
    #                 corr_data = self.datadict[dataSource].values
    #                 self.all_features += list(self.datadict[dataSource].columns)
    #             else:
    #                 corr_data = np.hstack((corr_data, self.datadict[dataSource].values))
    #                 self.all_features += list(self.datadict[dataSource].columns)
        
    #     # print("----")
    #     self.correlation_data = corr_data
        
    
    
    def LF_level1(self):
        self.read_data()
        features = self.dta.split("+")
        correlations = []
        for i,dataset in enumerate(features):
            if i==0:
                correlations = self.datadict[dataset]
                # featureList = list(self.datadict[dataset].columns)
            else:
                correlations = pd.concat([correlations, self.datadict[dataset]], axis = 1)
                # correlations = np.hstack((correlations, self.datadict[dataset].values))
                # featureList += list(self.datadict[dataset].columns)
        self.correlation_data = correlations
        self.all_features = list(self.correlation_data.columns)
        # self.all_features = featureList
        
    
    def LF_level2(self):
        print("data = ", str(self.dta))
        data_combination = self.dta.split("+")
        data_combination = sorted(data_combination)
        # data_combination = data_combination.split("-")
        dataPath = "/projectnb/skiran/saurav/Fall-2022/src2/data/" + self.experiment + "/" + "lateFusionData/"
        fname = None
        
        # if self.experiment == "EXP-without-stans-features":
        #     temp = datasets
        #     datasets = temp.remove("stan_optimal")

        if "noStan" in self.experiment or "without-stans-features" in self.experiment:
            datasets_copy = datasets
            datasets_copy.remove("stan_optimal")

        
        if len(data_combination) == len(datasets):
            data_combination = self.model
            fname = data_combination + "_allModalityOutputs.xlsx"

        # if self.experiment == "EXP-without-stans-features" and len(data_combination) == len(datasets)-1:
            
        #     data_combination = self.model
        #     fname = data_combination + "_allModalityOutputs.xlsx"
        else:
            
            # print("dc = ",data_combination)

            data_combination = "_".join(data_combination)
            fname =  self.model + "_" + data_combination + "_ModalityOutputs.xlsx"
        
        
        print("fileName = ", fname)
        
        dataPath += self.model + "/"  + fname
        
        self.correlation_data = pd.read_excel(dataPath)
        self.outputs = self.correlation_data["ground truth score"].values
        self.all_features = list(self.correlation_data.columns) 
        self.correlation_data = self.correlation_data.drop(["ground truth score", "Unnamed: 0"], axis = 1)
        # self.correlation_data = self.correlation_data.values
        

    def getReshapedData(self, dataSources, dataSizes=None):
        self.read_data()
        
        if self.feature_base == "entire-data":        
            for dataSource in dataSources:
                self.all_features = []
                ds = dataSource.split("_")[0]
                self.datadict[ds] = self.reduce_features( self.datadict[ds], self.outputs, dataSizes[ds], self.datadict[ds].columns )
                self.datadict[ds] = pd.DataFrame(self.datadict[ds], columns = self.all_features)

        elif self.feature_base == "train-data":
            for dataSource in dataSources:
                self.all_features = []
                ds = dataSource.split("_")[0]
                # print("dataSource = ", ds)
                self.datadict[ds] = self.datadict[ds][self.dataFeatures[ds]]
                # print("shape = ", self.datadict[ds].shape, "  --- len = ", len(self.dataFeatures[ds]))
            
        self.all_features = []
        
    
    def EF_level2_entire_data(self):
        files = datasets
        if self.experiment == "EXP-without-stans-features":
            if "stan_optimal" in datasets:
                files.remove("stan_optimal")
        final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
        dataSources = [f.split("_")[0] + "_results" for f in files if not os.path.isfile(final_path + f)] 
        dataSizes = dict()
        for dataSource in dataSources:
            path = PATH + "results/" + self.experiment + "/" + self.approach + "/" + self.model + "_predictions" + "/" + "level1" + "/" + dataSource + "/" + dataSource + "_aggregate.csv"
            data = pd.read_csv(path)
            data = data.sort_values(by=["validate RMSE"])
            bestFeatures = data.iloc[0]["num features"]
            match_number = re.compile('-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
            bestFeatures = int(re.findall(match_number, bestFeatures)[0])
            dataSizes[dataSource.split("_")[0]] = bestFeatures
        
        self.getReshapedData(dataSources,dataSizes)
        # print("dataSizes = ", dataSizes, dataSources)

        data_combination = self.dta.split("_")[0]
        data_combination = data_combination.split("-")
        
        # print("data combination = ", data_combination)
        final_data = None
        for i,dataSource in enumerate(data_combination):
            if i==0:
                final_data = self.datadict[dataSource]
                # print("dataSource = ", dataSource)
                # print("data shape here = ", final_data.shape)
                self.all_features += list(self.datadict[dataSource].columns)
            else:
                final_data = np.hstack((final_data, self.datadict[dataSource]))
                # print("dataSoure = ", dataSource)
                self.all_features += list(self.datadict[dataSource].columns)
        
        self.correlation_data = final_data




    # def EF_level2_train_data(self):
    #     files = datasets

    #     if "without-stans-features" in self.experiment or "noStan" in self.experiment:
    #         if "stan_optimal" in datasets:
    #             files.remove("stan_optimal")
    #     final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/"
    #     dataSources = [f.split("_")[0] + "_results" for f in files if not os.path.isfile(final_path + f)] 
    #     self.dataFeatures = dict()
        
        
    #     for dataSource in dataSources:
    #         path = PATH + "results/" + self.experiment + "/" + self.approach + "/" + self.model + "_predictions" + "/" + "level1" + "/" + dataSource + "/" + "bestFeatureSet.csv"
    #         data = pd.read_csv(path)
    #         self.dataFeatures[dataSource.split("_")[0]] = list(data["features"])
        
        
    #     self.getReshapedData(dataSources)
    #     # print("dataSizes = ", dataSizes, dataSources)

    #     data_combination = self.dta.split("_")[0]
    #     data_combination = data_combination.split("-")
        
    #     # print("data combination = ", data_combination)
    #     final_data = None
    #     for i,dataSource in enumerate(data_combination):
    #         if i==0:
    #             final_data = self.datadict[dataSource]
    #             # print("dataSource = ", dataSource)
    #             # print("data shape here = ", final_data.shape)
    #             self.all_features += list(self.datadict[dataSource].columns)
    #         else:
    #             final_data = np.hstack((final_data, self.datadict[dataSource]))
    #             # print("dataSoure = ", dataSource)
    #             self.all_features += list(self.datadict[dataSource].columns)
        
    #     self.correlation_data = final_data


    def EF_level2_train_data(self):
        
        data_combination = self.dta.split("+")
        data_combination = sorted(data_combination)
        
        final_path = "/projectnb/skiran/saurav/Fall-2022/src2/results/" + self.experiment + "/EF/" + self.model + "_predictions" + "/" + "level1/"
        
        nfolds = 12 if "normal" in self.experiment else 56
        
        
        
        self.read_data()

        self.all_features = []        
        for fold in range(1,nfolds,1):
            foldFeatures = []    
            for dataset in data_combination:
                fpath = final_path + dataset + "_results" + "/fold-" + str(fold) + "/" + "bestFeatureSet.csv"
                
                featureDf = pd.read_csv(fpath)
                flist = list(featureDf["features"].values)
                foldFeatures += flist 
            self.all_features.append(foldFeatures)
            
        
        
        # df2 = [self.datadict[key] for key in data_combination]
        # result = pd.concat(df2, axis=1)

        
        # result = pd.concat(selected_dataframes, axis=1)
        df2 = []
        for dataset in data_combination:
            
            if len(df2) == 0:
                df2 = self.datadict[dataset]
                df2 = df2.reset_index()
                # print("datadict shape before = ", df2.shape)
            else:
                # df2 = pd.hstack((df2, self.datadict[dataset]))
                A = self.datadict[dataset].reset_index()
                df2 = pd.concat([df2, A], axis=1)
                # df2 = df2.reset_index()
                # df2 = df2.join(self.datadict[dataset])
        print("datasets = ", data_combination)
        print("data shape = ", df2.shape)
        df2 = df2.fillna(df2.median())

        print("total dfolds = ", len(self.all_features))
        nanvalues = df2.isna().sum().sum()
        print("nan value count = ", nanvalues)

        for i, features in enumerate(self.all_features):
            print("shape_" + str(i) + " = ", df2[features].shape)

        # "+".join(datasets).to(csv(""))
            

        if "level_0" in list(df2.columns):
            df2 = df2.drop(["level_0"], axis = 1)

        df2.to_csv("/projectnb/skiran/saurav/Fall-2022/src2/experiment_jobs/EXP-final-SVR/combined_jobs/" + "_".join(data_combination)+".csv")
        print("\n\n")
        # print("all features")
        # print(self.all_features)
                
        self.correlation_data= df2
            
                
        

            
    
    def EF_level2(self):
        if self.feature_base == "entire-data":
            self.EF_level2_entire_data()
            
        elif self.feature_base == "train-data":
            self.EF_level2_train_data()
            
        
    
    def init3(self):
        if self.approach == "LF":
            if self.level == "level1":
                self.LF_level1()
            elif self.level == "level2":
                self.LF_level2()
                
        if self.approach == "EF":
            if self.level == "level1":
                self.LF_level1()
            elif self.level == "level2":
                self.EF_level2()
        
        
    
    def multi_modal(self):
        data = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/src2/data/" + "allModalityOutputs.xlsx" )
        self.outputs = data["ground truth score"].values
        self.all_features = data.columns
        self.correlation_data = data.drop(["ground truth score", "Unnamed: 0"], axis = 1)


    def reduce_features(self, data,outputs, num_features, columns=None):
        

        data = np.hstack((data, outputs))
        data = pd.DataFrame(data)
    
        corrs = data.corr().abs()
        importances = corrs.values[-1][:-1]
        
        top_columns = np.argpartition(importances, -num_features)[-num_features:]
    
        data = data.iloc[:,top_columns]
        self.all_features += list(columns[top_columns])
        
        outputs = outputs.ravel()
        data = data.values
        return data


    def stan_optimal(self):
        print("using stan's data")
        self.all_features = []
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")].values
        outputs = outputs.reshape(len(outputs),1)
        
        outputs_temp = df[("behavioral", "wab_aq_bd")].values  # based on this variable, you filter out the features in stan's feature way.
        outputs_temp = outputs_temp.reshape(len(outputs_temp),1)
    
        data = {}
        data["AQ"] = df[('behavioral', "wab_aq_bd")].values[:, np.newaxis]
        data["DM"] = df["demographic_info"].values
        
        
        featuresFAL = ["fa_avg_ccmaj", "fa_avg_ccmin", "fa_avg_lifof", "fa_avg_lilf", "fa_avg_lslf", "fa_avg_lunc", "fa_avg_larc"]
        featuresFAR = ["fa_avg_rifof", "fa_avg_rilf", "fa_avg_rslf", "fa_avg_runc", "fa_avg_rarc"]

        FA_L = df["average_FA_values"][featuresFAL].fillna(0).values
        FA_R = df["average_FA_values"][featuresFAR].fillna(df["average_FA_values"][featuresFAR].mean()).values
        data["FA"] = np.hstack((FA_L, FA_R))
        data["FA"] = self.reduce_features(data["FA"], outputs_temp, 2, pd.Index(featuresFAL + featuresFAR))
        # self.all_features+=featuresFAL
        # self.all_features += featuresFAR

        data["PS_G"] = df["percent_spared_in_gray_matter"].values
        data["PS_G"] = self.reduce_features(data["PS_G"], outputs_temp, 4, df["percent_spared_in_gray_matter"].columns)
        # self.all_features += list(df["percent_spared_in_gray_matter"].columns)

        data["RS"] = df["restingstate_bivariate_correlations"].values
        data["RS"] = self.reduce_features(data["RS"], outputs_temp, 11, df["restingstate_bivariate_correlations"].columns)
        
        self.all_features += list(df["demographic_info"].columns)
        total_data = np.hstack((data["FA"], data["PS_G"]))
        total_data = np.hstack((total_data, data["RS"]))
        # total_data = np.hstack((total_data, data["AQ"]))
        total_data = np.hstack((total_data, data["DM"]))
        
        total_data = pd.DataFrame(total_data)
        
        self.correlation_data = total_data.values 
        self.outputs = outputs

            
    def init2(self): # this needs to be removed later in early fusion.
        data = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        self.outputs = data[("behavioral", "wab_aq_bd")].values

        d1 = data["percent_spared_in_white_matter"]
        d2 = data["percent_spared_in_gray_matter"]
        d3 = data["lesion_size"]
        
        df = pd.concat([d1,d2], axis = 1)
        df = pd.concat([df,d3], axis = 1)
        self.all_features = df.columns
        self.correlation_data = df.values
            

    # def sortFiles(self) -> None:
    #     # READING THE DATA,
    #     self.column_names = pd.read_csv(self.path + "/" + "ROIs.csv", header = None)
    #     # self.all_features = self.column_names
    #     self.files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
    #     self.files.remove("ROIs.csv")
    #     self.files = np.sort(self.files) # file names for the data"

    #     # READING THE FILE TO GET PATIENT SCORES",
    #     real_df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/RS_bivariate_AQ_continuous.xlsx")
    #     rdf = real_df[["participant", "AQ"]]

    #     # EXTRACTING THE WAB SCORES OF THE PATIENTS
    #     parts = list(rdf["participant"])
    #     self.participants= parts[:30] + parts[31:32] + parts[35:51] + parts[53:60] + parts[61:63] + parts[30:31] # participant IDs"
    #     self.wabaq = list(rdf["AQ"])  # Participant scores"
    
    
    def sortFiles(self) -> None:
        mypath = "/projectnb/skiran/Isaac/data_for_saurav/"
        self.path =  mypath
        subjectIDs = pd.read_csv(mypath+"Subject_IDs.csv", header = None)
        
        filenames = listdir(mypath)
        csvfiles = [ filename for filename in filenames if filename.endswith( ".csv" ) ]
        csvfiles.remove('Subject_IDs.csv')
        csvfiles = sorted(csvfiles)
        
        pdf = {"patientIDs" : list(subjectIDs.values.flatten().astype(str)),
               "alias" : list(csvfiles)
              }
        pdf_alias = pd.DataFrame(pdf)
        
        
        df = pd.read_excel("/projectnb/skiran/saurav/Fall-2022/RS" + "/compiled_dataset_RSbivariate_without_controls_v7.xlsx", header = [0,1])
        outputs = df[("behavioral", "wab_aq_bd")]
        
        pdf = { "patientIDs": list(df[("participant", "participant")]),
                "scores" : list(outputs) 
              }
        pdf_scores = pd.DataFrame(pdf)
        
        corr_data = []
        scores = []
        
        for patient, score in pdf_scores.values:
            if patient != "BU29c07":
                fname = mypath  + list(pdf_alias[pdf_alias["patientIDs"] == patient]["alias"])[0]
                scores.append(score)
                df = pd.read_csv(fname)
                columns = df.columns
                df.index = columns
                corr_data.append(df)
            else:
                fname = mypath  + list(pdf_alias[pdf_alias["patientIDs"] == patient+"NU"]["alias"])[0]
                df = pd.read_csv(fname)
                columns = df.columns
                df.index = columns
                scores.append(score)
                corr_data.append(df)

        self.correlation_data = corr_data
        self.outputs = scores
        
        print("correlation data shape first new data = ", np.array(self.correlation_data).shape)
        print("output shape first new datz = ", np.array(self.outputs).shape)
        
        


    def noAugment(self) -> None:

        # self.correlation_data = []
        # self.outputs = []

        def modify_data():
            for index,data in enumerate(self.correlation_data):
                df = data
                df = df.where(np.triu(np.ones(df.shape),k=1).astype(np.bool))
                df = df.stack().reset_index()
                df.columns = ['Row','Column','Value']
                df["index"] = df["Row"] + "-vs-" + df["Column"]
                self.correlation_data[index] = df["Value"].values #data.values[np.triu_indices(48, k = 1)]
                self.all_features = df["index"]

            self.correlation_data = np.array(self.correlation_data)
            self.correlation_data = pd.DataFrame(self.correlation_data, columns = list(self.all_features))
            self.outputs =  np.array(self.outputs)

        # for patient_index, patient_file in enumerate(self.files):

            # READING THE PATIENT TIME SERIES FMRI DATA
            # file = pd.read_csv(self.path + "/" + self.files[patient_index], header = None)
            # file.columns = list(self.column_names[0])
            # file = file.reindex(sorted(file.columns), axis = 1)

            
            # CALCULATE THE CORRELATION MATRIX\n",
            # self.correlation_data.append(file.corr())
            # self.outputs.append(self.wabaq[patient_index])

        modify_data()

    # def reduce(self):


    def data(self, reduce = False):
        if reduce == True:
            self.reduce()
        return self.all_features, self.correlation_data, self.outputs

    def params(self, model):
        if model == "SVR":
            return


    def init(self):
        # GETTING THINGS READY TO GET THE DATA
        self.sortFiles()

        # GETTING THE DATA
        if self.augment:
            raise NotImplementedError
            self.augment() 
        else:
            self.noAugment()

    def describe(self):
        print('data shape = ', self.correlation_data.shape)
        print("output shape = ", self.outputs.shape)