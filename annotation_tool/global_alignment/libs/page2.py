import os
import sys
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from .util import get_rotation_matrix
from .find_rotation import get_rotation_matrix_3d
sys.path.append('../')
from labelling_ui.libs.visualizer import plot_2d, plot_3d

class Page2(tk.Frame):
    def __init__(self, data_type, root, controller, parent=None):
        tk.Frame.__init__(self, root)

        self.root = root
        self.data_type = data_type
        self.controller = controller
        self.parent = parent

        self.dataset_dir = "../../dataset"
        self.GAS_out_root = "{}/processed_data/globally_aligned_skeletons/{}".format(self.dataset_dir, self.data_type)

        self.R = np.identity(3)

       
        self.w_height = self.controller.winfo_screenheight()
        self.w_width = self.controller.winfo_screenwidth()

        self.class_name = ''
        self.vid = -1
        self.path = None
    
        self.w_height = self.controller.winfo_screenheight()
        self.w_width = self.controller.winfo_screenwidth()

        # Page 2 interface
        self.ratio = 4/5
        self.left_frame = tk.Frame(self, width=self.w_width*self.ratio)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        self.right_frame = tk.Frame(self, width =self.w_width*(1-self.ratio), height=700)
        self.right_frame.pack_propagate(0)
        self.right_frame.pack(side="right", fill="both", expand=False)

        self.controller_label = tk.Label(self.right_frame, text="Controller")
        self.controller_label.pack(fill="both", padx=20, pady=20)

        self.rx_frame = tk.Frame(self.right_frame)
        self.rx_frame.pack(fill="both",  padx=20, pady=10)
        self.rx_label = tk.Label(self.rx_frame, text="Rx: ")
        self.rx_label.pack(side="left")
        self.rx = tk.StringVar()
        self.rx_scale = tk.Scale(self.rx_frame, variable=self.rx, from_=-np.pi, to=np.pi, digits=3, resolution=0.01 ,orient=tk.HORIZONTAL, command=self.rotate)
        self.rx_scale.pack(side="top", fill="both")
        self.rx_scale.set(0)

        self.ry_frame = tk.Frame(self.right_frame)
        self.ry_frame.pack(fill="both",  padx=20, pady=10)
        self.ry_label = tk.Label(self.ry_frame, text="Ry: ")
        self.ry_label.pack(side="left")
        self.ry = tk.StringVar()
        self.ry_scale = tk.Scale(self.ry_frame, variable=self.ry, from_=-np.pi, to=np.pi, digits=3, resolution=0.01 ,orient=tk.HORIZONTAL, command=self.rotate)
        self.ry_scale.pack(side="top", fill="both")
        self.ry_scale.set(0)

        self.rz_frame = tk.Frame(self.right_frame)
        self.rz_frame.pack(fill="both",  padx=20, pady=10)
        self.rz_label = tk.Label(self.rz_frame, text="Rz: ")
        self.rz_label.pack(side="left")
        self.rz = tk.StringVar()
        self.rz_scale = tk.Scale(self.rz_frame, variable=self.rz, from_=-np.pi, to=np.pi, digits=3, resolution=0.01 ,orient=tk.HORIZONTAL, command=self.rotate)
        self.rz_scale.pack(side="top", fill="both")
        self.rz_scale.set(0)

        self.rx_input_frame = tk.Frame(self.right_frame)
        self.rx_input_frame.pack(fill="both",  padx=20, pady=10)
        self.rx_label_2 = tk.Label(self.rx_input_frame, text="Rx: ")
        self.rx_label_2.pack(side="left")
        self.rx_input_value = tk.StringVar(value='0')
        self.rx_input_box = tk.Entry(self.rx_input_frame, textvariable=self.rx_input_value) 
        self.rx_input_box.pack(side="top", fill="both")
        self.rx_input_box.bind('<Return>', (lambda _: self.callback(self.rx_input_box, self.rx)))

        self.ry_input_frame = tk.Frame(self.right_frame)
        self.ry_input_frame.pack(fill="both",  padx=20, pady=10)
        self.ry_label_2 = tk.Label(self.ry_input_frame, text="Ry: ")
        self.ry_label_2.pack(side="left")
        self.ry_input_value = tk.StringVar(value='0')
        self.ry_input_box = tk.Entry(self.ry_input_frame, textvariable=self.ry_input_value) 
        self.ry_input_box.pack(side="top", fill="both")
        self.ry_input_box.bind('<Return>', (lambda _: self.callback(self.ry_input_box, self.ry)))

        self.rz_input_frame = tk.Frame(self.right_frame)
        self.rz_input_frame.pack(fill="both",  padx=20, pady=10)
        self.rz_label_2 = tk.Label(self.rz_input_frame, text="Rz: ")
        self.rz_label_2.pack(side="left")
        self.rz_input_value = tk.StringVar(value='0')
        self.rz_input_box = tk.Entry(self.rz_input_frame, textvariable=self.rz_input_value) 
        self.rz_input_box.pack(side="top", fill="both")
        self.rz_input_box.bind('<Return>', (lambda _: self.callback(self.rz_input_box, self.rz)))

        reset_button = tk.Button(self.right_frame, text="Reset", command=self.reset)
        reset_button.pack(fill="both", padx=5, pady=5)

        lsq_button = tk.Button(self.right_frame, text="Use Least Square", command=self.least_square)
        lsq_button.pack(fill="both", padx=5, pady=5)

        load_button = tk.Button(self.right_frame, text="Load", command=self.load)
        load_button.pack(fill="both", padx=5, pady=5)

        alignment_button = tk.Button(self.right_frame, text="Align whole video", command=self.align)
        alignment_button.pack(fill="both", padx=5, pady=5)


        self.plot_alignment = Figure(figsize=(10, 3), dpi=90)
        self.display_3d = FigureCanvasTkAgg(self.plot_alignment, master=self.left_frame)
        self.display_3d.get_tk_widget().pack(side="top")

        self.plot_video = Figure(figsize=(10, 3), dpi=90)
        self.display_video = FigureCanvasTkAgg(self.plot_video, master=self.left_frame)
        self.display_video.get_tk_widget().pack(side="top")

        lb_frame = tk.Frame(self.left_frame, width=self.w_width*self.ratio, height=self.w_height*(1-self.ratio))
        lb_frame.pack(side="top", fill="x", anchor="nw", expand=False, padx=20, pady=20)
        self.scale = tk.Scale(lb_frame, from_=0, to=1, orient=tk.HORIZONTAL, command=self.change_frame)
        self.scale.pack(side="top", fill="both")

        frame = tk.Frame(self.right_frame)
        frame.pack(side="bottom", fill="both")

        save_button = tk.Button(frame, text="Save", command=self.save)
        save_button.pack(fill="both", padx=5, pady=5, side="bottom")

        exit_button = tk.Button(frame, text="Exit", command=self.exit)
        exit_button.pack(fill="both", padx=5, pady=5, side="bottom")

        save_and_exit_button = tk.Button(frame, text="Save and Exit", command=self.save_and_exit)
        save_and_exit_button.pack(fill="both", padx=5, pady=5, side="bottom")  
    

    def initialize(self):
        
        self.class_name = self.parent.current_video[0]
        try:
            self.video_name = self.parent.current_video[1]
            self.skeletons_3d = np.load(self.parent.skeletons_3d_root+'/{}/{}.npy'.format(self.class_name, self.video_name))

        except:
            self.video_name = self.parent.current_video[1][:-2]
            self.skeletons_3d = np.load(self.parent.skeletons_3d_root+'/{}/{}.npy'.format(self.class_name, self.video_name))
       

        self.rx.set('0')
        self.ry.set('0')
        self.rz.set('0')
        self.rx_input_value.set('0')
        self.ry_input_value.set('0')
        self.rz_input_value.set('0')

        self.skeleton_3d = np.copy(self.skeletons_3d[0])
        self.R = np.identity(3)
        self.rotated_skeleton = np.matmul(self.R, self.skeleton_3d.T).T
        
        self.video_length = self.skeletons_3d.shape[0]
        self.scale.configure(from_=1, to=self.video_length)
        self.scale.set(0)

        self.rotated_skeletons = np.copy(self.skeletons_3d)

        self.plot_global_alignment()
        self.plot_video_alignment(0)
    
    def align(self):
        n_frames = self.skeletons_3d.shape[0]
        expanded_R = np.repeat(np.expand_dims(self.R, 0), n_frames, axis=0)
        self.rotated_skeletons = np.transpose(np.matmul(expanded_R, np.transpose(self.skeletons_3d, (0, 2, 1))), (0, 2, 1))
        
    def change_frame(self, frame):
        self.plot_video_alignment(int(frame)-1)


    def callback(self, sv, rotate_axis):
        rotate_axis.set(sv.get())
        self.rotate()

    def rotate(self, input=None):
        theta_x = float(self.rx.get())
        theta_y = float(self.ry.get())
        theta_z = float(self.rz.get())

        self.rx_input_value.set('{}'.format(theta_x))
        self.ry_input_value.set('{}'.format(theta_y))
        self.rz_input_value.set('{}'.format(theta_z))
        self.R = get_rotation_matrix(theta_x, theta_y, theta_z)
        self.rotated_skeleton = np.matmul(self.R, np.copy(self.skeleton_3d.T)).T

        self.plot_global_alignment()

    def plot_video_alignment(self, i):
        self.plot_video.clf()

        ax = self.plot_video.add_subplot(141, projection='3d')
        plot_3d(self.rotated_skeletons[i], 'haa4d', ax, elev=-90)

        ax = self.plot_video.add_subplot(142)
        plot_2d(self.rotated_skeletons[i][ :, :-1], 'haa4d', ax)

        ax = self.plot_video.add_subplot(143)
        plot_2d(self.rotated_skeletons[i][ :, [0,2]], 'haa4d', ax, ylabel='z', ylim=[-1,1])

        ax = self.plot_video.add_subplot(144)
        plot_2d(self.rotated_skeletons[i][ :, [2,1]], 'haa4d', ax, xlim=[1,-1], xlabel='z')

        self.plot_video.suptitle('Video')
        self.plot_video.tight_layout()
        self.display_video.draw()
        return 

    def plot_global_alignment(self):
        self.plot_alignment.clf()

        ax = self.plot_alignment.add_subplot(141, projection='3d')
        plot_3d(self.rotated_skeleton, 'haa4d', ax, elev=-90)

        ax = self.plot_alignment.add_subplot(142)
        plot_2d(self.rotated_skeleton[:, :-1], 'haa4d', ax)

        ax = self.plot_alignment.add_subplot(143)
        plot_2d(self.rotated_skeleton[:, [0,2]], 'haa4d', ax, ylabel='z', ylim=[-1,1])

        ax = self.plot_alignment.add_subplot(144)
        plot_2d(self.rotated_skeleton[:, [2,1]], 'haa4d', ax, xlim=[1,-1], xlabel='z')

        self.plot_alignment.suptitle(self.class_name)
        self.plot_alignment.tight_layout()
        self.display_3d.draw()
        return 
    
    def reset(self):
        self.rx.set(0)
        self.ry.set(0)
        self.rz.set(0)

        self.rx_input_value.set(0)
        self.ry_input_value.set(0)
        self.rz_input_value.set(0)

        self.rotate()

    def least_square(self):
        ref_skeleton_path = '{}/{}/{}_000.npy'.format(self.GAS_out_root, self.class_name, self.class_name)
        if not os.path.exists(ref_skeleton_path):
            print('Please label the first video')
            return

        ref_skeleton = np.load(ref_skeleton_path)[0]
        _, R = get_rotation_matrix_3d(self.skeleton_3d, ref_skeleton)

        theta_x = np.arctan2(R[2,1], R[2,2])
        theta_y = np.arctan2(-R[2,0], np.sqrt(np.square(R[2,1])+np.square(R[2,2])))
        theta_z = np.arctan2(R[1,0], R[0,0])

        self.rx.set(theta_x)
        self.ry.set(theta_y)
        self.rz.set(theta_z)

        self.rx_input_value.set(theta_x)
        self.ry_input_value.set(theta_y)
        self.rz_input_value.set(theta_z)

        self.rotate()

    def load(self):
        load_path = '{}/processed_data/global_alignment_rotation/{}/{}.npy'.format(self.dataset_dir, self.class_name, self.video_name)
        video_out_path = '{}/{}/{}.npy'.format(self.GAS_out_root, self.class_name, self.video_name)

        if os.path.exists(load_path):
            data = np.load(load_path)
            theta_x = data[0]
            theta_y = data[1]
            theta_z = data[2]

            self.rx.set(theta_x)
            self.ry.set(theta_y)
            self.rz.set(theta_z)

            self.rx_input_value.set(theta_x)
            self.ry_input_value.set(theta_y)
            self.rz_input_value.set(theta_z)

            self.rotate()

            self.rotated_skeletons = np.load(video_out_path)

            


    def save(self):
        if not os.path.exists('{}/processed_data/global_alignment_rotation'.format(self.dataset_dir)):
            os.mkdir('{}/processed_data/global_alignment_rotation'.format(self.dataset_dir))
        if not os.path.exists('{}'.format(self.GAS_out_root)):
            os.mkdir(self.GAS_out_root)
        
        out_path = '{}/processed_data/global_alignment_rotation/{}/{}.npy'.format(self.dataset_dir, self.class_name, self.video_name)
        if not os.path.exists('{}/processed_data/global_alignment_rotation/{}'.format(self.dataset_dir, self.class_name)):
            os.mkdir('{}/processed_data/global_alignment_rotation/{}'.format(self.dataset_dir, self.class_name))

        np.save(out_path, np.array([float(self.rx_input_value.get()), float(self.ry_input_value.get()), float(self.rz_input_value.get())]))

        self.align()
        video_out_path = '{}/{}/{}.npy'.format(self.GAS_out_root, self.class_name, self.video_name)
        if not os.path.exists('{}/{}'.format(self.GAS_out_root, self.class_name)):
            os.mkdir('{}/{}'.format(self.GAS_out_root, self.class_name))
        
        np.save(video_out_path, self.rotated_skeletons)

    
    def show(self):
        pass
    
    def exit(self):
        self.controller.show_frame('Page1')
    
    def save_and_exit(self):
        self.save()
        self.exit()