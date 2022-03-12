import math
import numpy as np
import glob
import json

    

def find_distance(points1, points2):
    n = points1.shape[0]
    m = points2.shape[0]

    output2, output1 = np.meshgrid(np.arange(m), np.arange(n))
    first = points1[output1, :]
    second = points2[output2, :]

    dists = (np.linalg.norm(np.subtract(first, second), axis=2))

    return dists


def get_golden_circle():

    golden_ratio = (1+math.sqrt(5))/2

    a = math.sqrt(golden_ratio)/math.pow(5, 1/4)
    b = 1/(math.sqrt(golden_ratio)*math.pow(5, 1/4))

    vertices = []
    vertices.append([0, a, b])
    vertices.append([0, a, -b])
    vertices.append([0, -a, b])
    vertices.append([0, -a, -b])
    vertices.append([b, 0, a])
    vertices.append([b, 0, -a])
    vertices.append([-b, 0, a])
    vertices.append([-b, 0, -a])
    vertices.append([a, b, 0])
    vertices.append([a, -b, 0])
    vertices.append([-a, b, 0])
    vertices.append([-a, -b, 0])

    vertices = np.array(vertices)
    
    distance = find_distance(vertices, vertices)
    adjacency_matrix = np.where(distance==2*b, 1, 0)
    
    return vertices, adjacency_matrix

def cartesian_to_spherical(cartesian_point):
    dx, dy, dz = list(cartesian_point)
    r = math.sqrt(dx*dx + dy*dy + dz*dz)
    theta = math.atan2(math.sqrt(dx*dx + dy*dy), dz)
    phi = math.atan2(dy, dx)

    return r, theta, phi

def spherical_to_cartesian(spherical_pos):
    r, theta, phi = list(spherical_pos)


    x = r*math.sin(theta)*math.cos(phi)
    y = r*math.sin(theta)*math.sin(phi)
    z = r*math.cos(theta)

    return x, y, z

def rel_error(x,y):
    return np.max(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))


def load_skeletons(class_name, frame_idx=None):

    target_3d_folder = './dataset/joints3d/{}'.format(class_name)

    all_skeletons_2d = []
    all_skeletons_3d = []

    if frame_idx is None:
        for subfolder in sorted(glob.glob(target_3d_folder+'/*')):
            temporal_skeleton_2d = []
            temporal_skeleton_3d = []
            for file in sorted(glob.glob(subfolder+'/*.npy')):
                skeleton_3d = np.load(file)
                temporal_skeleton_3d.append(skeleton_3d)

                skeleton_2d_path = file.replace('joints3d', 'joints2d').replace('.npy', '.json')
                with open(skeleton_2d_path, 'rb') as jsonfile:
                    skeleton_2d = np.array(json.load(jsonfile)).reshape((-1, 2))
                temporal_skeleton_2d.append(skeleton_2d)

            temporal_skeleton_2d = np.array(temporal_skeleton_2d)
            temporal_skeleton_3d = np.array(temporal_skeleton_3d)


            all_skeletons_2d.append(temporal_skeleton_2d)
            all_skeletons_3d.append(temporal_skeleton_3d)
    
    else:
        for subfolder in sorted(glob.glob(target_3d_folder+'/*')):
            skeleton_3d = np.load(subfolder+'/{:04d}.npy'.format(frame_idx))
            skeleton_2d_path = subfolder.replace('joints3d', 'joints2d')
            with open(skeleton_2d_path+'/{:04d}.json'.format(frame_idx), 'rb') as jsonfile:
                skeleton_2d = np.array(json.load(jsonfile)).reshape((-1, 2))
            
            all_skeletons_2d.append(skeleton_2d)
            all_skeletons_3d.append(skeleton_3d) 

        all_skeletons_2d = np.array(all_skeletons_2d)
        all_skeletons_3d = np.array(all_skeletons_3d)
    return all_skeletons_2d, all_skeletons_3d
    

if __name__ == '__main__':
    all_skeletons_2d, all_skeletons_3d = load_skeletons('burpee')