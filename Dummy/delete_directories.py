import shutil
import os
from tqdm import tqdm
import sys
sys.path.append("/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Code/Radiomics/")
from config import parse_args

def main():
    args = parse_args()
    path_TIFF = args.path_TIFF_data
    for i in tqdm(sorted(os.listdir(path_TIFF))):
        for j in sorted(os.listdir(os.path.join(path_TIFF, i))):
            if j == "Mask_T2M" or j == "Mask_T2M+":
#                 print(i)
                shutil.rmtree(os.path.join(path_TIFF, i, j))
        
if __name__ == "__main__":
    main()
    print("Done!")
    