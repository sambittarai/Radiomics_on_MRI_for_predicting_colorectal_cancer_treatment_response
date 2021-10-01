import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    
    # Data Paths
    parser.add_argument("--path_Nrrd_data", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/Data_Nrrd", help="Path where all kinds of Nrrd data for all the patients is located/saved")
    
    parser.add_argument("--path_TIFF_data", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/Data_TIFF", help="Path where all the Patient's TIFF data is located")
    
    parser.add_argument("--path_DICOM_data", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/Data_DICOM", help="Path where all the Patient's DICOM data is located")
    
    parser.add_argument("--annotations", default=["T2M", "T2M+"], help="Path where all the T2M/T2M+ tiff annotations of each patient are stored")
    
    # df paths
    parser.add_argument("--df_raw", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/save_files/df_raw.csv", help="df with the following paths:- | Sl No. | Patient ID | DICOM path | Tiff T2M path | Tiff T2M+ path | Mask T2M path | Mask T2M+ path |")
    
#     parser.add_argument("--manualFeaturesPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/manual_features/manual_features_Emil.csv", help="Path to csv-file containing patient numbers and manually calculated features")
    
    parser.add_argument("--manualFeaturesPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/manual_features/manual_features_new.csv", help="Path to csv-file containing patient numbers and manually calculated features")
    
    parser.add_argument("--selectionFeaturesPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/feature_extraction/selection_features.csv", help="path to csv-file where to write all the extracted features")
    
    parser.add_argument("--DicomHtmlPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/DICOM_HTML", help="dicom_features")
    
    parser.add_argument("--df_nrrd", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/save_files/df_nrrd.csv", help="dataframe with path to the .nrrd files with the following columns:- | Sl No. | Patient ID | DICOM path | T2M path or T2M+ path |")
    
    # save files
    parser.add_argument("--save", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/save_files", help="save files")
    
    # Feature Extraction
    parser.add_argument("--paramsPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/Params.yaml", help="Path to Radiomics Parameter File")
    parser.add_argument("--img2use", default="T2", help="Type of MRI series used for feature extraction")
    parser.add_argument("--mask2use", default=["T2M"], help="Type of masks used for feature extraction (T2M or T2M+)")
    
    # Testing
    parser.add_argument("--paramSearchResultsPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/Predictions/param_search_results.csv", help="path to csv-file that will be created, containing results from the parameter optimization")
    parser.add_argument("--testIds", default=['Pat1'], help="Test IDs")
#     parser.add_argument("--testIds", default=['Pat1', 'Pat2', 'Pat4', 'Pat6', 'Pat9', 'Pat10', 'Pat20', 'Pat21', 'Pat40', 'Pat43', 'Pat44', 'Pat46', 'Pat54', 'Pat55', 'Pat101'], help="Test IDs")
    parser.add_argument("--predResultsPath", default="/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/Predictions/prediction_results.csv", help="Path to the csv-file where to write the results")
    
    # Data
    parser.add_argument("--reverse_IDs", default=['Pat10', 'Pat25', 'Pat30', 'Pat31', 'Pat32', 'Pat63', 'Pat64', 'Pat65', 'Pat73', 'Pat74', 'Pat75', 'Pat76', 'Pat77', 'Pat78', 'Pat79', 'Pat80', 'Pat82', 'Pat83', 'Pat84', 'Pat85', 'Pat86', 'Pat87', 'Pat88', 'Pat103', 'Pat107', 'Pat108', 'Pat109', 'Pat110', 'Pat111', 'Pat112', 'Pat113', 'Pat115', 'Pat116', 'Pat117', 'Pat118'], help="Patient IDs where the annotation is in the reverse order to that of the DICOMs")
    
    # Manual IDs (Pat IDs where generate_masks.py fail for T2M)
    parser.add_argument("--Manual_IDs_T2M", default=['Pat6', 'Pat8', 'Pat10', 'Pat11', 'Pat13', 'Pat21', 'Pat26', 'Pat31', 'Pat32', 'Pat42', 'Pat46', 'Pat51', 'Pat65', 'Pat70', 'Pat71', 'Pat74', 'Pat75', 'Pat81', 'Pat85', 'Pat88', 'Pat94', 'Pat101', 'Pat103', 'Pat108', 'Pat111', 'Pat112', 'Pat113', 'Pat116', 'Pat118'], help="Patient IDs where mask generation failed")
    
    args = parser.parse_args()
    return args