"""
Create a dataframe with the following columns:

Sl No. | Patient ID | DICOM path | Tiff T2M path | Tiff T2M+ path | Mask T2M path | Mask T2M+ path |

DICOM path - Path where all the dicom slices of each patient is stored.
TIFF path - Path where all the tiff slices of each patient is stored.
"""
import sys
sys.path.append("/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/")
from config import parse_args
import os
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

def get_T2_DICOM_path(path_DICOM, i):
    path_pat = os.path.join(path_DICOM, i)
    path_T2 = os.path.join(path_pat, i.split('_')[0] + '_T2')

    path_temp_1 = os.listdir(path_T2)
    for j in path_temp_1:
        if not os.path.isfile(os.path.join(path_T2, j)):
            path = os.path.join(path_T2, j)
            path_temp_2 = os.listdir(path)
            for k in path_temp_2:
                if not os.path.isfile(os.path.join(path, k)):
                    final_path = os.path.join(path, k)
    return final_path

def get_T2_tiff_path(path_TIFF, i, annotations='T2M'):
    """
    Get the path where all the T2M/T2M+ tiff annotations of each patient are stored.
    """
    path_pat = os.path.join(path_TIFF, i)
    final_path = os.path.join(path_pat, i + annotations)
    return final_path

def main():
    # Create dataframe for raw DICOM T2 sequence
    args = parse_args()
    path = args.path_DICOM_data
    DICOM_paths = []
    Patient_ID_DICOM = []
    pat_data = sorted(os.listdir(path))
    for i in pat_data:
        final_path = get_T2_DICOM_path(path, i)
        DICOM_paths.append(final_path)
        Patient_ID_DICOM.append(i)

    path = args.path_TIFF_data
    Patient_ID_TIFF = []
    TIFF_paths = []
    pat_data = sorted(os.listdir(path))
    for i in pat_data:
        final_path = get_T2_tiff_path(path, i, args.annotations[0])
        TIFF_paths.append(final_path)
        Patient_ID_TIFF.append(i)

    for i in range(len(Patient_ID_DICOM)):
        Patient_ID_DICOM[i] = Patient_ID_DICOM[i].replace('_DICOM', '')

    dict = {'Patient_ID': Patient_ID_DICOM, 'DICOM_paths': DICOM_paths}
    df1 = pd.DataFrame(dict)
    dict = {'Patient_ID': Patient_ID_TIFF, 'TIFF_T2M_paths': TIFF_paths}
    df2 = pd.DataFrame(dict)
    df = pd.merge(df1, df2, how="inner", on="Patient_ID")
    
    df['TIFF_T2M+_paths'] = df['TIFF_T2M_paths'] + "+"
    df['Mask_T2M_paths'] = df['TIFF_T2M_paths']
    df['Mask_T2M_paths'] = df.Mask_T2M_paths.replace({'T2M':'_Mask_T2M'}, regex=True)
    df['Mask_T2M+_paths'] = df['Mask_T2M_paths'] + "+"
    
    # Remove Patient IDs where either T2M or T2M+ folder is empty
    temp_IDs = []
    for index, i in df.iterrows():
        if len(os.listdir(i['Mask_T2M_paths'])) == 0 or len(os.listdir(i['Mask_T2M+_paths'])) == 0:
            temp_IDs.append(i['Patient_ID'])
    df = df[~df['Patient_ID'].isin(temp_IDs)].reset_index(drop=True)

    # Write all the patient's ID into a text file where either the DICOM or the TIFF does not exist.
    uncommon_patients = set(Patient_ID_DICOM)^set(Patient_ID_TIFF)
    textfile = open("/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/save_files/patients.txt", "w")
    for element in uncommon_patients:
        textfile.write(element + "\n")
    textfile.close()

    df.to_csv('/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/save_files/df_raw.csv')
    
if __name__ == "__main__":
    main()
    print("Done!")
    