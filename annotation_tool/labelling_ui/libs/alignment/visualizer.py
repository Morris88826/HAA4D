import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import glob
import matplotlib.cm as cm

from numpy.core.defchararray import title

def visualize_camera(joints3d, camera_positions):
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    bones_indices = [
        [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
        [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
        [[0,7],[7,8],[8,9],[9,10]] # black
    ] # left-> pink, right->blue

    for _, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, z0 = list(joints3d[start])
            x1, y1, z1 = list(joints3d[end])
            ax.plot([x0, x1], [y0, y1], [z0, z1])
    # draw dots
    ax.scatter(joints3d[:, 0], joints3d[:, 1], joints3d[:, 2])
    ax.set(xlim=[-1000, 1000], ylim=[-1000, 1000], zlim=[-1000, 1000], title='Camera Position')

    colors = cm.rainbow(np.linspace(0, 1, 20))

    for i in range(20):
        ax.scatter(camera_positions[i, 0], camera_positions[i, 1], camera_positions[i, 2], label='video {}'.format(i),c=colors[i].reshape(1,-1))
    
    ax.legend()
    plt.show()
    raise NotImplementedError

def visualize_alignment(original, aligned, max_range=None):
    bones_indices = [
        [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
        [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
        [[0,7],[7,8],[8,9],[9,10]] # black
    ] # left-> pink, right->blue


    fig = plt.figure(figsize=plt.figaspect(0.5))
    #===============
    #  First subplot
    #===============
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    if max_range is None:
        max_range = np.amax(np.abs(original))
    ax1.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range, max_range], title='Original')

    for bones in (bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, z0 = list(original[start])
            x1, y1, z1 = list(original[end])
            ax1.plot([x0, x1], [y0, y1], [z0, z1])
    # draw dots
    ax1.scatter(original[:, 0], original[:, 1], original[:, 2])


    #===============
    #  Second subplot
    #===============
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    if max_range is None:
        max_range = np.amax(np.abs(aligned))
    ax2.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range, max_range], title='Aligned')

    for bones in (bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, z0 = list(aligned[start])
            x1, y1, z1 = list(aligned[end])
            ax2.plot([x0, x1], [y0, y1], [z0, z1])
    # draw dots
    ax2.scatter(aligned[:, 0], aligned[:, 1], aligned[:, 2])

    return fig

def visualize(joints, filename='example', max_range=None, save=False):

    bones_indices = [
        [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
        [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
        [[0,7],[7,8],[8,9],[9,10]] # black
    ] # left-> pink, right->blue

    if joints.shape[1] == 2:

        fig, ax = plt.subplots()

        if max_range is None:
            max_range = np.amax(np.abs(joints))
        
        ax.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range])

        for _, bones in enumerate(bones_indices):
            for bone in (bones):
                start = bone[0]
                end = bone[1]

                x0, y0, = list(joints[start])
                x1, y1, = list(joints[end])
                ax.plot([x0, x1], [y0, y1])
        
        # draw dots
        ax.scatter(joints[:, 0], joints[:, 1])

        if save:
            fig.savefig('./{}.png'.format(filename))

    else:
        plot_3d = Figure(figsize=(4, 4), dpi=50)

        ax = plot_3d.add_subplot(111, projection="3d")

        if max_range is None:
            max_range = np.amax(np.abs(joints))
        ax.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range, max_range])
        # ax.view_init(elev=180, azim=0)

        for _, bones in enumerate(bones_indices):
            for bone in (bones):
                start = bone[0]
                end = bone[1]

                x0, y0, z0 = list(joints[start])
                x1, y1, z1 = list(joints[end])
                ax.plot([x0, x1], [y0, y1], [z0, z1])
        # draw dots
        ax.scatter(joints[:, 0], joints[:, 1], joints[:, 2])

        if save:
            plot_3d.savefig('./{}.png'.format(filename))





if __name__ == '__main__':

    target_folder = './dataset/joints3d/burpee'
    for subfolder in sorted(glob.glob(target_folder+'/*')):
        
        filename =  '{:04}.npy'.format(1)
        joints3d = np.load(subfolder+'/'+filename)
        visualize(joints3d, '{}'.format(subfolder.split('/')[-1].replace('.npy', '')))
