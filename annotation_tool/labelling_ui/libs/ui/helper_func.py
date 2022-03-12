import argparse
import os
import time
import numpy as np
import torch
from tqdm import tqdm
import glob
import json
import os
import matplotlib.pyplot as plt
from PIL import Image

def modify_joints(A):
    points = np.zeros([17,2])
    points[0] = (A[11] + A[12]) / 2
    points[1] = A[12]
    points[2] = A[14]
    points[3] = A[16]
    points[4] = A[11]
    points[5] = A[13]
    points[6] = A[15]
    points[7] = (A[5] + A[6] + A[11] + A[12] ) /4
    points[8] = (A[5] + A[6]) / 2
    points[9] = (A[5] + A[6] + A[0]) / 3
    points[10] = A[0]
    points[11] = A[5]
    points[12] = A[7]
    points[13] = A[9]
    points[14] = A[6]
    points[15] = A[8]
    points[16] = A[10]

    return points

def get_joints2d(data):
    joints2d = np.reshape(np.array(data['keypoints']), (-1, 3))[:,:2]
    joints2d = modify_joints(joints2d)
    return joints2d


