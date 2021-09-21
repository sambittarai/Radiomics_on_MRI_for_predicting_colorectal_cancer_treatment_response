from PIL import Image
import numpy as np
from utils import erosion
import os

path = "/media/sambit/HDD/Sambit/Projects/Radiomics_Project1/Data/Data_Dummy_new/apply erosion"

for i in sorted(os.listdir(path)):
    path_temp = os.path.join(path, i)
#     print(i)
    for j in sorted(os.listdir(path_temp)):
        img_temp = np.asarray(Image.open(os.path.join(path_temp, j)))
        img_temp = np.where(img_temp>0, 255, 0).astype('uint8')
        img_temp = erosion(img_temp)
        mask = Image.fromarray(img_temp)
        save_path = os.path.join(path_temp, j)
        mask.save(save_path)

print("Done!")
