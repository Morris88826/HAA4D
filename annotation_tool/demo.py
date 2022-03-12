import numpy as np
import matplotlib.pyplot as plt
import json
import sys
sys.path.insert(1, '..')
from libs.visualizer import plot_2d, plot_3d
from PIL import Image

if __name__ == "__main__":

    class_name = "abseiling"
    video_idx = 0
    frame_idx = 0


    skeleton_2d = np.load(
        "./labelled_data/skeletons_2d/{}/{}_{:03d}.npy".format(class_name, class_name, video_idx))[frame_idx]
    skeleton_3d = np.load(
        "./labelled_data/skeletons_3d/{}/{}_{:03d}.npy".format(class_name, class_name, video_idx))[frame_idx]
    image = np.array(Image.open(
        "../dataset/raw/{}/{}_{:03d}/{:04d}.png".format(class_name, class_name, video_idx, frame_idx+1)))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)
    plot_2d(skeleton_2d, "haa4d", ax, xlim=None)
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plot_3d(skeleton_3d, "haa4d", ax, max_range=1000)
    plt.show()

    try:
        globally_aligned_skeletons = np.load(
            "./dataset/processed_data/globally_aligned_skeletons/haa4d/{}/{}_{:03d}.npy".format(class_name, class_name, video_idx))[frame_idx]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        plot_3d(globally_aligned_skeletons, "haa4d", ax, max_range=1)
        plt.show()
    except:
        print("Globally aligned skeleton not exist.")
