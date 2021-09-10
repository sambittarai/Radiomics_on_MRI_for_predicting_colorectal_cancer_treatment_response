import cv2
import numpy as np
import os
import csv
import re

def create_mask(imagePath, addInterior=True):
    """ 
    ACTION: 
        Generates a black and white mask of the input image
        The white area corresponds to green markings in the
        file including any interior points and the rest is black. 
        Note that this algorithm fails in some situations, 
        check the output visually to make sure it is correct. 
    INPUTS: 
        imagePath: path to image file
        addInterior: True/False, whether the pixels inside the green line should be labeled white or not
    OUTPUT: 
        1 if mask was created, 0 if not
    """

    # Read image (if it exists) and make copy for comparison
    if cv2.haveImageReader(imagePath):
        originalImage = cv2.imread(imagePath)
    else:
        print(f"Failed to read input file at {imagePath}")
        return 0
    image = originalImage.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color range and mask everything within range
    lower = np.array([50, 125, 125], dtype="uint8")
    upper = np.array([100, 255, 255], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    if addInterior:
        # Add interior points to mask
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        mask = cv2.fillPoly(mask, cnts, (255, 255, 255))
        mask = erosion(mask) # Perform erosion on mask

    # Save the output
    # if not cv2.imwrite(maskPath, mask):
    #     print(f"Failed to write output file at {maskPath}")

    return mask

def erosion(inputMask):
    """
    ACTION: 
        Performs erosion on the input mask, returns the result
    INPUTS: 
        inputMask: binary mask on which to perform erosion on
    OUTPUT: 
        Eroded version of the input mask
    """
    kernel = np.ones((3,3),np.uint8)
    kernel[0,0] = 0
    kernel[0,-1] = 0
    kernel[-1,0] = 0
    kernel[-1,-1] = 0
    return cv2.erode(inputMask,kernel,iterations = 1)

def extract_dicom_feature(dicomPath, feature):
    """ 
    ACTION: 
        Reads html-file with DICOM header information, searches for the feature and outputs the value 
    INPUTS: 
        dicomPath: path to the html-file with DICOM header information
        feature: the feature of interest as a string, note that it is case sensitive
    OUTPUT:
        value of the given feature, 0 if feature can't be found in the file
    """

    htmlData = open(dicomPath, 'rb').read().decode('utf-16') #Open file in correct format

    # Extract string contain feature, everything inbetween, and the value
    tdfeatureString = re.findall('<td>' + feature + '</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td><td>.*?</td>', htmlData)

    # Check that the feature was found
    if len(tdfeatureString) > 0:
        tdValue = re.findall('<td>.*?</td>', tdfeatureString[0])  # List all <td> </td> found in the string, the last value is the one of interest
        value = re.sub('</*td>', '', tdValue[-1]) # remove <td> and </td> and get the last value
        return value 

    # Print text and return 0 if the extraction failed.
    else:
        print(f'Could not find {feature} in HTML file')
        return 0

def extract_dicom_features(dataPath, features = ['Patients Sex', 'Patients Weight', 'Pixel Spacing', 'Spacing Between Slices']):
    """
    ACTION: 
        Reads html-file with DICOM header information for all patients, creates a csv with content of interest and returns a dictionary for all patients with the same content.
    INPUTS: 
        dataPath: path to the folder containg all the data, the structure inside this folder is important and specified in 'README.md'
        features: list of features to extract from DICOM-files
    OUTPUT:
        A dictionary containing dictionaries for each patient with its DICOM features 
    """

    # Create a dictionary which will contain a dictionary for each patient
    allPatsDict = {}

    # Create file for output
    outcomePath = dataPath + "/dicom_features.csv"
    with open(outcomePath, "w") as f:
        f.truncate() 

    # Create list with all existing patient IDs in the data folder
#     folderContent = os.listdir(dataPath)
#     patIds = [x for x in folderContent if re.search('^Pat[0-9]?[0-9]?[0-9]$', x)]
    
    patIds = [x for x in sorted(os.listdir(dataPath))]
    # Go through all the patients
    for patientId in patIds:
        ID = patientId.split('_')[0]
        #path to html file
        dicomPath = os.path.join(dataPath, patientId, ID + '_T2.HTML')
#         dicomPath = dataPath + "/DICOM/" + patientId + "T2.HTML" #path to html file
        patDict = {} # new dictionary

        # Check that we have HTML file
        if os.path.isfile(dicomPath):
            for feature in features:
                patDict[feature] = extract_dicom_feature(dicomPath, feature) # Read HTML file

            # Some readings requires manual adjustments
            if 'Pixel Spacing' in features:
                pixelSpacing = patDict['Pixel Spacing'].split('\\')
                patDict['Pixel Spacing x'] = pixelSpacing[0]
                patDict['Pixel Spacing y'] = pixelSpacing[1]
                
            if 'Patients Sex' in features:
                patSex = patDict['Patients Sex']
                patDict['Patients Sex'] = 0 if patSex == 'M' else 1

            # Store patient dict in all patients dict
            allPatsDict[patientId[3:]] = patDict

        # Header in CSV is the keys from the dictionary
        header = list(patDict.keys())

        # Check if file is empty, if it is we also create the header
        if os.path.getsize(outcomePath) == 0:
            with open(outcomePath, 'w', newline='') as File:
                writer = csv.DictWriter(File, fieldnames=header, delimiter = ';')
                writer.writeheader()
                writer.writerow(patDict)

        # If file is not empty we append the new content
        else:
            with open(outcomePath, 'a', newline='') as File:
                writer = csv.DictWriter(File, fieldnames=header, delimiter = ';')
                writer.writerow(patDict)

    return allPatsDict