


result_save_path = "results/"

As = Augmentation_settings

if As["Cross Validation Type"] == "kTkV":
    cvr = model.cv_results_
else:
    m = model.model
    cvr = pd.DataFrame(m.cv_results_)

fname = As["Cross Validation Type"] + "_" + As["model"] + "_" + As["metric"] + "_" + "reduced" + ".csv"
cvr.to_csv(result_save_path + fname)

