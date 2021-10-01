import feature_selection as fesel
import ml_prediction as mlpred
from config import parse_args



args = parse_args()

# # Feature selection
# FSmethod = 'MRMR'
# FSparams = {'nFeatures': 15, 
#             'internalFEMethod': 'MID', 
#             'nBins': 4, 
#             'discStrategy': 'kmeans'}

# FSmethod = 'LASSO'
# FSparams = {'nFeatures': 20}

FSmethod = 'LogReg'
FSparams = {'nFeatures': 20}

selectedFeatures = fesel.select_features(FSmethod, FSparams, args.selectionFeaturesPath, args.manualFeaturesPath, args)
print(f'Features selected by {FSmethod}:')
print(selectedFeatures)

# Max_Rel_Features = ['wavelet-HL_glrlm_LongRunEmphasis_T2_T2M', 'gradient_glrlm_GrayLevelNonUniformity_T2_T2M', 'wavelet-HL_glszm_ZoneVariance_T2_T2M', 'original_firstorder_Skewness_T2_T2M', 'wavelet-HL_glrlm_RunVariance_T2_T2M', 'wavelet-HL_glcm_ClusterProminence_T2_T2M', 'lbp-2D_firstorder_RootMeanSquared_T2_T2M', 'wavelet-HL_glcm_DifferenceVariance_T2_T2M', 'wavelet-HL_glcm_Contrast_T2_T2M', 'lbp-2D_glcm_Correlation_T2_T2M', 'wavelet-HH_glcm_Contrast_T2_T2M', 'wavelet-HH_glszm_ZoneVariance_T2_T2M', 'logarithm_glrlm_LongRunEmphasis_T2_T2M', 'logarithm_glrlm_RunVariance_T2_T2M']

# selectedFeatures = Max_Rel_Features
# print(selectedFeatures)

# Prediction models

# # Prediction model 1
# MLmethod = 'RFreg'
# rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
#             'max_depth': [None, 1, 3, 5, 10, 15],
#             'max_features': [0.33, 0.67, 1.0, 'sqrt']}  
# scoring = 'r2'

# # Prediction model 2
# MLmethod = 'RFclass'
# rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
#             'max_depth': [None, 1, 3, 5, 10, 15],
#             'max_features': [0.33, 0.67, 1.0, 'sqrt']}  
# scoring = 'r2'

# Prediction model 3
MLmethod = 'RFclass'
rfParams = {'n_estimators': [5, 10, 15, 25, 50, 75], 
            'max_depth': [None, 1, 3, 5, 10, 15],
            'max_features': [0.33, 0.67, 1.0, 'sqrt'],
            'class_weight': "balanced"}  
scoring = 'r2'

# # Prediction model 4
# MLmethod = 'LogReg'
# rfParams = {'penalty': 'l2', 
#             'multi_class': 'ovr'}  
# scoring = 'r2'

yTrueTest, yPredRegTest, yTrueVal, yPredRegVal, MLparams = mlpred.create_evaluate_model(args, MLmethod, rfParams, selectedFeatures, args.selectionFeaturesPath, args.manualFeaturesPath, args.paramSearchResultsPath, optimizeParams=True, scoringOptiMetric=scoring)

# Write validation- and test- results to csv-file
#mlpred.write_results_to_csv(args.predResultsPath, args.selectionFeaturesPath, FSmethod, FSparams, selectedFeatures, MLmethod, MLparams, yTrueTest, yPredRegTest, yTrueVal, yPredRegVal)

print("Done!")




