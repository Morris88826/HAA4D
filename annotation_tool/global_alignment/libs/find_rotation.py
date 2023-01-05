import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable

class AngleModel(nn.Module):
    def __init__(self):
        super(AngleModel, self).__init__()
        self.r = nn.Parameter(torch.tensor(0.0))
        self.theta = nn.Parameter(torch.tensor(0.0))
        self.phi = nn.Parameter(torch.tensor(0.0))

    def forward(self, input):
        
        Rx = torch.zeros((3, 3)).type(input.dtype)
        Ry = torch.zeros_like(Rx)
        Rz = torch.zeros_like(Rx)  

        Rx[0, 0] = 1
        Rx[1, 1] = torch.cos(self.r)
        Rx[1, 2] = -1*torch.sin(self.r)
        Rx[2, 1] = torch.sin(self.r)
        Rx[2, 2] = torch.cos(self.r)

        Ry[1, 1] = 1
        Ry[0, 0] = torch.cos(self.theta)
        Ry[0, 2] = torch.sin(self.theta)
        Ry[2, 0] = -1*torch.sin(self.theta)
        Ry[2, 2] = torch.cos(self.theta)


        Rz[2, 2] = 1
        Rz[0, 0] = torch.cos(self.phi)
        Rz[0, 1] = -1*torch.sin(self.phi)
        Rz[1, 0] = torch.sin(self.phi)
        Rz[1, 1] = torch.cos(self.phi)

        output = torch.matmul(Rz, torch.matmul(Ry, torch.matmul(Rx, input)))
        output = output.permute(1, 0)

        R = torch.matmul(Rz, torch.matmul(Ry, Rx))

        return output, R

def get_rotation_matrix_3d(points_3d, target_points_3d):

    points_3d = np.copy(points_3d.T)

    model = AngleModel()
    optimizer = torch.optim.Adam(model.parameters(), 5e-2)
    loss_func = nn.L1Loss()

    ## Train
    for _ in range(1000):
        optimizer.zero_grad()

        t_points_3d = Variable(torch.tensor(points_3d).type(torch.float))
        t_target_points_3d = Variable(torch.tensor(target_points_3d).type(torch.float))

        output, R = model.forward(t_points_3d)

        loss = loss_func(output, t_target_points_3d)
        loss.backward()

        optimizer.step()

    
    output = output.detach().cpu().numpy()
    R = R.detach().cpu().numpy()
    return output, R  
