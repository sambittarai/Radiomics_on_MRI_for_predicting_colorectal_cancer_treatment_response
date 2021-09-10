import feature_selection as fesel
import ml_prediction as mlpred
from config import parse_args





# Feature Selection
args = parse_args()

# Feature selection
# FSmethod = 'MRMR'
# FSparams = {'nFeatures': 15, 
#             'internalFEMethod': 'MID', 
#             'nBins': 4, 
#             'discStrategy': 'kmeans'}

# FSmethod = 'LASSO'
# FSparams = {'nFeatures': 15}

FSmethod = 'LogReg'
FSparams = {'nFeatures': 15}

selectedFeatures = fesel.select_features(FSmethod, FSparams, args.selectionFeaturesPath, args.manualFeaturesPath, args)
print(f'Features selected by {FSmethod}:')
print(selectedFeatures)

# Prediction models

# Prediction model 1
MLmethod = 'RFreg'
rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
            'max_depth': [None, 1, 3, 5, 10, 15],
            'max_features': [0.33, 0.67, 1.0, 'sqrt']}  
scoring = 'r2'

# # Prediction model 2
# MLmethod = 'RFclass'
# rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
#             'max_depth': [None, 1, 3, 5, 10, 15],
#             'max_features': [0.33, 0.67, 1.0, 'sqrt']}  
# scoring = 'r2'

# yTrueTest, yPredRegTest, yTrueVal, yPredRegVal, MLparams = mlpred.create_evaluate_model(args, MLmethod, rfParams, selectedFeatures, args.selectionFeaturesPath, args.manualFeaturesPath, args.paramSearchResultsPath, optimizeParams=True, scoringOptiMetric=scoring)

# # Prediction model 3
# MLmethod = 'LogReg'
# rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
#             'max_depth': [None, 1, 3, 5, 10, 15],
#             'max_features': [0.33, 0.67, 1.0, 'sqrt']}  
# scoring = 'r2'

yTrueTest, yPredRegTest, yTrueVal, yPredRegVal, MLparams = mlpred.create_evaluate_model(args, MLmethod, rfParams, selectedFeatures, args.selectionFeaturesPath, args.manualFeaturesPath, args.paramSearchResultsPath, optimizeParams=True, scoringOptiMetric=scoring)

# Write validation- and test- results to csv-file
mlpred.write_results_to_csv(args.predResultsPath, args.selectionFeaturesPath, FSmethod, FSparams, selectedFeatures, MLmethod, MLparams, yTrueTest, yPredRegTest, yTrueVal, yPredRegVal)

print("Done!")




