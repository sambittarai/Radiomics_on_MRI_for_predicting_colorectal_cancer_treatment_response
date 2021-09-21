'''
Generate Manual Masks for 'T2M' annotation without adding interior.
'''
import numpy as np
import os
from PIL import Image
import cv2
from tqdm import tqdm
import sys
sys.path.append("/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/")
from utils import create_mask
from config import parse_args
    
def main():
    """
    Generates 2D Binary Masks (for T2M and T2M+) from .tiff files and saves it.
    """
    args = parse_args()
    # List with Patient IDs where masks cannot be generated
    Patients_no_Mask = []
    path_TIFF = args.path_TIFF_data
    # Loop over all the patients. e.g. Pat1, Pat2, ...
    for i in tqdm(sorted(os.listdir(path_TIFF))):
        if i in args.Manual_IDs_T2M:
            try:
                # args.annotations = [T2M, T2M+].
                j = args.annotations[0]
                # Pat1T2M
                ID = i + j
                path = os.path.join(path_TIFF, i, ID)
                mask_dir = os.path.join(path_TIFF, i, i + '_Mask_' + j)
                if not os.path.exists(mask_dir):
                    os.mkdir(mask_dir)
                # Loop over all the .tiff annotations
                for k in sorted(os.listdir(path)):
                    if k.endswith('.tiff'):
                        # Creata mask without adding interior
                        mask = create_mask(os.path.join(path, k), addInterior=False)
                        # Save Mask
                        mask = Image.fromarray(mask)
                        save_path = os.path.join(mask_dir, k.split('.')[0] + '.png')
                        mask.save(save_path)
            except:
                print("Masks cannot be generated for the Patient: {}".format(i))
                Patients_no_Mask.append(i)
    
if __name__ == "__main__":
    main()
    print("Done!")