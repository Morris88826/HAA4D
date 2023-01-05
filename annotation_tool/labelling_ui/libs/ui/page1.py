import os
import glob
import json
import numpy as np
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

class Page1(tk.Frame):
    def __init__(self, root, controller, parent=None):
        tk.Frame.__init__(self, root)
        self.dataset_root = "../../dataset"
        self.name = 'Page 1'
        self.root = root
        self.controller = controller
        self.parent = parent
        self.current_video = None

        s = ttk.Style()
        s.configure('Treeview', rowheight=50) 

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
        with open(self.dataset_root+'/info.json', 'rb') as jsonfile:
            self.info = json.load(jsonfile)

        self.progress = [f.split('/')[-1].split('.')[0] for f in glob.glob(self.dataset_root+'/skeletons_2d/*/*')]

    def show(self):
        self.treeview.delete(*self.treeview.get_children())
        videos = defaultdict(lambda: defaultdict(list))

        videos["primary_classes"] = defaultdict(list)
        videos["additional_classes"] = defaultdict(list)
 
        for video in glob.glob("{}/images/*/*".format(self.dataset_root)):
            class_name = video.split("/")[-2]
            video_name = video.split("/")[-1]

            if class_name in self.info["primary_classes"]:
                videos["primary_classes"][class_name].append(video_name)
            elif class_name in self.info["additional_classes"]:
                videos["additional_classes"][class_name].append(video_name)

        self.treeview.insert('', 1, "primary_classes", text = "Primary Classes")
        for i, class_name in enumerate(sorted(videos["primary_classes"].keys())):
            self.treeview.insert('primary_classes', i+1, class_name, text = class_name)
            for j, video_name in enumerate(sorted(videos["primary_classes"][class_name])):
                text_name = video_name
                if(text_name in self.progress):
                    text_name += ' *'
                self.treeview.insert(class_name, j+1, video_name, text = text_name)
        self.treeview.insert('', 2, "additional_classes", text = "Additional Classes")
        for i, class_name in enumerate(sorted(videos["additional_classes"].keys())):
            self.treeview.insert('additional_classes', i+1, class_name, text = class_name)
            for j, video_name in enumerate(sorted(videos["additional_classes"][class_name])):
                text_name = video_name
                if(text_name in self.progress):
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

        if parent != "" and parent!= "primary_classes" and parent!="additional_classes":
            self.controller.show_frame('Page2')

        return
        
