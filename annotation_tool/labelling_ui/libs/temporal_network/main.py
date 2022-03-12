import torch
import numpy as np
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from libs.evoskeleton.load_model import EvoNet 
from libs.temporal_network.libs.model import TemporalConvNet
from libs.temporal_network.libs.util import rigid_transformation

class _TemporalData(Dataset):
    def __init__(self, joints2d_occ=None, data_package=None, time_frames=9):
        super(_TemporalData, self).__init__()

        if joints2d_occ is not None:
            self.full_data = False
            self.joints2d_occ = joints2d_occ
        elif data_package is not None:
            self.full_data = True
            self.joints2d_occ = data_package['2d_occ']
            self.joints2d_gt = data_package['2d_gt']
            self.joints3d_gt = data_package['3d']

        self.time_frames = time_frames
        self.length = self.joints2d_occ.shape[0]

    def __getitem__(self, idx):

        if self.full_data:
            joints2d_ori = np.copy(self.joints2d_occ[idx])
            joints2d_occ = np.expand_dims(self.joints2d_occ[idx], axis=0)
            joints2d_gt = self.joints2d_gt[idx]
            joints3d_gt = self.joints3d_gt[idx]

            joints2d_occ = np.repeat(joints2d_occ, self.time_frames, axis=0)
            
            for i, j in enumerate(range(-self.time_frames//2+1, self.time_frames//2 + 1)):
                if idx + j >= 0 and idx + j < self.length:
                    joints2d_occ[i] = self.joints2d_occ[idx+j]

            joints2d_occ = self.normalization(joints2d_occ)
            joints2d_gt = self.normalization(joints2d_gt)
            joints3d_gt = self.normalization(joints3d_gt)

            return joints2d_occ, joints2d_gt, joints3d_gt, joints2d_ori
        else:
            joints2d_ori = np.copy(self.joints2d_occ[idx])
            joints2d_occ = np.expand_dims(self.joints2d_occ[idx], axis=0)
            joints2d_occ = np.repeat(joints2d_occ, self.time_frames, axis=0)
            for i, j in enumerate(range(-self.time_frames//2+1, self.time_frames//2 + 1)):
                if idx + j >= 0 and idx + j < self.length:
                    joints2d_occ[i] = self.joints2d_occ[idx+j]
            joints2d_occ = self.normalization(joints2d_occ)
            return joints2d_occ, joints2d_ori

    def normalization(self, joints):
        if joints.ndim == 3:
            displacement = np.copy(joints[self.time_frames//2, 0, :2])
            joints[:, :, :2] -= displacement
            scaler = np.max(np.abs(joints[:, :, :2]))
            joints[:, :, :2] /= scaler
        else:
            displacement = np.copy(joints[0])
            joints -= displacement
            scaler = np.max(np.abs(joints))
            joints /= scaler

        return joints

    def __len__(self):
        return self.joints2d_occ.shape[0]

class TemporalModel():
    def __init__(self) -> None:
        # Using device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Load Model
        self.evoNet = EvoNet().to(self.device)
        self.evoNet.eval()

        self.temp_ckpt = './libs/temporal_network/checkpoints/train_2.pth'
        self.temporal_net = TemporalConvNet(in_channels=51, out_channels=34).to(self.device)
        self.temporal_net.load_state_dict(torch.load(self.temp_ckpt, map_location=self.device)['model'])
        self.temporal_net.eval()

    def process_input(self, images, batch_size=10):
        dataset = _TemporalData(images)
        return DataLoader(dataset, batch_size=batch_size)

    def forward(self, x, get_3d=True):

        intermediate = x = self.temporal_net(x)

        if get_3d:
            x = self.evoNet.predict(x)
            return intermediate, x
        else:
            return intermediate
    
    def afterprocessing(self, joints2d_ori, joints2d_occ, joints2d_pred):
        joints2d_pred_recover = np.zeros_like(joints2d_pred)
        for i in range(joints2d_occ.shape[0]):
            frame_non_occ = joints2d_occ[i, 4, :, 2]
            frame_non_occ = np.argwhere(frame_non_occ>0.999).flatten()
            translation, scale = rigid_transformation(joints2d_pred[i, frame_non_occ], joints2d_ori[i, frame_non_occ, :2])
            joints2d_pred_recover[i] = scale*joints2d_pred[i] + translation

        return joints2d_pred_recover 

    def predict(self, images, get_3d=True):
        assert images.shape == (images.shape[0], 17, 3)
        dataloader = self.process_input(images, batch_size=10)

        vid_2d_ori = None
        vid_2d_pred = None
        vid_2d_pred_recover = None

        if get_3d:
            vid_3d_pred = None

        for _, data in enumerate(dataloader):
            _joints2d_occ, _joints2d_ori = data
            bs, time_frames, _, _ = _joints2d_occ.shape
            joints2d_occ = Variable(_joints2d_occ).type(torch.float).to(self.device).view(bs, time_frames, -1)

            if get_3d:
                joints2d_pred, joints3d_pred = self.forward(joints2d_occ, get_3d)
            else:
                joints2d_pred = self.forward(joints2d_occ, get_3d)
            
            joints2d_ori = _joints2d_ori.detach().cpu().numpy()
            _joints2d_occ = _joints2d_occ.detach().cpu().numpy()
            joints2d_pred = joints2d_pred.detach().cpu().numpy()
            
            joints2d_pred_recover = self.afterprocessing(joints2d_ori, _joints2d_occ, joints2d_pred)
            
            if vid_2d_pred is None:
                vid_2d_ori = joints2d_ori
                vid_2d_pred = joints2d_pred
                vid_2d_pred_recover = joints2d_pred_recover
                if get_3d:
                    vid_3d_pred = joints3d_pred


            else:
                vid_2d_ori = np.concatenate([vid_2d_ori, joints2d_ori], axis=0)
                vid_2d_pred = np.concatenate([vid_2d_pred, joints2d_pred], axis=0)
                vid_2d_pred_recover = np.concatenate([vid_2d_pred_recover, joints2d_pred_recover], axis=0)

                if get_3d:
                    vid_3d_pred = np.concatenate([vid_3d_pred, joints3d_pred], axis=0)
            
        if get_3d:
            return vid_2d_ori, vid_2d_pred, vid_2d_pred_recover, vid_3d_pred
        else:
            return vid_2d_ori, vid_2d_pred, vid_2d_pred_recover
