import glob
import tqdm
import os
import argparse
from libs.alignment.skeleton import Skeleton
from libs.evoskeleton.load_model import EvoNet
import json
import matplotlib.pyplot as plt
import imageio
import numpy as np
import torch
import sys
sys.path.append("../")


def plot_2d_ax(ax, skeleton, add_index=True):
    pose_connection = [[0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6], [0, 7], [7, 8],
                       [8, 9], [9, 10], [8, 11], [11, 12], [12, 13], [8, 14], [14, 15], [15, 16]]

    for segment_idx in range(len(pose_connection)):
        point1_idx = pose_connection[segment_idx][0]
        point2_idx = pose_connection[segment_idx][1]
        point1 = skeleton[point1_idx]
        point2 = skeleton[point2_idx]
        ax.plot([int(point1[0]), int(point2[0])],
                [int(point1[1]), int(point2[1])],
                linewidth=2)
    if add_index:
        for idx in range(skeleton.shape[0]):
            plt.text(skeleton[idx][0],
                     skeleton[idx][1],
                     str(idx),
                     color='b'
                     )
    ax.scatter(skeleton[:, 0], skeleton[:, 1], s=1, c='black')
    # ax.set_xlim(-1280,1280)
    # ax.set_ylim(1280,-1280)
    return


def plot_3d_ax(joints3d, ax, elev=-80, azim=-90):
    max_range = np.amax(np.abs(joints3d))
    ax.set(xlim=[-max_range, max_range], ylim=[-max_range,
           max_range], zlim=[-max_range, max_range])
    # ax.view_init(elev=180, azim=0)

    bones_indices = [
        [[0, 4], [4, 5], [5, 6], [8, 11], [11, 12], [12, 13]],  # left -> pink
        [[0, 1], [1, 2], [2, 3], [8, 14], [14, 15], [15, 16]],  # right -> blue
        [[0, 7], [7, 8], [8, 9], [9, 10]]  # black
    ]  # left-> pink, right->blue

    for i, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, z0 = list(joints3d[start])
            x1, y1, z1 = list(joints3d[end])
            ax.plot([x0, x1], [y0, y1], [z0, z1])

    # draw dots
    sk = Skeleton()
    for i in range(17):
        if sk.dict_idx_2_joint[i] in (sk.body_parts['torso'] + sk.body_parts['head']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='b')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='r')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
            ax.scatter(joints3d[i, 0], joints3d[i, 1], joints3d[i, 2], c='g')
        else:
            raise NotImplementedError

    ax.set(xlabel='x', ylabel='y', zlabel='z')
    ax.view_init(elev=elev, azim=azim)
    return


def visualize(class_name, video_idx, frame_idx):

    image_name = '{}/{}_{:03d}/{:04d}'.format(
        class_name, class_name, video_idx, frame_idx)
    image_path = '../dataset/raw/{}.png'.format(image_name)

    f = plt.figure(figsize=(9, 3))
    ax1 = f.add_subplot(131)
    try:
        img = imageio.imread(image_path)
        ax1.imshow(img)
    except:
        pass

    plt.title('Input image')

    ax2 = f.add_subplot(132)
    num_joints = 17
    plt.title('2D key-point inputs: {:d}*2'.format(num_joints))
    ax2.set_aspect('equal')
    ax2.invert_yaxis()

    skeleton_2d = np.load('../dataset/skeletons_2d/{}/{}_{:03d}.npy'.format(
        class_name, class_name, video_idx))[frame_idx-1]

    plot_2d_ax(ax2, skeleton_2d)
    model = EvoNet()
    input_data = torch.from_numpy(skeleton_2d.astype(np.float32)).unsqueeze(0)
    prediction = model.predict(input_data)[0]
    ax3 = f.add_subplot(133, projection='3d')
    plot_3d_ax(prediction, ax3)
    plt.show()


def test(class_name=None, video_idx=0, frame_idx=1):
    if class_name is None:
        class_name = 'bench_dip'

    visualize(class_name, video_idx, frame_idx)


def run(class_name):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = EvoNet().to(device)
    model.eval()

    folder_root = '../dataset/skeletons_2d/{}'.format(class_name)

    target_root = folder_root.replace('skeletons_2d', 'skeletons_3d')

    if not os.path.exists('../dataset/skeletons_3d'):
        os.mkdir('../dataset/skeletons_3d')

    if not os.path.exists(target_root):
        os.mkdir(target_root)

    for video_path in tqdm.tqdm(sorted(glob.glob(folder_root+'/*'))):

        # load skeletons_2d
        target_path = video_path.replace('skeletons_2d', 'skeletons_3d')

        
        vid_skeletons = np.load(video_path)
        vid_skeletons_3d = []

        for frame in range(vid_skeletons.shape[0]):


            data = vid_skeletons[frame]
            input_data = torch.from_numpy(
                data.astype(np.float32)).unsqueeze(0)

            joints3d = model.predict(input_data)[0]
            vid_skeletons_3d.append(joints3d)
        
        vid_skeletons_3d = np.array(vid_skeletons_3d)
        np.save(target_path, vid_skeletons_3d)

def convert_all():
    for c in sorted(glob.glob('../dataset/skeletons_2d/*')):
        class_name = c.split('/')[-1]
        run(class_name)

def convert(action_name, video_idx):

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = EvoNet().to(device)
    model.eval()

    folder_root = '../dataset/skeletons_2d/{}'.format(action_name)
    target_root = folder_root.replace('skeletons_2d', 'skeletons_3d')

    if not os.path.exists('../dataset/skeletons_3d'):
        os.mkdir('../dataset/skeletons_3d')

    if not os.path.exists(target_root):
        os.mkdir(target_root)

    vid_skeletons = np.load('../dataset/skeletons_2d/{}/{}_{:03d}.npy'.format(action_name, action_name, video_idx))
    vid_skeletons_3d = []


    for frame in range(vid_skeletons.shape[0]):


        data = vid_skeletons[frame]
        input_data = torch.from_numpy(
            data.astype(np.float32)).unsqueeze(0)

        joints3d = model.predict(input_data)[0]
        vid_skeletons_3d.append(joints3d)
    
    vid_skeletons_3d = np.array(vid_skeletons_3d)
    np.save(target_root+'/{}_{:03d}.npy'.format(action_name, video_idx), vid_skeletons_3d)

if __name__ == '__main__':
    # test(class_name='abseiling')
    # convert_all()
    convert('air_hocky', 3)
    
