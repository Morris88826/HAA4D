import tkinter as tk
import os
from tkinter.constants import LEFT, NO
from PIL import ImageTk, Image
import os
import json
import numpy as np
from copy import deepcopy
from scipy.ndimage import gaussian_filter1d
from .helper_func import modify_joints
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from libs.evoskeleton.load_model import EvoNet
import torch
from .temp_page import Temporal_window
from .modify_display import Modify_display_window
from libs.skeleton.skeleton import Skeleton


class Page2(tk.Frame):
    def __init__(self, root, controller, parent=None):
        tk.Frame.__init__(self, root)

        self.root = root
        self.controller = controller
        self.parent = parent

        self.raw_images_root = '../../dataset/raw'
        self.w_height = self.controller.winfo_screenheight()
        self.w_width = self.controller.winfo_screenwidth()

        # Page 2 interface
        self.ratio = 3/4
        self.left_frame = tk.Frame(
            self, width=self.w_width*self.ratio, height=self.w_height*self.ratio)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(
            self, width=self.w_width*(1-self.ratio), height=700)
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="both", expand=False)

        self.label = tk.Label(self.right_frame, text="")
        self.label.pack(side="top")

        self.current_joint_label = tk.Label(self.right_frame, text="")
        self.current_joint_label.pack(fill="both", padx=5, pady=5)

        self.frame1 = tk.Frame(self.right_frame)
        self.frame1.pack(fill="both", padx=5, pady=5)
        load_alphapose_button = tk.Button(
            self.frame1, text="Load from alphapose", command=self.load_from_alphapose)
        load_alphapose_button.grid(row=0, column=0)
        load_joints2d_button = tk.Button(
            self.frame1, text="Load from joints2d", command=self.load_from_joints2d)
        load_joints2d_button.grid(row=0, column=1)

        reset_button = tk.Button(
            self.frame1, text="Reset Zoom", command=self.reset_zoom)
        reset_button.grid(row=1, column=0)
        modify_display_button = tk.Button(
            self.frame1, text="Modify Display", command=self.modify_displaying)
        modify_display_button.grid(row=1, column=1)

        label_everything_button = tk.Button(
            self.frame1, text="Label Everything (L)", command=self.label_everything)
        label_everything_button.grid(row=2, column=0)

        temporal_prediction_button = tk.Button(
            self.frame1, text="Temporal Prediction", command=self.temporal_predicting)
        temporal_prediction_button.grid(row=2, column=1)

        # all_shown_button = tk.Button(self.frame1, text="Mark all unoccluded", command=self.shown_all)
        # all_shown_button.grid(row=2, column=1)

        self.switch_frame = tk.Frame(self.right_frame)
        self.switch_frame.pack(fill="both", padx=5, pady=5)

        self.switch_variable = tk.StringVar(value="off")
        off_button = tk.Radiobutton(self.switch_frame, text="Off", variable=self.switch_variable,
                                    indicatoron=False, value="off", width=8, command=self.make_all_occ_or_unocc)
        o_button = tk.Radiobutton(self.switch_frame, text="All Occluded", variable=self.switch_variable,
                                  indicatoron=False, value="occluded", command=self.make_all_occ_or_unocc)
        uo_button = tk.Radiobutton(self.switch_frame, text="All Unoccluded", variable=self.switch_variable,
                                   indicatoron=False, value="unoccluded", command=self.make_all_occ_or_unocc)
        off_button.pack(side="left")
        o_button.pack(side="left")
        uo_button.pack(side="left")

        info_label = tk.Label(
            self.right_frame, text="To label one joint: (4,5), (q-u), (a-j),(v)", font=("Helvetica", 8))
        info_label.pack(fill="both")
        info_label2 = tk.Label(
            self.right_frame, text="Press (1) to change a joint to hidden. Press (2) to delete joint.", font=("Helvetica", 8))
        info_label2.pack(fill="both")

        self.instruction = tk.Canvas(self.right_frame, width=self.w_width*(
            1-self.ratio)*(3/5), height=self.w_width*(1-self.ratio)*(3/5))
        self.instruction.pack(side="top")
        img = Image.open("./libs/ui/instruction.jpg")
        img = img.resize((int(self.w_width*(1-self.ratio)*(3/5)),
                         int(self.w_width*(1-self.ratio)*(3/5))))
        self.inst_img = ImageTk.PhotoImage(img)
        self.instruction.create_image(0, 0, image=self.inst_img, anchor="nw")
        self.instruction_position = {
            0: [87/192, 98/192],
            1: [78/192, 107/192],
            2: [73/192, 144/192],
            3: [72/192, 179/192],
            4: [101/192, 107/192],
            5: [106/192, 144/192],
            6: [107/192, 179/192],
            7: [87/192, 77/192],
            8: [87/192, 54/192],
            9: [87/192, 41/192],
            10: [87/192, 23/192],
            11: [111/192, 50/192],
            12: [120/192, 76/192],
            13: [123/192, 109/192],
            14: [68/192, 50/192],
            15: [59/192, 76/192],
            16: [56/192, 109/192]
        }

        self.instruction_size = self.w_width*(1-self.ratio)*(3/5)

        auto_interpolate_button = tk.Button(
            self.right_frame, text="Auto interpolate", command=self.auto_interpolate)
        auto_interpolate_button.pack(fill="both", padx=5, pady=5)

        smoothing_button = tk.Button(
            self.right_frame, text="Motion Smoothing", command=self.gaussian_smoothing)
        smoothing_button.pack(fill="both", padx=5, pady=5)

        # Load Model
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.evoNet = EvoNet().to(self.device)
        self.evoNet.eval()

        self.show_3d = False
        display3d_button = tk.Button(
            self.right_frame, text="Show/close 3D display", command=self.toggle_3d_display)
        display3d_button.pack(fill="both")
        self.plot_3d = Figure(figsize=(4, 4), dpi=50)
        self.display_3d = FigureCanvasTkAgg(
            self.plot_3d, master=self.right_frame)
        self.display_3d.get_tk_widget().pack(side="top")

        save_exit_button = tk.Button(
            self.right_frame, text="Save and Exit", command=self.save_and_exit)
        save_exit_button.pack(fill="both", padx=5, pady=5, side="bottom")

        exit_button = tk.Button(
            self.right_frame, text="Exit without Saving", command=self.exit)
        exit_button.pack(fill="both", padx=5, pady=5, side="bottom")

        save_button = tk.Button(
            self.right_frame, text="Save", command=self.save)
        save_button.pack(fill="both", padx=5, pady=5, side="bottom")

        self.alert_label = tk.Label(
            self.right_frame, text="", fg="red", font=("Helvetica", 8))
        self.alert_label.pack(fill="both", padx=5, pady=5)

        self.canvas = tk.Canvas(
            self.left_frame, width=self.w_width*self.ratio, height=self.w_height*self.ratio)
        self.canvas.pack(side="top", padx=10, pady=10,
                         anchor="nw", fill="both", expand=True)

        lb_frame = tk.Frame(self.left_frame, width=self.w_width *
                            self.ratio, height=self.w_height*(1-self.ratio))
        lb_frame.pack(side="top", fill="x", anchor="nw",
                      expand=False, padx=20, pady=20)

        self.scale = tk.Scale(lb_frame, from_=0, to=1,
                              orient=tk.HORIZONTAL, command=self.changed_frame)
        self.scale.pack(side="top", fill="both")

        # Page 2 information
        self.num_joints = 17
        self.current_frame = 1
        self.current_joint = -1
        self.video_length = -1
        self.image_corner = [self.w_width*self.ratio *
                             (0.1), self.w_height*self.ratio*(0.1)]
        self.zoom = -4
        self.position = [-1, -1]
        self.joint_circle_size = 2
        self.bone_width = 3
        self.label_everything_mode = False
        self.joint2d_init()
        self.user_selected = {}

        self.bones_indices = [
            [[0, 4], [4, 5], [5, 6], [8, 11], [11, 12], [12, 13]],  # left -> pink
            [[0, 1], [1, 2], [2, 3], [8, 14], [14, 15], [15, 16]],  # right -> blue
            [[0, 7], [7, 8], [8, 9], [9, 10]]  # black
        ]  # left-> pink, right->blue
        self.bone_colors = ['pink', 'blue', 'gray']
        self.joints_index_2_key = Skeleton().dict_idx_2_joint

        self.key_bind_table = ['v', 'g', 'h', 'j', 'd', 's',
                               'a', 'f', 'r', '4', '5', 'e', 'w', 'q', 't', 'y', 'u']
        self.label_everything_mode = False

    def initialize(self):
        self.key_binding()
        self.path = self.raw_images_root + \
            '/{}/{}'.format(self.parent.current_video[0],
                            self.parent.current_video[1])
        self.video_length = len(os.listdir(self.path))
        self.current_frame = 1
        self.current_joint = -1
        self.image_corner = [self.w_width*self.ratio *
                             (0.1), self.w_height*self.ratio*(0.1)]
        self.zoom = -4
        self.position = [-1, -1]
        self.joint_circle_size = 2
        self.show_3d = False
        self.show_3d_skeleton()
        self.switch_variable.set('off')

        self.canvas.delete("oval")
        self.canvas.delete("bone")
        self.label.config(text="Current frame: {}".format(self.current_frame))
        self.current_joint_label.config(text="Current joint: None")
        self.scale.configure(from_=1, to=self.video_length)
        self.scale.set(1)
        self.joint2d_init()

        self.user_selected = {}
        for i in range(self.num_joints):
            self.user_selected[i] = {}

    def key_binding(self):
        self.canvas.bind("<Button-1>", self.event_handler)
        self.canvas.bind("<B1-Motion>", self.event_handler)
        self.canvas.bind("<ButtonRelease-1>", self.event_handler)
        self.canvas.bind("<MouseWheel>", self.event_handler)

        self.controller.bind('z', self.event_handler)
        self.controller.bind('x', self.event_handler)
        self.controller.bind('1', self.event_handler)
        self.controller.bind('2', self.event_handler)
        self.controller.bind('3', self.event_handler)
        self.controller.bind('0', self.event_handler)
        self.controller.bind('l', self.event_handler)
        self.controller.bind('`', self.event_handler)
        self.controller.bind('o', self.event_handler)
        self.controller.bind('p', self.event_handler)
        for key in self.key_bind_table:
            self.controller.bind(key, self.event_handler)

    def key_unbinding(self):
        self.controller.unbind('z')
        self.controller.unbind('x')
        self.controller.unbind('1')
        self.controller.unbind('2')
        self.controller.unbind('3')
        self.controller.unbind('0')
        self.controller.unbind('l')
        self.controller.unbind('`')
        self.controller.unbind('o')
        self.controller.unbind('p')

        for key in self.key_bind_table:
            self.controller.unbind(key)

    def run_from_alphapose(self):
        print('Run alphapose')

    def load_from_alphapose(self):
        path = self.path.replace('raw', 'alphapose')
        file_path = path+'.json'
        if not os.path.exists(file_path):
            self.run_from_alphapose()
            return

        with open(file_path, 'rb') as jsonfile:
            data = json.load(jsonfile)

        _temp = {}
        scores = {}
        for d in data:
            frame_id = int(d['image_id'].split('.')[0])
            keypoints = np.array(d['keypoints']).reshape((self.num_joints, 3))
            keypoints[:, -1] = 1
            keypoints[:, :2] = modify_joints(keypoints[:, :2])

            score = d['score']

            if frame_id in scores.keys():
                if scores[frame_id] < score:
                    scores[frame_id] = score
                    _temp[frame_id] = keypoints
            else:
                _temp[frame_id] = keypoints
                scores[frame_id] = score

        for i in _temp.keys():
            if i > self.video_length:
                continue
            tmp = {}
            for j in range(len(self.joints_index_2_key.keys())):
                tmp[j] = list(_temp[i][j])
            self.joints2d[i] = tmp

        self.update_skeleton()

    def joint2d_init(self):
        self.joints2d = {}
        for i in range(self.video_length):
            frame_id = i + 1
            tmp = {}
            for j in range(len(self.joints_index_2_key.keys())):
                tmp[j] = None
            self.joints2d[frame_id] = tmp

    def load_from_joints2d(self):

        path = "../labelled_data/skeletons_2d/{}/{}.npy".format(
            self.path.split('/')[-2], self.path.split('/')[-1])
        if not os.path.exists(path):
            return
        skel = np.load(path)

        for i in range(self.video_length):
            frame_id = i + 1
            d = skel[i]
            if d.shape[-1] == 2:
                tmp = d
                d = np.ones((self.num_joints, 3))
                d[:, :2] = tmp

            for j in range(len(self.joints_index_2_key.keys())):
                self.joints2d[frame_id][j] = list(d[j])

        self.update_skeleton()

    def auto_interpolate(self):
        for joint in self.user_selected:
            start_frame = 1
            for idx, frame in enumerate(sorted(self.user_selected[joint])):
                if idx == 0:
                    for f in range(start_frame, frame):
                        self.joints2d[f][joint] = deepcopy(
                            self.user_selected[joint][frame])
                        self.joints2d[f][joint][-1] = 1
                else:
                    dif_x = self.user_selected[joint][frame][0] - \
                        self.user_selected[joint][start_frame][0]
                    dif_y = self.user_selected[joint][frame][1] - \
                        self.user_selected[joint][start_frame][1]
                    for f in range(start_frame+1, frame):
                        delta = (f-start_frame)/(frame - start_frame)
                        i_x = self.user_selected[joint][start_frame][0] + \
                            dif_x*delta
                        i_y = self.user_selected[joint][start_frame][1] + \
                            dif_y*delta
                        self.joints2d[f][joint] = [i_x, i_y, 1]

                if idx == (len(self.user_selected[joint])-1):
                    for f in range(frame+1, self.video_length+1):
                        self.joints2d[f][joint] = deepcopy(
                            self.user_selected[joint][frame])
                        self.joints2d[f][joint][-1] = 1
                start_frame = frame

    def label_everything(self):
        if self.label_everything_mode == True:
            self.label_everything_mode = False
            self.instruction.delete("oval")
            self.current_joint = -1
            self.current_joint_label.config(text="Current joint: None")
            return
        self.label_everything_mode = True
        self.current_joint = 0
        self.instruction.delete("oval")
        _x, _y = list(np.array(
            self.instruction_position[self.current_joint]) * self.instruction_size)
        self.instruction.create_oval(
            _x-3, _y-3, _x+3, _y+3, fill='red', outline='red', tags="oval")
        self.current_joint_label.config(text="Current joint: {}".format(
            self.joints_index_2_key[self.current_joint]))

    def check_if_labaled(self, skeleton):
        for f in skeleton:
            if skeleton[f] is None:
                return False
        return True

    def check_if_all_labeled(self):
        for joint in range(self.num_joints):
            for f in (self.joints2d):
                if self.joints2d[f] is None:
                    print('Fail to performance motion smoothing')
                    print('Please label frame {}, joint {}'.format(f, joint))
                    return False
        return True

    def gaussian_smoothing(self):

        if self.check_if_all_labeled():
            for joint in range(self.num_joints):
                xs = []
                ys = []
                for f in (self.joints2d):
                    _x = self.joints2d[f][joint][0]
                    _y = self.joints2d[f][joint][1]
                    xs.append(_x)
                    ys.append(_y)

                new_x = gaussian_filter1d(xs, sigma=1)
                new_y = gaussian_filter1d(ys, sigma=1)

                for f in (self.joints2d):
                    self.joints2d[f][joint][0] = new_x[f-1]
                    self.joints2d[f][joint][1] = new_y[f-1]

            self.update_skeleton()

    def temporal_predicting(self):
        print('Having some bug, currently undergoing fixing process ~')
        # return
        self.new = tk.Toplevel(self.root)
        self.temporal_window = Temporal_window(self.new, self)

    def modify_displaying(self):
        self.new = tk.Toplevel(self.root)
        self.modify_display_window = Modify_display_window(self.new, self)

    def shown_all(self):
        for joint in self.joints2d[self.current_frame]:
            if self.joints2d[self.current_frame][joint] is not None:
                self.joints2d[self.current_frame][joint][-1] = 1
        self.update_skeleton()

    def make_all_occ_or_unocc(self):
        if self.switch_variable.get() == 'off':
            return
        confidence_score = -1 if self.switch_variable.get() == 'occluded' else 1
        for joint in self.joints2d[self.current_frame]:
            if self.joints2d[self.current_frame][joint] is not None:
                self.joints2d[self.current_frame][joint][-1] = confidence_score
        self.update_skeleton()

    def reset_zoom(self):
        self.zoom = -4
        self.image_corner = [self.w_width*self.ratio *
                             (0.1), self.w_height*self.ratio*(0.1)]
        self.bone_width = 2
        self.joint_circle_size = 2
        self.bone_scale.set(self.bone_width)
        self.joint_circle_scale.set(self.joint_circle_size)
        self.show()

    def changed_frame(self, value):
        self.current_frame = int(value)
        self.label.config(text="Current frame: {}".format(self.current_frame))
        self.switch_variable.set('off')

        self.label_everything_mode = False
        self.instruction.delete("oval")
        self.current_joint = -1
        self.current_joint_label.config(text="Current joint: None")
        self.show()

    def event_handler(self, event):
        if str(event.type) == "MouseWheel":
            if event.delta < 0:
                self.zoom += 1
                self.zoom = min(self.zoom, 10)
            else:
                self.zoom -= 1
                self.zoom = max(self.zoom, -10)
            self.show()

        elif str(event.type) == "ButtonPress":
            if self.current_joint == -1:
                self.position = [event.x, event.y]
            else:
                scaler = 2**(self.zoom/5)
                position = [(event.x-self.image_corner[0])/scaler,
                            (event.y-self.image_corner[1])/scaler]

                if self.joints2d[self.current_frame][self.current_joint] is None:
                    self.joints2d[self.current_frame][self.current_joint] = [
                        position[0], position[1], 1]
                else:
                    self.joints2d[self.current_frame][self.current_joint][:2] = [
                        position[0], position[1]]

                self.user_selected[self.current_joint][self.current_frame] = [
                    position[0], position[1], 1]

                if self.label_everything_mode:
                    self.current_joint += 1
                    self.instruction.delete("oval")
                    if self.current_joint == self.num_joints:
                        self.current_joint = -1
                        self.label_everything_mode = False
                self.update_skeleton()
        elif str(event.type) == "Motion":
            if self.current_joint == -1:
                move = [event.x-self.position[0], event.y-self.position[1]]
                self.position = [event.x, event.y]
                self.image_corner[0] += move[0]
                self.image_corner[1] += move[1]
                self.show()

        elif str(event.type) == "KeyPress":
            if event.char == 'z':
                self.current_frame -= 1
                self.current_frame = max(1, self.current_frame)
                self.changed_frame(self.current_frame)
                self.scale.set(self.current_frame)
                self.switch_variable.set("off")

            elif event.char == 'x':
                self.current_frame += 1
                self.current_frame = min(self.video_length, self.current_frame)
                self.changed_frame(self.current_frame)
                self.scale.set(self.current_frame)
                self.switch_variable.set("off")

            elif event.char == '`':
                if self.current_joint != -1:
                    for i in range(self.video_length):
                        frame_id = i + 1
                        if self.joints2d[frame_id][self.current_joint] is not None:
                            self.joints2d[frame_id][self.current_joint][-1] = - \
                                1*self.joints2d[frame_id][self.current_joint][-1]
                self.update_skeleton()

            elif event.char == 'o' or event.char == 'p':
                if event.char == 'o':
                    for i in range(self.num_joints):
                        if (self.joints2d[self.current_frame][i] is not None) and (self.current_frame not in self.user_selected[i].keys()):
                            self.user_selected[i][self.current_frame] = self.joints2d[self.current_frame][i]
                else:
                    for i in range(self.num_joints):
                        try:
                            self.user_selected[i].pop(self.current_frame)
                        except:
                            pass

            elif event.char == '1' or event.char == '2' or event.char == '3' or event.char == '0':
                if self.current_joint != -1:
                    if self.joints2d[self.current_frame][self.current_joint] != None:
                        if event.char == '1':
                            if not self.label_everything_mode:
                                self.joints2d[self.current_frame][self.current_joint][-1] = - \
                                    1*self.joints2d[self.current_frame][self.current_joint][-1]
                            else:
                                self.joints2d[self.current_frame][self.current_joint][-1] = -1
                                self.current_joint += 1
                                if self.current_joint == self.num_joints:
                                    self.current_joint = -1
                        elif event.char == '3':
                            if self.label_everything_mode:
                                self.joints2d[self.current_frame][self.current_joint][-1] = 1
                                self.current_joint += 1
                                if self.current_joint == self.num_joints:
                                    self.current_joint = -1

                        elif event.char == '2':
                            self.joints2d[self.current_frame][self.current_joint] = None
                            try:
                                self.user_selected[self.current_joint].pop(
                                    self.current_frame)
                            except:
                                pass

                if event.char == '0':
                    for i in range(self.num_joints):
                        self.joints2d[self.current_frame][i] = None
                        try:
                            self.user_selected[i].pop(self.current_frame)
                        except:
                            pass

                self.update_skeleton()
            elif event.char == 'l':
                self.label_everything()

            elif event.char in self.key_bind_table:
                self.label_everything_mode = False
                self.instruction.delete("oval")
                index = self.key_bind_table.index(event.char)
                if self.current_joint == index:
                    self.current_joint = -1
                else:
                    self.current_joint = index
                self.update_skeleton()

    def toggle_3d_display(self):
        if not self.check_if_labaled(self.joints2d[self.current_frame]):
            self.plot_3d.clf()
            return
        self.show_3d = not self.show_3d
        self.show_3d_skeleton()

    def to_joints(self, joints_dict):
        joints = []
        for i in (joints_dict):
            info = joints_dict[i]
            if info == None:
                info = np.random.rand(self.num_joints, 3)
                info[:, -1] = -1
                info = list(info)
            joints.append(info)
        return np.array(joints)

    def show_3d_skeleton(self):
        self.plot_3d.clf()
        if self.show_3d:
            joints2d = self.to_joints(self.joints2d[self.current_frame])
            input = torch.Tensor(
                joints2d[np.newaxis][:, :, :2]).to(self.device)

            joints3d = self.evoNet.predict(input)[0]
            self.draw_3d_skeleton(joints3d)

        self.display_3d.draw()

    def show(self):
        path = self.path + '/{:04d}.png'.format(self.current_frame)
        self.image = Image.open(path)
        self.img_size = self.image.size
        self.update_image()
        self.update_skeleton()

    def update_skeleton(self):
        self.instruction.delete("oval")

        if self.current_joint == -1:
            self.current_joint_label.config(text="Current joint: None")
        else:
            _x, _y = list(np.array(
                self.instruction_position[self.current_joint]) * self.instruction_size)
            self.instruction.create_oval(
                _x-3, _y-3, _x+3, _y+3, fill='red', outline='red', tags="oval")
            self.current_joint_label.config(text="Current joint: {}".format(
                self.joints_index_2_key[self.current_joint]))

        try:
            skeleton = self.joints2d[self.current_frame]
        except:
            return

        if self.show_3d and self.check_if_labaled(skeleton):
            self.show_3d_skeleton()
        else:
            self.show_3d = False

        self.canvas.delete("oval")
        self.canvas.delete("bone")

        scaler = 2**(self.zoom/5)
        # draw bones
        for i, bones in enumerate(self.bones_indices):
            for bone in (bones):
                start = bone[0]
                end = bone[1]
                if skeleton[start] is not None and skeleton[end] is not None:
                    x0, y0 = list(np.array(self.image_corner) +
                                  np.array(skeleton[start][:2])*scaler)
                    x1, y1 = list(np.array(self.image_corner) +
                                  np.array(skeleton[end][:2])*scaler)
                    self.canvas.create_line(
                        x0, y0, x1, y1, fill=self.bone_colors[i], width=self.bone_width, tags='bone')

        # draw dots
        for key, value in zip(skeleton.keys(), skeleton.values()):
            if value is not None:
                r = self.joint_circle_size

                color = 'red' if key != self.current_joint else 'green'
                color = color if value[-1] == 1 else 'black'

                position = [self.image_corner[0]+value[0] *
                            scaler, self.image_corner[1]+value[1]*scaler]
                self.canvas.create_oval(position[0]-r, position[1]-r, position[0]+r, position[1]+r,
                                        fill=color, outline=color, tags='oval')

    def draw_3d_skeleton(self, skeleton, elev=-80, azim=-90):
        ax = self.plot_3d.add_subplot(111, projection="3d")

        max_range = np.amax(np.abs(skeleton))
        ax.set(xlim=[-max_range, max_range], ylim=[-max_range,
               max_range], zlim=[-max_range, max_range])
        # ax.view_init(elev=180, azim=0)

        bones_indices = [
            [[0, 4], [4, 5], [5, 6], [8, 11], [11, 12], [12, 13]],  # left -> pink
            [[0, 1], [1, 2], [2, 3], [8, 14], [14, 15], [15, 16]],  # right -> blue
            [[0, 7], [7, 8], [8, 9], [9, 10]]  # black
        ]  # left-> pink, right->blue

        for i, bones in enumerate(bones_indices):
            for bone in (bones):
                start = bone[0]
                end = bone[1]

                x0, y0, z0 = list(skeleton[start])
                x1, y1, z1 = list(skeleton[end])
                ax.plot([x0, x1], [y0, y1], [z0, z1])

        # draw dots
        sk = Skeleton()
        for i in range(17):
            if sk.dict_idx_2_joint[i] in (sk.body_parts['torso'] + sk.body_parts['head']):
                ax.scatter(skeleton[i, 0], skeleton[i, 1],
                           skeleton[i, 2], c='b')
            elif sk.dict_idx_2_joint[i] in (sk.body_parts['left_leg'] + sk.body_parts['left_arm']):
                ax.scatter(skeleton[i, 0], skeleton[i, 1],
                           skeleton[i, 2], c='r')
            elif sk.dict_idx_2_joint[i] in (sk.body_parts['right_leg'] + sk.body_parts['right_arm']):
                ax.scatter(skeleton[i, 0], skeleton[i, 1],
                           skeleton[i, 2], c='g')
            else:
                raise NotImplementedError

        ax.set(xlabel='x', ylabel='y', zlabel='z')
        ax.view_init(elev=elev, azim=azim)
        # ax.invert_zaxis()
        return

    def update_image(self):
        size = self.img_size
        new_size = (int(size[0] * 2**(self.zoom/5)),
                    int(size[1] * 2**(self.zoom/5)))
        self.image = self.image.resize(new_size)
        self.img = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(
            self.image_corner[0], self.image_corner[1], image=self.img, anchor="nw")

    def save(self):
        need_save = True
        # check if all are not None

        for frame in self.joints2d:
            for joint in self.joints2d[frame]:
                if self.joints2d[frame][joint] is None:
                    print('Frame {}, joint {} was not labelled'.format(frame, joint))
                    need_save = False

        if need_save:
            if not os.path.exists("../labelled_data"):
                os.mkdir("../labelled_data")
            out_dir_2d = '../labelled_data/skeletons_2d'
            if not os.path.exists(out_dir_2d):
                os.mkdir(out_dir_2d)
            video_class = self.path.split('/')[-2]
            video_name = self.path.split('/')[-1]
            if not os.path.exists('{}/{}'.format(out_dir_2d, video_class)):
                os.mkdir('{}/{}'.format(out_dir_2d, video_class))
            out_path_2d = '{}/{}/{}.npy'.format(out_dir_2d,
                                             video_class, video_name)

            out_dir_3d = '../labelled_data/skeletons_3d'
            if not os.path.exists(out_dir_3d):
                os.mkdir(out_dir_3d)
            if not os.path.exists('{}/{}'.format(out_dir_3d, video_class)):
                os.mkdir('{}/{}'.format(out_dir_3d, video_class))
            out_path_3d = '{}/{}/{}.npy'.format(out_dir_3d,
                                                video_class, video_name)

            skeletons_2d = []
            for frame in self.joints2d:
                if frame > self.video_length:
                    break
                my_list = []
                for joint in sorted(self.joints2d[frame]):
                    my_list.append(self.joints2d[frame][joint][:2])

                skeletons_2d.append(np.array(my_list))

            skeletons_2d = np.array(skeletons_2d)
            np.save(out_path_2d, skeletons_2d)

            skeletons_3d = self.convert_skeletons_3d(skeletons_2d)
            np.save(out_path_3d, skeletons_3d)

            print('Saved')

    def convert_skeletons_3d(self, skeletons_2d):

        input = torch.Tensor(
            skeletons_2d).to(self.device)

        skeletons_3d = self.evoNet.predict(input)
        
        return skeletons_3d

    def exit(self):
        self.key_unbinding()
        self.controller.show_frame('Page1')

    def save_and_exit(self):
        self.save()
        self.exit()
