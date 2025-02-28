from tkinter import *
color = None
class FRAME: # handles Frame-widgets

    def __init__(self, name, master, orientation, sx, sy, color, border=False, anchor=None):
        self.name = name
        self.children = {}
        self.master = master
        self.sx, self.sy = sx, sy

        self.frame = Frame(master.frame, height=sy, width=sx, relief=SOLID, bd=border, bg=color)
        self.frame.pack_propagate(0)
        self.frame.pack(side=orientation, anchor=anchor)


    def resize(self, factor): # on window resize
        self.frame.configure(width=int(factor*self.sx), height=int(factor*self.sy))
        for child in self.children.values():
            child.resize(factor)


    def add_frame(self, name, orientation, sx, sy, color, border=False): # creates new FRAME, adds it as child
        obj = FRAME(name, self, orientation, sx, sy, color, border=border)
        self.children.update({name : obj})


    def add_obj(self,obj): # add object to childs
        self.children.update({obj.name : obj})


    def get(self, name): # tree search for name
        if self.name == name:
            return self
        else:
            for child in self.children.values():
                val = child.get(name)
                if val:
                    return val

        return None

    def get_all(self):
        return self.children


class BUTTON:

    def __init__(self, name, master, orientation, sx, sy, _text, _color, method):
        self.color = _color
        self.name = name
        self.master = master
        self.sx = sx
        self.sy = sy

        self.frame = Frame(master.frame, height=sy, width=sx, bd=0, relief=SOLID, bg=_color)
        self.frame.pack_propagate(0)
        self.frame.pack(side=orientation)

        self.button = Button(self.frame, command=method, bd=1, relief=SOLID, bg=_color, fg=color.color_text_low, activebackground=color.color_click)
        self.button.pack_propagate(0)
        self.button.pack(fill=BOTH, expand=1)
        self.re_text(_text)


    def re_text(self, new_text):
        self.button.configure(text=new_text)


    def resize(self, scale):
        self.frame.configure(height=int(scale*self.sy), width=int(scale*self.sx))


    def activate(self):
        self.button.configure(bg=color.color_active)


    def deactivate(self):
        self.button.configure(bg=self.color)


    def get(self, name):
        if self.name == name:
            return self
        else:
            return None


class LABEL:

    def __init__(self, name, master, orientation, sx, sy, _text, color_fg, color_bg):
        self.name = name
        self.master = master
        self.sx = sx
        self.sy = sy

        self.frame = Frame(master.frame, height=sy, width=sx, bd=0, relief=SOLID, bg=color_bg)
        self.frame.pack_propagate(0)
        self.frame.pack(side=orientation)

        self.label = Label(self.frame, bd=0, bg=color_bg, fg=color_fg)
        self.label.pack_propagate(0)
        self.label.pack(fill=BOTH, expand=1)
        self.re_text(_text)

    def re_text(self, new_text):
        self.label.configure(text=new_text)

    def resize(self, scale):
        self.frame.configure(height=int(scale * self.sy), width=int(scale * self.sx))

    def re_color(self, _color):
        self.label.configure(fg=_color)

    def get(self, name):
        if self.name == name:
            return self
        else:
            return None