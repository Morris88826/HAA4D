import numpy as np
from .joint import Joint2d, Joint3d

class Skeleton():
    def __init__(self, type='haa3d'):
        
        # Skeleton Info
        self.type = type
        if type == 'haa3d':
            self.num_joints = 17

            self.root_joint = 'lower_spine'
            self.body_parts = {
                'torso': ['lower_spine', 'mid_spine', 'upper_spine'],
                'left_leg': ['lower_spine', 'left_hip', 'left_knee', 'left_ankle'],
                'right_leg': ['lower_spine', 'right_hip', 'right_knee', 'right_ankle'],
                'left_arm': ['upper_spine', 'left_shoulder', 'left_elbow', 'left_hand'],
                'right_arm': ['upper_spine', 'right_shoulder', 'right_elbow', 'right_hand'],
                'head': ['upper_spine', 'neck', 'nose']
            }
            self.body_parts_color = {
                'torso': 'blue',
                'left_leg': 'pink',
                'right_leg': 'greenyellow',
                'left_arm': 'red',
                'right_arm': 'green',
                'head': 'aqua'
            }

            self.dict_joint_2_idx = {
                'lower_spine': 0,
                'right_hip': 1,
                'right_knee': 2,
                'right_ankle': 3,
                'left_hip': 4,
                'left_knee': 5,
                'left_ankle': 6,
                'mid_spine': 7,
                'upper_spine': 8,
                'neck': 9,
                'nose': 10,
                'left_shoulder': 11,
                'left_elbow': 12,
                'left_hand': 13,
                'right_shoulder': 14,
                'right_elbow': 15,
                'right_hand': 16
            }

            self.dict_idx_2_joint = {
                0: 'lower_spine',
                1: 'right_hip',
                2: 'right_knee',
                3: 'right_ankle',
                4: 'left_hip',
                5: 'left_knee',
                6: 'left_ankle',
                7: 'mid_spine',
                8: 'upper_spine',
                9: 'neck',
                10: 'nose',
                11: 'left_shoulder',
                12: 'left_elbow',
                13: 'left_hand',
                14: 'right_shoulder',
                15: 'right_elbow',
                16: 'right_hand'
            }

        elif type == 'ntu':
            self.num_joints = 25

            self.root_joint = 'lower_spine'
            self.body_parts = {
                'torso': ['lower_spine', 'mid_spine', 'upper_spine'],
                'left_leg': ['lower_spine', 'left_hip', 'left_knee', 'left_ankle', 'left_foot'],
                'right_leg': ['lower_spine', 'right_hip', 'right_knee', 'right_ankle', 'right_foot'],
                'left_arm': ['upper_spine', 'left_shoulder', 'left_elbow', 'left_wrist', 'left_hand', 'left_hand_tip'],
                'left_hand': ['left_hand', 'left_thumb'],
                'right_arm': ['upper_spine', 'right_shoulder', 'right_elbow', 'right_wrist', 'right_hand', 'right_hand_tip'],
                'right_hand': ['right_hand', 'right_thumb'],
                'head': ['upper_spine', 'neck', 'nose']
            }

            self.body_parts_color = {
                'torso': 'blue',
                'left_leg': 'pink',
                'right_leg': 'greenyellow',
                'left_arm': 'red',
                'left_hand': 'red',
                'right_arm': 'green',
                'right_hand': 'green',
                'head': 'aqua'
            }
            
            self.dict_joint_2_idx = {
                'lower_spine': 0,
                'mid_spine': 1,
                'neck': 2,
                'nose': 3,
                'left_shoulder': 4,
                'left_elbow': 5,
                'left_wrist': 6,
                'left_hand': 7,
                'right_shoulder': 8,
                'right_elbow': 9,
                'right_wrist': 10,
                'right_hand': 11,
                'left_hip': 12,
                'left_knee': 13,
                'left_ankle': 14,
                'left_foot': 15,            
                'right_hip': 16,
                'right_knee': 17,
                'right_ankle': 18,
                'right_foot': 19,
                'upper_spine': 20,
                'left_hand_tip': 21,
                'left_thumb': 22,
                'right_hand_tip': 23,
                'right_thumb': 24
            }

            self.dict_idx_2_joint = {
                0: 'lower_spine',
                1: 'mid_spine',
                2: 'neck',
                3: 'nose',
                4: 'left_shoulder',
                5: 'left_elbow',
                6: 'left_wrist',
                7: 'left_hand',
                8:'right_shoulder',
                9: 'right_elbow',
                10: 'right_wrist',
                11: 'right_hand',
                12: 'left_hip',
                13: 'left_knee',
                14: 'left_ankle',
                15: 'left_foot' ,          
                16: 'right_hip',
                17: 'right_knee',
                18: 'right_ankle',
                19: 'right_foot',
                20: 'upper_spine',
                21: 'left_hand_tip',
                22: 'left_thumb',
                23: 'right_hand_tip',
                24: 'right_thumb'
            }

    def get_bones_indices(self):
        bones = []
        for _, joints in zip(self.body_parts.keys(), self.body_parts.values()):
            for i in range(1, len(joints)):
                start = self.dict_joint_2_idx[joints[i-1]]
                end = self.dict_joint_2_idx[joints[i]]
                bones.append([start, end])
        return np.array(bones)

