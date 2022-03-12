import torch
import torch.nn as nn


class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels, hidden_features, dilation=1):
        super(ConvBlock, self).__init__()
        self.layer = nn.Sequential(*[
            nn.Conv2d(in_channels=in_channels, out_channels=hidden_features, kernel_size=(3,1), dilation=dilation),
            nn.BatchNorm2d(hidden_features),
            nn.ReLU(),
            nn.Conv2d(in_channels=hidden_features, out_channels=out_channels, kernel_size=1),
            nn.BatchNorm2d(hidden_features),
            nn.ReLU()
        ])

    def forward(self, x):
        out = self.layer(x)
        border = (x.shape[-2] - out.shape[-2])//2
        x = out + x[:, :, border:-border, :] 
        return x