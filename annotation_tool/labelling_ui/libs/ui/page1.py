import tkinter as tk
from tkinter import ttk
import glob
import os
import numpy as np
from collections import defaultdict

class Page1(tk.Frame):
    def __init__(self, root, controller, parent=None):
        tk.Frame.__init__(self, root)

        self.name = 'Page 1'
        self.root = root
        self.controller = controller
        self.parent = parent
        self.current_video = None

        s = ttk.Style()
        s.configure('Treeview', rowheight=50) 

        # label = tk.Label(self, text="This is page 1")
        # label.pack()

        treeview = ttk.Treeview(self)
        self.treeview = treeview
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.bind("<Double-1>", lambda x : self.btn_action())
        
        frame = tk.Frame(self)
        frame.pack(side="bottom", fill="both")

        button = ttk.Button(frame, text="select", command=self.btn_action)
        button.pack(side=tk.LEFT, padx=20, pady=20)

        self.T = tk.Label(frame, height=2, text="", fg="red")
        self.T.pack(side=tk.LEFT, fill="both")

    def initialize(self):
        pass

    def show(self):
        self.treeview.delete(*self.treeview.get_children())
        videos = defaultdict(list)

        for video in glob.glob("../../dataset/raw/*/*"):
            class_name = video.split("/")[-2]
            video_name = video.split("/")[-1]
            videos[class_name].append(video_name)

        for i, class_name in enumerate(sorted(videos.keys())):
            self.treeview.insert('',i+1,class_name, text = class_name)

            for j, video_name in enumerate(sorted(videos[class_name])):
                text_name = video_name
                if os.path.exists("../labelled_data/skeletons_2d/{}/{}.npy".format(class_name, video_name)):
                    skel = np.load(
                        "../labelled_data/skeletons_2d/{}/{}.npy".format(class_name, video_name))
                    if skel.shape[0] == len(glob.glob("../../dataset/raw/{}/{}/*.png".format(class_name, video_name))):
                        text_name += ' *'
                self.treeview.insert(class_name, j+1, video_name, text = text_name)

    def btn_action(self):

        selected = self.treeview.selection()

        if len(selected) == 0:
            self.T.config(text="nothing is selected")
            return
        
        selected = selected[0]

        parent = self.treeview.parent(selected)

        self.T.config(text="")
        self.current_video = [parent, selected]

        if parent != "":
            self.controller.show_frame('Page2')

        return
        
