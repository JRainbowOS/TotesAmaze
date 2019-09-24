from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize
import numpy as np

# img_path = r"C:\Users\YS15101711\Documents\Python Scripts\TotesAmaze\bitmaps\hampton_court - Copy.png"
img_path = r"C:\Users\JRainbow\Documents\Python Scripts\TotesAmaze\bitmaps\hampton_court - Copy.png"
img = imread(img_path, as_grey=True)

print(img.shape)
#img.resize((24,40))
binarized = np.where(img > 0.5, 1, 0)
image_rescaled = (1e8 * rescale(binarized, 0.19))
image_resized = resize(binarized, (23, 39))
vals = np.unique(image_resized)

change_lower = np.where(image_resized == vals[0], 0, image_resized)
#change_middle = np.where(change_lower == vals[1], 1, change_lower)
change_upper = np.where(change_lower == vals[-1], 1, change_lower)
change_upper[-1][19] = 1
change_upper[14][19] = 1

print(np.unique(change_upper))

imsave(r"C:\Users\JRainbow\Documents\Python Scripts\TotesAmaze\bitmaps\hampton_court_bitmap.png", (255 * change_upper.astype(np.uint8)))

fig, ax = plt.subplots(1,1, figsize=(15,15))
ax.imshow(255 * change_upper)