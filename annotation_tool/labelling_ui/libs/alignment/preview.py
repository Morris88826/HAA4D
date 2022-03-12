import numpy
import json
import matplotlib.pyplot as plt
import glob
import numpy as np
from .skeleton import Skeleton, normalize_skeleton

class_name = 'abseiling'
frame_idx = 1

target_3d_folder = './dataset/joints3d/{}'.format(class_name)

all_joints3d = []
for subfolder in sorted(glob.glob(target_3d_folder+'/*')):

    filename =  '{:04}.npy'.format(frame_idx)
    joints3d = np.load(subfolder+'/'+filename)
    all_joints3d.append(joints3d)
    
all_joints3d = np.array(all_joints3d)

target_2d_folder = target_3d_folder.replace('joints3d', 'joints2d')

all_joints2d = []
for subfolder in sorted(glob.glob(target_2d_folder+'/*')):
    filename =  '{:04}.json'.format(frame_idx)
    with open(subfolder+'/'+filename, 'rb') as jsonfile:
        data = json.load(jsonfile)

    joints2d = np.array(data).reshape((17, -1))
    all_joints2d.append(joints2d)

all_joints2d = np.array(all_joints2d)
equalized_all_joints2d = normalize_skeleton(all_joints2d)
equalized_all_joints3d = normalize_skeleton(all_joints3d)


num_videos = 20
fig = plt.figure(1, figsize=(20, 10), dpi=50)
fig.suptitle('frame {}'.format(frame_idx))
for i in range(num_videos):
    ax = fig.add_subplot(4,5,i+1)
    
    bones_indices = [
        [[0,4],[4,5],[5,6],[8,11],[11,12],[12,13]], # left -> pink
        [[0,1],[1,2],[2,3],[8,14],[14,15],[15,16]], # right -> blue
        [[0,7],[7,8],[8,9],[9,10]] # black
    ] # left-> pink, right->blue

    ax.set_xlim(-1,1)
    ax.set_ylim(1,-1)
    # ax.view_init(elev=180, azim=0)

    for _, bones in enumerate(bones_indices):
        for bone in (bones):
            start = bone[0]
            end = bone[1]

            x0, y0 = list(equalized_all_joints3d[i, start][[0,2]])
            x1, y1 = list(equalized_all_joints3d[i, end][[0,2]])
            ax.plot([x0, x1], [y0, y1])
    # draw dots
    sk = Skeleton()
    for j in range(17):
        if sk.dict_idx_2_joint[j] in (sk.body_parts['torso'] + sk.body_parts['head']):
            ax.scatter(equalized_all_joints3d[i, j, 0], equalized_all_joints3d[i, j, 2], c='b', s=1)
        elif sk.dict_idx_2_joint[j] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
            ax.scatter(equalized_all_joints3d[i, j, 0], equalized_all_joints3d[i, j, 2], c='r', s=1)
        elif sk.dict_idx_2_joint[j] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
            ax.scatter(equalized_all_joints3d[i, j, 0], equalized_all_joints3d[i, j, 2], c='g', s=1)
        else:
            raise NotImplementedError

plt.show()