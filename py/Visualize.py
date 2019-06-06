#  Data visualization class
#
#  4D Plot, Slices, etc 

import numpy as np
import matplotlib.pyplot as plt

class Visualize:
    

    def __init__(self):
        pass

    #Sets xyz resolution, parameter is resolution tuple
    def set_resolution(self, res):
        self.res = res
        self.x,self.y,self.z = np.indices((res[0],res[1],res[2]))
        self.sphere = np.sqrt(np.square(self.x-5) + np.square(self.y-5) + np.square(self.z-5))

    def update_noise(self):
        self.frame = np.random.standard_normal(self.res[0]*self.res[1]*self.res[2])

    def plot(self):
        fig = plt.figure()
        ax = fig.gca()
        ax.voxels(self.sphere, edgecolor='k')
        plt.show()




if __name__ == '__main__':
    vis = Visualize()
    vis.set_resolution((10,10,10))
    vis.plot()
