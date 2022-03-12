import numpy as np
from .util import cartesian_to_spherical, spherical_to_cartesian, cartesian_to_polar, polar_to_cartesian

class Joint():
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.idx = -1

        self.cartesian_coord = None

    def set_parent(self, parent):
        self.parent = parent
        self.parent.add_child(self)
    
    def add_child(self, child):
        self.children.append(child)
    
class Joint2d(Joint):
    def __init__(self, name, cartesian_coord=None, polar_coord=None):
        super(Joint2d, self).__init__(name)

        if cartesian_coord is not None:
            self.cartesian_coord = cartesian_coord

        elif polar_coord is not None:
            self.polar_coord = polar_coord
    
    def set_polar_coord(self):
        if self.parent is None:
            self.polar_coord = np.zeros(2)
        else:
            self.polar_coord = cartesian_to_polar(self.parent.cartesian_coord, self.cartesian_coord)

    def set_cartesian_coord(self):
        if self.parent is None:
            self.cartesian_coord = np.zeros(2)
        else: 
            self.cartesian_coord = polar_to_cartesian(self.parent.cartesian_coord, self.polar_coord)
            


class Joint3d(Joint):
    def __init__(self, name, cartesian_coord=None, spherical_coord=None):
        super(Joint3d, self).__init__(name)

        if cartesian_coord is not None:
            self.cartesian_coord = cartesian_coord

        elif spherical_coord is not None:
            self.spherical_coord = spherical_coord
    
    def set_spherical_coord(self):
        if self.parent is None:
            self.spherical_coord = np.zeros(3)
        else:
            self.spherical_coord = cartesian_to_spherical(self.parent.cartesian_coord, self.cartesian_coord)
    def set_cartesian_coord(self):
        if self.parent is None:
            self.cartesian_coord = np.zeros(3)
        else: 
            self.cartesian_coord = spherical_to_cartesian(self.parent.cartesian_coord, self.spherical_coord)
            