class Skeleton2d(Skeleton):
    def __init__(self, joints, type, is_cartesian=True):
        super(Skeleton2d, self).__init__(type=type)
        self._build_skeleton(joints, is_cartesian)
        self.joints = joints

    def _build_skeleton(self, joints, is_cartesian):

        if is_cartesian:
            setattr(self, self.root_joint, Joint2d(self.root_joint, cartesian_coord=joints[self.dict_joint_2_idx[self.root_joint]]))
            getattr(self, self.root_joint).set_polar_coord()
            for body_part in self.body_parts.keys():
                for i, joint_name in enumerate(self.body_parts[body_part]):
                    if i == 0:
                        continue
                    else:
                        joint = Joint2d(joint_name, cartesian_coord=joints[self.dict_joint_2_idx[joint_name]])
                        joint.set_parent(getattr(self, self.body_parts[body_part][i-1]))
                        joint.set_polar_coord()
                        setattr(self, joint_name, joint)
        else:
            setattr(self, self.root_joint, Joint2d(self.root_joint, polar_coord=joints[self.dict_joint_2_idx[self.root_joint]]))
            getattr(self, self.root_joint).set_cartesian_coord()
            for body_part in self.body_parts.keys():
                for i, joint_name in enumerate(self.body_parts[body_part]):
                    if i == 0:
                        continue
                    else:
                        joint = Joint2d(joint_name, polar_coord=joints[self.dict_joint_2_idx[joint_name]])
                        joint.set_parent(getattr(self, self.body_parts[body_part][i-1]))
                        joint.set_cartesian_coord()
                        setattr(self, joint_name, joint)

    def get_cartesian_joints(self):
        cartesian_joints = np.zeros((self.num_joints, 2))
        for i in range(self.num_joints):
            cartesian_joints[i] = getattr(self, self.dict_idx_2_joint[i]).cartesian_coord

        return cartesian_joints

    def get_polar_joints(self):
        polar_joints = np.zeros((self.num_joints, 2))
        for i in range(self.num_joints):
            polar_joints[i] = getattr(self, self.dict_idx_2_joint[i]).polar_coord

        return polar_joints


