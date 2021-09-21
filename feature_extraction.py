import cv2 
import os
from radiomics import featureextractor, setVerbosity
import scipy
# import trimesh
from tqdm import tqdm
import csv
import re
from config import parse_args
from utils import extract_dicom_features
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def extract_features_from_image(imagePath, maskPath, paramsPath):
    """
    ACTION: 
        Extract radiomic features from one image, given mask and parameters, 
        and return a dictionary with the feature values
    INPUT: 
        imagePath: path to image nrrd-file (without extension)
        maskPath: path to mask nrrd-file (without extension)
        paramsPath: path to file with radiomic feature extraction settings
    OUTPUT: 
        dictionary with all extracted features
    """
    if not os.path.isfile(imagePath):
        raise IOError('File does not exist: %s' % img)
    elif not os.path.isfile(maskPath):
        raise IOError('File does not exist: %s' % mask)
    elif not os.path.isfile(paramsPath):
        raise IOError('File does not exist: %s' % paramsPath)
    
    extractor = featureextractor.RadiomicsFeatureExtractor(paramsPath)
    setVerbosity(40) # Set level of verbosity, 40=Errors, 30=Warnings, 20=Info, 10=Debug
    results = extractor.execute(imagePath, maskPath)
    return results

def extract_features_from_patient(df, patientId, img2use, mask2use, paramsPath, selectionFeaturesPath, manualFeaturesDict, dicomFeaturesDict):
    """
    ACTION: 
        Extract all features from a patient and write the result to a csv (selectionFeaturesPath).
    INPUT:  
        dataPath: path to the folder containg all the data, the structure inside this folder is important and specified in 'README.md'
        patientId: Patient ID in string format, ex "13"
        img2use: list of types of scans to extract features from, ex ["T1", "T2", "Diff", "ADC"]
        mask2use: list of masks to use for extracting features, ex ["M", "M+", "Mfrisk"]
        paramsPath: path to file with radiomic feature extraction settings
        selectionFeaturesPath: path to csv-file where to write the result
        manualFeaturesDict: Dictionary with manually calculated features for this patient
        dicomFeaturesDict: Dictionary with features for this patient extracted from the html-file with DICOM header information
    OUTPUT: 
        1 if extraction was successful, 0 if not
    """    
    # Add patient ID first in the dictionary
    features = {"patientId": patientId} 
    # Add manually extracted, and dicom- features to the directory 
    features.update(manualFeaturesDict)
    features.update(dicomFeaturesDict)
    
    # We are only using T2 MRI images
    imagePath = df['DICOM_paths'].to_string().split(' ')[-1]    
    # Go through all masks and get mask paths (T2M, T2M+)
    for mask in mask2use:
        maskPath = df[mask + '_paths'].to_string().split(' ')[-1]
        # Extract radiomic features
        try:
            radiomicFeaturesDict = extract_features_from_image(imagePath, maskPath, paramsPath)
        except:
            return 0 # Extraction failed
        # Add suffix specifying image and mask and append to features dictionary
        radiomicFeaturesDict = {k + '_' + img2use + '_' + mask: v for k, v in radiomicFeaturesDict.items()}
        features.update(radiomicFeaturesDict)
        
    # List all the feature names  
    header = list(features.keys())    
    # If file is empty we create the header and then add the content
    filesize = os.path.getsize(selectionFeaturesPath)
    if filesize == 0:
        with open(selectionFeaturesPath, 'w', newline='') as featuresFile:
            writer = csv.DictWriter(featuresFile, fieldnames=header, delimiter = ';')
            writer.writeheader()
            writer.writerow(features)
    # If file is not empty we append the new content
    else:
        with open(selectionFeaturesPath, 'a', newline='') as featuresFile:
            writer = csv.DictWriter(featuresFile, fieldnames=header, delimiter = ';')
            writer.writerow(features)
    
    return 1 # Successful extraction

def extract_manual_feature(manualFeaturesPath, features):
    """
    ACTION: 
        Open a csv-file with patient information created manually, read the content and create a dictionary with dictionaries containing specified features
    INPUT: 
        manualFeaturesPath: Path to csv-file containing patient numbers and manually calculated features, structure of the file is specified in 'README.md'
        features: A list of features (strings) to put in the dictionary 
    OUTPUT: 
        allPatsDict: A dictionary with patient number (string) as key, and dictionary with features as value
    """
    allPatsDict = {} # Directory containing directories
    with open(manualFeaturesPath, 'r', newline='') as csvFile: # Open the file
        #reader = csv.DictReader(csvFile, delimiter=';') # Create a reader
        reader = csv.DictReader(csvFile) # Create a reader
        for row in reader: # For every row in the csv-file, add a tuple to the dictionary
            patDict = {} # Create a directory with features for every patient
            for feature in features:
                patDict[feature] = row[feature] # Adding feature to patients directory
            allPatsDict[row['id']] = patDict # Adding the directory to the 'One directory to rule them all'
    return allPatsDict

def main(args):
    df_nrrd = pd.read_csv(args.df_nrrd)
    with open(args.selectionFeaturesPath, "w") as f:
        f.truncate()
    # Collect
    manualFeaturesDict = extract_manual_feature(args.manualFeaturesPath, ['age', 'treatment'])
    dicomFeaturesDict = extract_dicom_features(args.DicomHtmlPath, ['Patients Sex', 'Patients Weight'])
    
    # Updating the Dictionary keys
    dicomFeaturesDict = { 'Pat' + k.replace('_DICOM', ''): v for k, v in dicomFeaturesDict.items() }
#     manualFeaturesDict = { 'Pat' + k: v for k, v in manualFeaturesDict.items() }
    
    # All patient IDs with a DICOM-file
    DICOM_IDs = list(dicomFeaturesDict.keys())
    # All patient IDs with nrrds
    Nrrd_IDs = df_nrrd['Patient_ID']
    # All patient IDs with images, dicom-files, age and outcome
    pat_IDs = []
    for id in Nrrd_IDs:
        if id in DICOM_IDs:
            pat_IDs.append(id)
        else:
            print("DICOM HTML file does not exists: ", id)

    print("pat_IDs length: {}, NRRDs length: {}, DICOMs length: {}".format(len(pat_IDs), len(Nrrd_IDs), len(DICOM_IDs)))
    # Extract features for every patient and put the result in a file
    for patientId in tqdm(sorted(pat_IDs)):
        if extract_features_from_patient(df_nrrd[df_nrrd['Patient_ID'] == patientId], patientId, args.img2use, args.mask2use, args.paramsPath, args.selectionFeaturesPath, manualFeaturesDict[patientId], dicomFeaturesDict[patientId]):
            print(f"{patientId}: features extracted")
        else:
            print(f"{patientId}: failed to extract features")
    
if __name__ == "__main__":
    args = parse_args()
    main(args)
    print("Done!")