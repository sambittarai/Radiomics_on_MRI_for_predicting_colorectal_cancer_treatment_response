'''
| Sl No. | Patient ID | DICOM path | T2M path | T2M+ path |
'''

from config import parse_args
import os
import pandas as pd

def main(args):
    Patient_IDs = []
    DICOM_Nrrd_paths = []
    T2M_Nrrd_paths = []
    T2Mplus_Nrrd_paths = []
    for i in sorted(os.listdir(args.path_Nrrd_data)):
        Patient_IDs.append(i)
        DICOM_Nrrd_paths.append(os.path.join(args.path_Nrrd_data, i, 'DICOM.nrrd'))
        T2M_Nrrd_paths.append(os.path.join(args.path_Nrrd_data, i, 'T2M.nrrd'))
        T2Mplus_Nrrd_paths.append(os.path.join(args.path_Nrrd_data, i, 'T2M+.nrrd'))
    
    dict = {'Patient_ID': Patient_IDs, 'DICOM_paths': DICOM_Nrrd_paths, 'T2M_paths': T2M_Nrrd_paths, 'T2M+_paths': T2Mplus_Nrrd_paths}
    df = pd.DataFrame(dict)
#     df.to_csv(os.path.join(args.save, 'df_nrrd.csv'))
    df.to_csv(args.df_nrrd)
    
    
if __name__ == "__main__":
    args = parse_args()
    main(args)
    print("Done!")