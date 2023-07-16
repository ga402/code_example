# Basic class for greyscale 3D images/numpy arrays
#

import matplotlib.pyplot as plt
from func import *


class baseImage:
    def __init__(self, image):
        try:
            self.image = image
            self.z, self.y, self.x = self.image.shape
            self.z_levels = range(self.z)
            print(
                f"image loaded.\ny={self.image.shape[1]}\nx={self.image.shape[2]}\nz={self.image.shape[0]}"
            )
        except:
            print("unable to load image file")

    def showImage(self, level, save=False, figure_name="figure"):
        if level > self.image.shape[0] or level < 0:
            return print(
                f"level outside the z dimensions of image  (0 to {image.shape[0]})"
            )
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(self.image[level, :, :], cmap="gray")
        plt.axis("off")
        if save == True:
            plt.savefig(f"{figure_name}.png")
        plt.show()

    def getImage(self):
        return self.image

    def printShape(self):
        print(
            f"\ny={self.image.shape[1]}\nx={self.image.shape[2]}\nz={self.image.shape[0]}"
        )

    def getDim(self):
        return self.z, self.y, self.x
