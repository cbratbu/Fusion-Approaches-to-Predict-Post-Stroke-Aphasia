import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import argparse
from scripts.make import *
import math
from scipy.stats import norm
from scipy.stats import wilcoxon
from sklearn.metrics import mean_squared_error
# Vector of r-values for each feature set



def getPval(r_A, r_B):
    # Convert r-values to Fisher's Z-scores
    z_A = 0.5 * math.log((1 + r_A) / (1 - r_A))
    z_B = 0.5 * math.log((1 + r_B) / (1 - r_B))

    # Calculate standard error of the difference
    n = 55
    se = math.sqrt((1 / (n - 3)) + (1 / (n - 3)))

    # Calculate test statistic (Z)
    z_diff = (z_A - z_B) / se

    # Calculate p-value
    p_value = 2 * (1 - norm.cdf(abs(z_diff)))
    return p_value




def geterrors(feature_set_A, gt):


    gt, feature_set_A = zip(*sorted(zip(gt, feature_set_A)))

    lst = feature_set_A

    corr_values = []
    rmse_values = []
    for i in range(0, 55, 5):
        # pred_chunk = lst[:i] + lst[i+5:]
        # gt_chunk = gt[:i] + gt[i+5:]

        pred_chunk = lst[i:i+5] # + lst[i+5:]
        gt_chunk = gt[i:i+5] # + gt[i+5:]

        correlation_matrix = np.corrcoef(pred_chunk, gt_chunk)
        correlation_coefficient = correlation_matrix[0, 1]    
        corr_values.append(correlation_coefficient)

        mse = mean_squared_error(pred_chunk, gt_chunk)
        rmse_values.append(mse)
        
    return rmse_values
        
        
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="enter network arguments")
    parser.add_argument("-experiment", nargs = "?", type = str, help = "what experiment to run: [with_stans_features, without_stans_features]", default = "EXP-with-stans-features")   
    args = parser.parse_args()

    experiment = args.experiment
    approach = parameters["-approach"][0]

    model = "SVR" if "SVR" in experiment else "RF"
    modalityPath = "results/" + experiment + "/" + approach + "/" + model + "_predictions/" + "modalityResults.csv"

    correlation_data = pd.read_csv(modalityPath) 
    correlation_data = correlation_data.sort_values(by="r Corr Coef", ascending=False)
    # correlation_data = correlation_data.replace("RS-", "")
    datacombinations = list(correlation_data["Data Combination"])[:20]

    level1_data = ["DM", "PSG", "PSW", "RS", "RS-bet", "RS-deg", "RS-eff", "RS-trans"]
    datacombinations += ["DM", "PSG", "PSW", "RS", "RS-bet", "RS-deg", "RS-eff", "RS-trans", "DM+PSG+PSW+RS+RS-bet+RS-deg+RS-eff+RS-trans"]


    datapath = "results/" + experiment + "/" + approach + "/" + model + "_predictions/"  

    num_feature_sets = len(datacombinations)
    pairwise_p_values = np.zeros((num_feature_sets, num_feature_sets))

    for i, FS1 in enumerate(datacombinations):
        for j, FS2 in enumerate(datacombinations):
            
            FS1 = FS1.split() 
            FS1 = "+".join(FS1)

            FS2 = FS2.split() 
            FS2 = "+".join(FS2)

            
            if FS1 == FS2:
                pairwise_p_values[i,j] = -1
                continue
            
            if FS1 in level1_data:
                o1 = pd.read_csv(datapath + "level1/" + FS1 + "_results/" + "best_outputs.csv")
                gt1 = list(o1["ground truth score"])
                o1 = list(o1["predictions"])
                
            else:
                o1 = pd.read_csv(datapath + "level2/" + FS1 + "_results/" + "best_outputs.csv")
                gt1 = list(o1["ground truth score"])
                o1 = list(o1["predictions"])
                
            if FS2 in level1_data:
                o2 = pd.read_csv(datapath + "level1/" + FS2 + "_results/" + "best_outputs.csv")
                gt2 = list(o2["ground truth score"])
                o2 = list(o2["predictions"])
            else:
                o2 = pd.read_csv(datapath + "level2/" + FS2 + "_results/" + "best_outputs.csv")
                gt2 = list(o2["ground truth score"])
                o2 = list(o2["predictions"])

            e1 = geterrors(o1, gt1)
            e2 = geterrors(o2, gt2)
            
            print("e1 = ", e1)
            print("e2 = ", e2)
            print("\n")
            
            _, p_value = wilcoxon(e1, e2)            
            pairwise_p_values[i, j] = p_value

    # Adjust p-values for multiple comparisons
    # adjusted_p_values = multipletests(pairwise_p_values[np.triu_indices(num_feature_sets, 1)], method='holm')[1]
    # pairwise_p_values[np.triu_indices(num_feature_sets, 1)] = adjusted_p_values

    # Print the pairwise comparison results
    # print("Pairwise comparison results (adjusted p-values):")
    # for i in range(num_feature_sets):
    #     for j in range(i + 1, num_feature_sets):
    #         print(f"Feature set {i + 1} vs Feature set {j + 1}: adjusted p-value = {pairwise_p_values[i, j]}")

            
    pairwise_p_values = pd.DataFrame(pairwise_p_values, columns = datacombinations)
    pairwise_p_values.index = datacombinations 
    pairwise_p_values.to_csv(experiment + "_pvals.csv")
    

    # In this modified code, the r_values variable is a vector containing the r-values for each feature set. The pairwise t-tests are performed accordingly using [r_values[i]] and [r_values[j]] as the input for ttest_ind. The rest of the code remains the same.

    # I apologize for the oversight in the previous response. Thank you for bringing it to my attention, and I appreciate your understanding.
