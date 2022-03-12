import tkinter as tk
import numpy as np
from libs.temporal_network.main import TemporalModel

class Temporal_window(tk.Frame):
    def __init__(self, master, parent):
        super(Temporal_window, self).__init__()
        self.master = master
        self.parent = parent
        self.master.geometry('200x200')
        self.master.wm_title("Temporal Prediction")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.joints2d = parent.joints2d # shallow copy

        self.length = parent.video_length
    
        self.model = TemporalModel()

        default_options = list(np.arange(self.length) + 1)

        start_frame = tk.Label(self.master, text="Start frame:")
        start_frame.grid(row=0, column=0)
        self.v1 = tk.StringVar(master)
        self.v1.set(default_options[0]) # default value
        self.d1 = tk.OptionMenu(master, self.v1, *default_options)
        self.d1.grid(row=0, column=1)

        end_frame = tk.Label(self.master, text="End frame:")
        end_frame.grid(row=1, column=0)
        self.v2 = tk.StringVar(master)
        self.v2.set(default_options[1]) # default value
        self.d2 = tk.OptionMenu(master, self.v2, *default_options)
        self.d2.grid(row=1, column=1)

        predict_button = tk.Button(self.master, text="Predict", command=self.predict)
        predict_button.grid(row=2, columnspan=2)

        self.v1.trace('w', self.update_end_frame)

    def predict(self):
        start_frame = int(self.v1.get())
        end_frame = int(self.v2.get())

        input = []
        for i in range(start_frame, end_frame+1):  
            joints = self.to_joints(self.joints2d[i])
            input.append(joints)
        input = np.array(input)

        _, _, vid_2d_pred_recover, _ = self.model.predict(input, get_3d=True)

        for i in range(start_frame, end_frame+1):  
            for j in range(17):
                self.joints2d[i][j][:2] = vid_2d_pred_recover[i-start_frame][j]

        self.parent.update_skeleton()
        return

    def to_joints(self, joints_dict):
        joints = []
        for i in (joints_dict):
            info = joints_dict[i]
            if info == None:
                info = np.random.rand(17, 3)
                info[:, -1] = -1
                info = list(info)
            joints.append(info)
        return np.array(joints)

    def on_closing(self):
        self.master.destroy()

    def update_end_frame(self, *args):
        frames = list(np.arange(int(self.v1.get()), self.length) + 1)
        self.v2.set(frames[0])
        self.d2['menu'].delete(0, 'end')
        for f in frames:
            self.d2['menu'].add_command(label=f, command=lambda frame=f: self.v2.set(frame))

