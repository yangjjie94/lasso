# import the required libraries
import glob
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

%matplotlib inline

import cv2

from torch.utils.data import Dataset, DataLoader

class DropDectectionDataset(Dataset):
    """
    Face Landmarks dataset.
    
    param:
    - root_dir: "data" dir
    - transform
    """

    def __init__(self, root_dir, transform=None):
#     def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
#         self.key_pts_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        os.chdir(root_dir)
        self.img_names = sorted(glob.glob('*/*.jpg'))

    def __len__(self):
        return len(self.img_names)
        

    def __getitem__(self, idx):
#         image_name = os.path.join(self.root_dir,
#                                 self.key_pts_frame.iloc[idx, 0])
        
#         image = mpimg.imread()
        imgname = os.path.join(self.root_dir, self.img_names[idx])
        image = cv2.imread(imgname, cv2.IMREAD_GRAYSCALE)
#         # if image has an alpha color channel, get rid of it
#         if(image.shape[2] == 4):
#             image = image[:,:,0:3]
        
#         key_pts = self.key_pts_frame.iloc[idx, 1:].as_matrix()
#         key_pts = key_pts.astype('float').reshape(-1, 2)
        key_pts = None 
        sample = {'image': image, 'keypoints': key_pts}

        if self.transform:
            sample = self.transform(sample)

        return sample
    
    
def show_hist(mat):
    plt.hist(mat.ravel(),256,[0,256]); plt.show()
    
    
def show_imgs(imgs, exist_beta=None):
    for idx, img in enumerate(imgs, 1):
        if exist_beta:
            print('image #{}: beta={:.2f}'.format(idx, 0.1*BIN_BG_BETA[idx-1]))
        else:
            print('image #{}:'.format(idx))
        plt.figure(12, figsize=(30,10))
        plt.subplot(121)
        plt.imshow(img, cmap='gray')

        plt.subplot(122)
        show_hist(img)

def get_subtraction(dataset, n=None):
    """
    subtract the background
    compute the background (mean of n images)and then get it subtracted from each pic.
    """
    if len(dataset) > 0:    
        bgimg = np.zeros(dataset[0]['image'].shape)
    else:
        return None
    
    if not (n or (n < len(dataset))):
        n = len(dataset)
    
    for idx in range(n):
        bgimg = np.add(bgimg, dataset[idx]['image'])
    bgimg /= n
    
    return bgimg
    
    
def bg_sub(img, bg, beta=1):
    """
    subtract background from input img
    """
    assert (img.shape == bg.shape)
    output = np.subtract(beta * bg, img)
    # 解决正负号的问题
    
    # 强行截断是不对的
#     output[output >= 0] = 1
#     output[output < 0] = 0
    # 规整化不能重复
    # 取绝对值：证明效果最好
    output = abs(output)
    assert output.min() >= 0
    return output


def crop(img, bound=None):
    """
    crop the image into a given shape and return cropped image
    
    params:
    - img: input image
    - bound: boundary, input 4 int number, left, top, right, bottem
    """
    if not bound:
        left = 0; top = 0; right, bottem = img.shape
        bound = (left, top, right, bottem)
    assert len(bound) == 4
    
    left, top, right, bottem = bound
    output = img[top:bottem, left:right]
    
    return output


def Clahe(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(np.array(img, dtype=np.uint8))

