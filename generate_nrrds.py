import numpy as np
import nrrd
import cv2
import os
import csv
import SimpleITK as sitk
from PIL import Image
from tqdm import tqdm
from config import parse_args
import pandas as pd
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

def load_DICOM(path, get_spacing=True):
    try:
        series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path)
        series_file_names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(path, series_IDs[0])
        series_reader = sitk.ImageSeriesReader()
        series_reader.SetFileNames(series_file_names)
        image3D_dcm = series_reader.Execute()
        image3D_arr = sitk.GetArrayFromImage(image3D_dcm)
        if get_spacing == True:
            spacing = {'x_spacing' : image3D_dcm.GetSpacing()[0], 'y_spacing' : image3D_dcm.GetSpacing()[1], 'z_spacing' : image3D_dcm.GetSpacing()[2]}
            return image3D_arr, spacing
        else:
            return image3D_arr
    except:
        print("DICOM cannot be loaded with this function. Try others")
        
def load_Masks(path):
    mask_list = []
    for i in sorted(os.listdir(path)):
        mask = np.asarray(Image.open(os.path.join(path, i)))
        mask_list.append(mask)

    mask_arr = np.stack(mask_list, axis=0)     
    return mask_arr

def create_3d_nrrd(data, dataPath, name, patientDict):
    # Add spacing information in nrrd header    
    spacings = [patientDict['x_spacing'], patientDict['y_spacing'], patientDict['z_spacing']]
    header = {'spacings' : spacings}
#     nrrd.write(dataPath + '.nrrd', data, header) # Write 3D-nrrd-file
    nrrd.write(os.path.join(dataPath, name), data, header) # Write 3D-nrrd-file
    return 1
        
def main():
    args = parse_args()
    save_nrrd_path = args.path_Nrrd_data
    df = pd.read_csv(args.df_raw)
    
    for index, i in tqdm(df.iterrows()):
        DICOM_path, Mask_T2M_path, Mask_T2Mplus_path  = i['DICOM_paths'], i['Mask_T2M_paths'], i['Mask_T2M+_paths']
        # Get array from Image
        image_arr, spacing = load_DICOM(DICOM_path, get_spacing=True)
        mask_T2M_arr = load_Masks(Mask_T2M_path)
        mask_T2Mplus_arr = load_Masks(Mask_T2Mplus_path)
        # Generate .nrrd files for those patients where DICOM.shape == Mask_T2M.shape == Mask_T2M+.shape.
        if image_arr.shape == mask_T2M_arr.shape and image_arr.shape == mask_T2Mplus_arr.shape:
            # Generate Nrrds and save it
            save_temp = os.path.join(save_nrrd_path, i['Patient_ID'])
            if not os.path.exists(save_temp):
                os.mkdir(save_temp)
                # Generate Nrrd for DICOM
                create_3d_nrrd(image_arr, save_temp, 'DICOM.nrrd', spacing)
                # Generate Nrrd for T2M
                create_3d_nrrd(mask_T2M_arr, save_temp, 'T2M.nrrd', spacing)
                # Generate Nrrd for T2M+
                create_3d_nrrd(mask_T2Mplus_arr, save_temp, 'T2M+.nrrd', spacing)
            elif len(os.listdir(save_temp)) != 3:
                create_3d_nrrd(image_arr, save_temp, 'DICOM.nrrd', spacing)
                create_3d_nrrd(mask_T2M_arr, save_temp, 'T2M.nrrd', spacing)
                create_3d_nrrd(mask_T2Mplus_arr, save_temp, 'T2M+.nrrd', spacing)
            else:
                pass
        else:
            print("Dimension of DICOM, T2M, T2M+ do not match: {}",format(i['Patient_ID']))
    
if __name__ == "__main__":
    main()
    print("Done!")
    
    
    






