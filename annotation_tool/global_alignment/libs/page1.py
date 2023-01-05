import os
import glob
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

class Page1(tk.Frame):
    def __init__(self, data_type, root, controller, parent=None):
        tk.Frame.__init__(self, root)

        self.name = 'Page 1'
        self.data_type = data_type
        self.root = root
        self.controller = controller
        self.parent = parent
        self.current_video = None
        self.dataset_dir = "../../dataset"
        self.GAS_out_root = "{}/processed_data/globally_aligned_skeletons/{}".format(self.dataset_dir, self.data_type)
        self.skeletons_3d_root =  "{}/processed_data/normalized_skeletons_3d".format(self.dataset_dir)

        s = ttk.Style()
        s.configure('Treeview', rowheight=50) 

        frame1 = tk.Frame(self)
        frame1.pack(side="top", fill="both")

        treeview = ttk.Treeview(self)
        self.treeview = treeview
        self.treeview.pack(expand=True, fill=tk.BOTH)
        self.treeview.bind("<Double-1>", lambda x : self.btn_action())
        
        frame2 = tk.Frame(self)
        frame2.pack(side="bottom", fill="both")

        button = ttk.Button(frame2, text="select", command=self.btn_action)
        button.pack(side=tk.LEFT, padx=20, pady=20)

        self.T = tk.Label(frame2, height=2, text="", fg="red")
        self.T.pack(side=tk.LEFT, fill="both")

    def initialize(self):
        pass


    def show(self):
        self.treeview.delete(*self.treeview.get_children())
        videos = defaultdict(list)

        for video in glob.glob("{}/processed_data/normalized_skeletons_3d/*/*".format(self.dataset_dir)):
            class_name = video.split("/")[-2]
            video_name = video.split("/")[-1].split('.')[0]

            if int(video_name[-3:]) > 9:
                continue
            videos[class_name].append(video_name)

        for i, class_name in enumerate(sorted(videos.keys())):
            self.treeview.insert('',i+1,class_name, text = class_name)

            for j, video_name in enumerate(sorted(videos[class_name])):
                text_name = video_name
                if os.path.exists("{}/{}/{}.npy".format(self.GAS_out_root, class_name, video_name)):
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
        
