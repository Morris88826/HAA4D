import libs.evoskeleton.model.model as libm
from libs.evoskeleton.dataset.h36m.data_utils import unNormalizeData

import torch
import numpy as np
import imageio
import matplotlib.pyplot as plt
import json
import torch.nn as nn

class EvoNet(nn.Module):
    def __init__(self, model_path='./libs/evoskeleton/examples/example_model.th', stats_path='./libs/evoskeleton/examples/stats.npy'):
        super(EvoNet, self).__init__()
        self.num_joints = 16

        # 16 out of 17 key-points are used as inputs in this examplar model
        self.re_order_indices= [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16]

        # paths   
        self.stats = np.load(stats_path, allow_pickle=True).item()
        self.model = self.initialize_model(torch.load(model_path))

        self.I   = np.array([1,2,3,1,7,8,1, 13,14,15,14,18,19,14,26,27])-1 # start points
        self.J   = np.array([2,3,4,7,8,9,13,14,15,16,18,19,20,26,27,28])-1 # end points
        self.LR  = np.array([1,1,1,0,0,0,0, 0, 0, 0, 0, 0, 0, 1, 1, 1], dtype=bool)

    def initialize_model(self, ckpt):
        # initialize the model
        cascade = libm.get_cascade()
        input_size = 32
        output_size = 48
        for stage_id in range(2):
            # initialize a single deep learner
            stage_model = libm.get_model(stage_id + 1,
                                        refine_3d=False,
                                        norm_twoD=False, 
                                        num_blocks=2,
                                        input_size=input_size,
                                        output_size=output_size,
                                        linear_size=1024,
                                        dropout=0.5,
                                        leaky=False)
            cascade.append(stage_model)
        cascade.load_state_dict(ckpt)
        cascade.eval()

        return cascade

    # def normalize(self, skeleton, re_order=None):
    #     norm_skel = skeleton.copy()
    #     if re_order is not None:
    #         norm_skel = norm_skel[re_order].reshape(32)
    #     norm_skel = norm_skel.reshape(16, 2)
    #     mean_x = np.mean(norm_skel[:,0])
    #     std_x = np.std(norm_skel[:,0])
    #     mean_y = np.mean(norm_skel[:,1])
    #     std_y = np.std(norm_skel[:,1])
    #     denominator = (0.5*(std_x + std_y))
    #     norm_skel[:,0] = (norm_skel[:,0] - mean_x)/denominator
    #     norm_skel[:,1] = (norm_skel[:,1] - mean_y)/denominator
    #     norm_skel = norm_skel.reshape(32)         
    #     return norm_skel

    def normalize(self, skeleton, re_order):
        norm_skel = skeleton
        bs = norm_skel.shape[0]
        norm_skel = norm_skel[:,re_order].reshape(bs, 32)

        norm_skel = norm_skel.reshape(bs, 16, 2)
        mean_x = torch.mean(norm_skel[:,:,0], dim=1).unsqueeze(1)
        std_x = torch.std(norm_skel[:,:,0], dim=1).unsqueeze(1)
        mean_y = torch.mean(norm_skel[:,:,1], dim=1).unsqueeze(1)
        std_y = torch.std(norm_skel[:,:,1], dim=1).unsqueeze(1)
        denominator = (0.5*(std_x + std_y))

        norm_skel[:,:,0] = (norm_skel[:,:,0] - mean_x)/denominator
        norm_skel[:,:,1] = (norm_skel[:,:,1] - mean_y)/denominator

        norm_skel = norm_skel.reshape(bs, 32)         
        return norm_skel


    def re_order(self, skeleton):
        bs = skeleton.shape[0]
        skeleton = skeleton.copy().reshape(bs, -1,3)

        return skeleton

    def afterprocessing(self, skeleton):
        # Make connection matrix

        bs = skeleton.shape[0]
        output = np.zeros((bs, self.num_joints+1, 3))
        for batch_idx in range(bs):
            for i in np.arange(len(self.I)):
                x, y, z = [np.array([skeleton[batch_idx, self.I[i], j], skeleton[batch_idx, self.J[i], j]] ) for j in range(3)]
                output[batch_idx, i+1] = np.array([x[-1],y[-1],z[-1]])

        return output
        
    def predict(self, skeleton_2d):
        
        input_data = self.normalize(skeleton_2d, self.re_order_indices).reshape(skeleton_2d.shape[0], -1)

        # forward pass to get prediction for the first stage
        num_stages = len(self.model)
        # for legacy code that does not have the num_blocks attribute
        for i in range(len(self.model)):
            self.model[i].num_blocks = len(self.model[i].res_blocks)
        prediction = self.model[0](input_data)
        # prediction for later stages
        for stage_idx in range(1, num_stages):
            prediction += self.model[stage_idx](input_data)

        pred = unNormalizeData(prediction.data.cpu().numpy(),
                            self.stats['mean_3d'],
                            self.stats['std_3d'],
                            self.stats['dim_ignore_3d']
                            )      

        pred = self.re_order(pred)

        output = self.afterprocessing(pred)

        return output


