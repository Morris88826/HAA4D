joints_key_2_index = {
    'lower_spine':0, 
    'right_hip':1, 
    'right_knee': 2, 
    'right_foot':3, 
    'left_hip':4, 
    'left_knee': 5, 
    'left_foot':6, 
    'mid_spine':7, 
    'upper_spine':8,
    'neck':9, 
    'head':10, 
    'left_shoulder':11, 
    'left_elbow':12, 
    'left_hand':13, 
    'right_shoulder':14, 
    'right_elbow':15, 
    'right_hand':16
}

joints_index_2_key = {
    0:'lower_spine', 
    1:'right_hip', 
    2:'right_knee', 
    3:'right_foot', 
    4:'left_hip', 
    5:'left_knee', 
    6:'left_foot', 
    7:'mid_spine', 
    8:'upper_spine',
    9:'neck', 
    10:'head', 
    11:'left_shoulder', 
    12:'left_elbow', 
    13:'left_hand', 
    14:'right_shoulder', 
    15:'right_elbow', 
    16:'right_hand'
}

reference_joint = 'upper_spine'

class Joint2d():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.parent = None
        self.children = []
        self.num_children = len(self.children)

    def add_parent(self, parent):
        self.parent = parent
        
    def add_child(self, child):
        self.children.append(child)
        self.num_children = len(self.children)
        child.add_parent(self)
    

class Skeleton2d():
    def __init__(self, list_joints=None):
        self.parent_dict = {
            'upper_spine': None,
            'mid_spine': 'upper_spine',
            'lower_spine': 'mid_spine',
            'neck': 'upper_spine',
            'head': 'neck',
            'left_shoulder': 'upper_spine',
            'left_elbow': 'left_shoulder',
            'left_hand': 'left_elbow',
            'right_shoulder': 'upper_spine',
            'right_elbow': 'right_shoulder',
            'right_hand': 'right_elbow',
            'left_hip': 'lower_spine',
            'left_knee': 'left_hip',
            'left_foot': 'left_knee',
            'right_hip': 'lower_spine',
            'right_knee': 'right_hip',
            'right_foot': 'right_knee'
        }

        self.num_joints = 0

        if list_joints is not None:
            for joint in list_joints:
                self.add_joint(joint)

    
    def add_joint(self, joint:Joint2d):
        if getattr(self, joint.name, None) is None:
            self.num_joints += 1
            setattr(self, joint.name, joint)

            current_joint = getattr(self, joint.name)

            for key, value in zip(self.parent_dict.keys(), self.parent_dict.values()):
                if (value == joint.name) and (getattr(self, key, None) is not None):
                    joint.add_child(getattr(self, key))

            if self.parent_dict[current_joint.name] is not None:
                parent_joint = getattr(self, self.parent_dict[current_joint.name], None)
            else:
                parent_joint = None

            if parent_joint is not None:
                parent_joint.add_child(current_joint)
        else:
            current_joint = getattr(self, joint.name)
            current_joint.position = joint.position
        
    def get_joints(self):
        joints = []
        for key in self.parent_dict.keys():
            joint = getattr(self, key, None)
            if joint is not None:
                joints.append(joint)
        
        return joints
        

