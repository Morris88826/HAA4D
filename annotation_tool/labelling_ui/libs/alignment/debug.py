import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
import json



bones_indices = [
    [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
    [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
    [[0,7],[7,8],[8,9],[9,10]] # black
] # left-> pink, right->blue


class Skeleton():
    def __init__(self):
        
        # Skeleton Info
        self.num_joints = 17

        self.root_joint = 'lower_spine'
        self.body_parts = {
            'torso': ['lower_spine', 'mid_spine', 'upper_spine'],
            'left_leg': ['lower_spine', 'left_hip', 'left_knee', 'left_ankle'],
            'right_leg': ['lower_spine', 'right_hip', 'right_knee', 'right_ankle'],
            'left_arm': ['upper_spine', 'left_shoulder', 'left_elbow', 'left_hand'],
            'right_arm': ['upper_spine', 'right_shoulder', 'right_elbow', 'right_hand'],
            'head': ['upper_spine', 'neck', 'nose']
        }

        self.dict_joint_2_idx = {
            'lower_spine': 0,
            'right_hip': 1,
            'right_knee': 2,
            'right_ankle': 3,
            'left_hip': 4,
            'left_knee': 5,
            'left_ankle': 6,
            'mid_spine': 7,
            'upper_spine': 8,
            'neck': 9,
            'nose': 10,
            'left_shoulder': 11,
            'left_elbow': 12,
            'left_hand': 13,
            'right_shoulder': 14,
            'right_elbow': 15,
            'right_hand': 16
        }

        self.dict_idx_2_joint = {
            0: 'lower_spine',
            1: 'right_hip',
            2: 'right_knee',
            3: 'right_ankle',
            4: 'left_hip',
            5: 'left_knee',
            6: 'left_ankle',
            7: 'mid_spine',
            8: 'upper_spine',
            9: 'neck',
            10: 'nose',
            11: 'left_shoulder',
            12: 'left_elbow',
            13: 'left_hand',
            14: 'right_shoulder',
            15: 'right_elbow',
            16: 'right_hand'
        }

def plot_3d(joints3d):

    fig = plt.figure(0, figsize=(10, 10), dpi=50)
    ax = fig.add_subplot(111, projection="3d")

    elev=-80
    azim=-90
    max_range = 1000
    ax.set(xlim = [-max_range, max_range], ylim=[-max_range, max_range], zlim=[-max_range,max_range])

    for _, bones in enumerate(bones_indices):
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


def plot_2d(joints2d):
    fig, ax = plt.subplots()
    ax.set(xlim = [0, 1024], ylim=[720, 0])
    sk = Skeleton()

    for _, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0, = list(joints2d[start])
            x1, y1, = list(joints2d[end])
            ax.plot([x0, x1], [y0, y1])

    # draw dots
    for i in range(17):
        if sk.dict_idx_2_joint[i] in (sk.body_parts['torso'] + sk.body_parts['head']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='b')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='r')
        elif sk.dict_idx_2_joint[i] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
            ax.scatter(joints2d[i, 0], joints2d[i, 1], c='g')
        else:
            raise NotImplementedError

if __name__ == '__main__':

    class_name = 'burpee'
    video_idx = 0
    frame_idx = 1

    joints2d_path = './dataset/joints2d/{}/{}_{:03d}/{:04d}.json'.format(class_name, class_name, video_idx, frame_idx)
    
    with open(joints2d_path, 'rb') as jsonfile:
        data = json.load(jsonfile)
        joints2d = np.array(data).reshape((17,-1))

    joints3d_path = joints2d_path.replace('joints2d', 'joints3d').replace('json', 'npy')
    joints3d = np.load(joints3d_path)



    plot_2d(joints2d)
    plot_3d(joints3d)

    plt.show()