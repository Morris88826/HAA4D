import tkinter as tk
from libs.ui.page1 import Page1
from libs.ui.page2 import Page2

class MainView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("2D Annotation")
        try:
            self.attributes('-zoomed', True)
            self.bind("<Escape>", lambda event: self.attributes("-zoomed", False))
        except:
            self.attributes('-fullscreen', True)
            self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))

        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)

        # initializing frames to an empty array
        self.frames = {} 
        self.frames['Page1'] = Page1(container, self)
        self.frames['Page2'] = Page2(container, self, parent=self.frames['Page1'])

        self.frames['Page1'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.frames['Page2'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        
        self.show_frame('Page1')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.initialize()
        frame.show()
        frame.tkraise()


if __name__ == "__main__":
    main = MainView()
    main.mainloop()