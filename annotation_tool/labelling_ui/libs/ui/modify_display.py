import tkinter as tk
import numpy as np

class Modify_display_window(tk.Frame):
    def __init__(self, master, parent):
        super(Modify_display_window, self).__init__()
        self.master = master
        self.parent = parent
        self.master.geometry('200x200')
        self.master.wm_title("Modify joint and bone size")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.joints2d = parent.joints2d # shallow copy

        self.length = parent.video_length
    
        self.bone_label = tk.Label(self.master, text="Set line width of Bone", fg="black")
        self.bone_label.pack(fill="both")
        self.bone_scale = tk.Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, command=self.changed_bone)
        self.bone_scale.pack(side="top", fill="both")
        self.bone_scale.set(2)

        self.joint_circle_label = tk.Label(self.master, text="Set circle size of joint", fg="black")
        self.joint_circle_label.pack(fill="both")
        self.joint_circle_scale = tk.Scale(self.master, from_=1, to=10, orient=tk.HORIZONTAL, command=self.changed_joint_circle)
        self.joint_circle_scale.pack(side="top", fill="both")
        self.joint_circle_scale.set(2)

    def on_closing(self):
        self.master.destroy()

    def changed_bone(self, value):
        self.parent.bone_width = int(value)
        self.parent.update_skeleton()

    def changed_joint_circle(self, value):
        self.parent.joint_circle_size = int(value)
        self.parent.update_skeleton()
    