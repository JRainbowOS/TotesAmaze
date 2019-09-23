from skimage.io import imread, imsave
#import matplotlib.pyplot as plt
from skimage.transform import rescale
import numpy as np

img_path = r"C:\Users\YS15101711\Documents\Python Scripts\TotesAmaze\bitmaps\hampton_court - Copy.png"
img = imread(img_path, as_grey=True)

print(img.shape)
#img.resize((24,40))
binarized = np.where(img > 0.5, 1, 0)
image_rescaled = rescale(binarized, 0.125, anti_aliasing=False)
print(image_rescaled)