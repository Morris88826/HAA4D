import torch
import torch.nn as nn
from .network import ConvBlock 
from libs.evoskeleton.load_model import EvoNet 
import numpy as np

class Joints3dNet(nn.Module):
    def __init__(self, temp_ckpt='./checkpoints/train1/epoch_19.pth', evoNet_root = './EvoSkeleton/examples'):
        super(Joints3dNet, self).__init__()
        temp_stat_dict = torch.load(temp_ckpt)
        self.temporalNet = TemporalConvNet(in_channels=51, out_channels=34)
        print('Loading Temporal Model ~')
        self.temporalNet.load_state_dict(temp_stat_dict['model'])
        self.evoNet = EvoNet(root = evoNet_root)
        self.evoNet.eval()
    
    def forward(self, x):
        intermediate = x = self.temporalNet(x)
        x = self.evoNet.normalize(x)
        x = self.evoNet(x)
        x = self.evoNet.afterprocessing(x)

        return intermediate, x
        



class TemporalConvNet(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(TemporalConvNet, self).__init__()
        hidden_features = 512
        
        self.upsample = nn.ConvTranspose2d(in_channels=in_channels, out_channels=hidden_features, kernel_size=1)
        self.layer1 = ConvBlock(in_channels=hidden_features, out_channels=hidden_features, hidden_features=hidden_features, dilation=1)
        self.layer2 = ConvBlock(in_channels=hidden_features, out_channels=hidden_features, hidden_features=hidden_features, dilation=3)
        self.downsample = nn.Conv2d(in_channels=hidden_features, out_channels=out_channels, kernel_size=1)

        self.init_weights()
        
    def forward(self, x):
        bs = x.shape[0]

        x = torch.transpose(x, dim0=2, dim1=1).unsqueeze(-1)        
        x = self.upsample(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.downsample(x)
        x = x.view(bs, -1, 2)

        return x

    def init_weights(self):
        self.upsample.weight.data.normal_(0, 0.01)
        for layer in self.layer1.layer:
            if isinstance(layer, nn.Conv2d):
                layer.weight.data.normal_(0, 0.01)
        for layer in self.layer2.layer:
            if isinstance(layer, nn.Conv2d):
                layer.weight.data.normal_(0, 0.01)
        self.downsample.weight.data.normal_(0, 0.01)

        return