import glob
import os
import cv2
import json
import tqdm
import argparse


def vid2images(filename, out_path):
    vidcap = cv2.VideoCapture(filename)
    success, image = vidcap.read()
    count = 1
    while success:
        frame_name = f"{count:04d}.png"
        # save frame as JPEG file
        cv2.imwrite(out_path+'/'+frame_name, image)
        success, image = vidcap.read()
        count += 1

def process(pose, read_root = './dataset/video', out_root="./dataset"):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--pose', '-p')
    # args = parser.parse_args()

    raw_images_root = out_root + '/raw'
    if not os.path.exists(raw_images_root):
        os.mkdir(raw_images_root)

    pose_root = raw_images_root + '/' + pose
    if not os.path.exists(pose_root):
        os.mkdir(pose_root)

    for v in tqdm.tqdm(glob.glob(read_root + '/' + pose + '/*')):
        filename = v.split('/')[-1].split('.')[0]
        out_folder = pose_root + '/' + filename
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        vid2images(v, out_folder)

    print('Done converting {} ~'.format(pose))

def process_all():
    with open('./dataset/info.json', 'rb') as jsonfile:
        info = json.load(jsonfile)

    poses = info['primary_classes'] + info['additional_classes']
    
    for pose in poses:
        process(pose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pose', help="name of the pose")
    args = parser.parse_args()

    process(args.pose)
