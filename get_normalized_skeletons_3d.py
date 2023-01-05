import glob
import os
import json
import tqdm
import argparse
import numpy as np
from libs.skeleton import normalize_skeletons

def process(pose, read_root = './dataset/skeletons_3d', out_root="./dataset/processed_data"):

    normalized_skeletons_3d_root = out_root + '/normalized_skeletons_3d'
    if not os.path.exists(normalized_skeletons_3d_root):
        os.mkdir(normalized_skeletons_3d_root)

    pose_root = normalized_skeletons_3d_root + '/' + pose
    if not os.path.exists(pose_root):
        os.mkdir(pose_root)

    for v in tqdm.tqdm(glob.glob(read_root + '/' + pose + '/*')):
        filename = v.split('/')[-1]
        skeletons_3d = np.load(v)
        normalize_skeletons_3d = normalize_skeletons(skeletons_3d, type='haa4d')
        np.save("{}/{}".format(pose_root, filename), normalize_skeletons_3d)

    print('Done converting {} ~'.format(pose))

def process_all():
    for p in glob.glob('./dataset/skeletons_3d/*'):
        process(p.split('/')[-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pose', default="", help="name of the action(pose)")
    parser.add_argument('--process_all', action='store_true')
    args = parser.parse_args()

    if args.process_all:
        process_all()
    else:
        process(args.pose)
