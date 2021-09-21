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
    
    for i in sorted(os.listdir(args.path_Nrrd_data)):
        if os.path.isfile(os.path.join(args.path_Nrrd_data, i, 'DICOM.nrrd')) and os.path.isfile(os.path.join(args.path_Nrrd_data, i, args.mask2use[0] + '.nrrd')):
            Patient_IDs.append(i)
            DICOM_Nrrd_paths.append(os.path.join(args.path_Nrrd_data, i, 'DICOM.nrrd'))
            T2M_Nrrd_paths.append(os.path.join(args.path_Nrrd_data, i, args.mask2use[0] + '.nrrd'))
    
    dict = {'Patient_ID': Patient_IDs, 'DICOM_paths': DICOM_Nrrd_paths, args.mask2use[0] + '_paths': T2M_Nrrd_paths}
    df = pd.DataFrame(dict)
    df.to_csv(args.df_nrrd)
    
    
if __name__ == "__main__":
    args = parse_args()
    main(args)
    print("Done!")