class Skeleton3d(Skeleton):
    def __init__(self, joints, type, is_cartesian=True):
        super(Skeleton3d, self).__init__(type=type)
        self._build_skeleton(joints, is_cartesian)
        self.joints = joints


    def _build_skeleton(self, joints, is_cartesian):
        if is_cartesian:
            setattr(self, self.root_joint, Joint3d(self.root_joint, cartesian_coord=joints[self.dict_joint_2_idx[self.root_joint]]))
            getattr(self, self.root_joint).set_spherical_coord()
            for body_part in self.body_parts.keys():
                for i, joint_name in enumerate(self.body_parts[body_part]):
                    if i == 0:
                        continue
                    else:
                        joint = Joint3d(joint_name, cartesian_coord=joints[self.dict_joint_2_idx[joint_name]])
                        joint.set_parent(getattr(self, self.body_parts[body_part][i-1]))
                        joint.set_spherical_coord()
                        setattr(self, joint_name, joint)

        else:
            setattr(self, self.root_joint, Joint3d(self.root_joint, spherical_coord=joints[self.dict_joint_2_idx[self.root_joint]]))
            getattr(self, self.root_joint).set_cartesian_coord()
            for body_part in self.body_parts.keys():
                for i, joint_name in enumerate(self.body_parts[body_part]):
                    if i == 0:
                        continue
                    else:
                        joint = Joint3d(joint_name, spherical_coord=joints[self.dict_joint_2_idx[joint_name]])
                        joint.set_parent(getattr(self, self.body_parts[body_part][i-1]))
                        joint.set_cartesian_coord()
                        setattr(self, joint_name, joint)

    def get_cartesian_joints(self):
        cartesian_joints = np.zeros((self.num_joints, 3))
        for i in range(self.num_joints):
            cartesian_joints[i] = getattr(self, self.dict_idx_2_joint[i]).cartesian_coord

        return cartesian_joints

    def get_spherical_joints(self):
        spherical_joints = np.zeros((self.num_joints, 3))
        for i in range(self.num_joints):
            spherical_joints[i] = getattr(self, self.dict_idx_2_joint[i]).spherical_coord

        return spherical_joints

def normalize_skeleton(skeleton, type):
    skeleton = skeleton - np.repeat(np.expand_dims(skeleton[0],0), skeleton.shape[0], axis=0)
    is_3d = True if skeleton.shape[-1]==3 else False
    
    if not is_3d:
        sk = Skeleton2d(skeleton, type)
        skeleton_length = np.linalg.norm(sk.get_polar_joints()[:, 0])
        normalized_polar = sk.get_polar_joints()
        normalized_polar[:, 0] = normalized_polar[:, 0]/skeleton_length
        new_skeleton = Skeleton2d(normalized_polar, type, is_cartesian=False).get_cartesian_joints()
    else:
        sk = Skeleton3d(skeleton, type)
        skeleton_length = np.linalg.norm(sk.get_spherical_joints()[:, 0])
        normalized_spher = sk.get_spherical_joints()
        normalized_spher[:, 0] = normalized_spher[:, 0]/skeleton_length
        new_skeleton = Skeleton3d(normalized_spher, type, is_cartesian=False).get_cartesian_joints()
    return new_skeleton

def normalize_skeletons(all_skeletons, type='haa3d'):
    if all_skeletons.shape[-1] == 3:
        normalized_all_skeletons = np.copy(all_skeletons)
        num_joints = normalized_all_skeletons.shape[1]
        average_bone_length = np.zeros(num_joints)
        for i in range(normalized_all_skeletons.shape[0]):
            normalized_all_skeletons[i] = normalize_skeleton(all_skeletons[i], type)
            skeleton = Skeleton3d(normalized_all_skeletons[i], type)
            average_bone_length += skeleton.get_spherical_joints()[:,0]/normalized_all_skeletons.shape[0]
        scaler = np.ones(num_joints)

        for i in range(normalized_all_skeletons.shape[0]):
            skeleton = Skeleton3d(normalized_all_skeletons[i], type)
            spherical_joints = skeleton.get_spherical_joints()
            scaler = (1/spherical_joints[1:,0])*average_bone_length[1:]
            spherical_joints[1:, 0] = (scaler)*spherical_joints[1:, 0]
            normalized_all_skeletons[i]=Skeleton3d(spherical_joints, type, is_cartesian=False).get_cartesian_joints()
        

        return normalized_all_skeletons

    elif all_skeletons.shape[-1] == 2:
        
        normalized_all_skeletons = np.copy(all_skeletons)

        for i in range(normalized_all_skeletons.shape[0]):
            displacement = np.zeros_like(all_skeletons[i,0]) - all_skeletons[i,0]
            normalized_all_skeletons[i] = all_skeletons[i] + displacement

        return normalized_all_skeletons



