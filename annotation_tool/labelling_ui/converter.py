import os
import numpy as np
import json
import glob
import tqdm

# change old skeletons_2d format to new ones (json to np)

def convert(action_name):
    skeletons_2d_root = '../dataset/old_skeletons_2d'
    out_root = '../dataset/skeletons_2d'

    for vid_path in sorted(glob.glob(skeletons_2d_root+'/{}/*'.format(action_name))):
        video_frames = []
        for frame_path in sorted(glob.glob(vid_path+'/*')):
            with open(frame_path, 'rb') as jsonfile:
                frame = np.array(json.load(jsonfile)).reshape((-1,2))
            video_frames.append(frame)
        
        video_frames = np.array(video_frames)
        
        if not os.path.exists(out_root+'/{}'.format(action_name)):
            os.mkdir(out_root+'/{}'.format(action_name))
        np.save(out_root+'/{}/{}.npy'.format(action_name, vid_path.split('/')[-1]), video_frames)

def convert_all():
    skeletons_2d_root = '../dataset/skeletons_2d'
    for action_path in tqdm.tqdm(sorted(glob.glob(skeletons_2d_root+'/*'))):
        action_name = action_path.split('/')[-1]
        convert(action_name)

def correct_wrong_3d(action_name, video_idx):
    out_path = '../dataset/skeletons_3d/{}/{}_{:03d}.npy'.format(action_name, action_name, video_idx)
    
    video_skeletons = np.load(out_path)

    video_skeletons[:, :, 2] = -1*video_skeletons[:, :, 2]
    # video_skeletons[:,  [1, 2, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16], :] = video_skeletons[:,  [4, 5, 6, 1, 2, 3, 14, 15, 16, 11, 12, 13], :]
    np.save(out_path, video_skeletons)

def correct_wrong_labelling(action_name, video_idx):

    out_path = '../dataset/skeletons_2d/{}/{}_{:03d}.npy'.format(action_name, action_name, video_idx)
    
    video_skeletons = np.load(out_path)

    video_skeletons[:, [11, 12, 13, 14, 15, 16], :] = video_skeletons[:, [14, 15, 16, 11, 12, 13], :]
    np.save(out_path, video_skeletons)

if __name__ == '__main__':
    # convert_all()
    # convert('basketball_jabstep')
    # correct_wrong_labelling('air_hocky', 3)

    # correct_wrong_3d('air_guitar', 4)
    pass