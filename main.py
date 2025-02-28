from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askokcancel
import os
from functools import partial
import color_themes, languages
from note import NOTE
import note
from copy import deepcopy
from gui_elements import *
import gui_elements
from song import SONG
import time
from plotter import plott
import plotter

# TODO: link maker
# TODO: settings bar
# TODO: logic
# TODO: export
# TODO: live view
# TODO: cutter
# TODO: Settings
# TODO: piano_creator
# TODO: veeh_creator



settings = {
    "language" : "english",
    "color_theme" : "dark"
}

def load_settings():
    global color
    global text
    global keys

    color = color_themes.load_theme(settings["color_theme"])

    text = languages.load_language(settings["language"])
    keys = text.keys
    note.lng = text
    plotter.lng = text
    gui_elements.color = color



class main: # Controlling Class

    # For main:

    def __init__(self):
        self.frame = Tk()
        self.frame.title("Veeh-Harpenator 2.0 (Benjamin Schaab)")
        self.frame.configure(bg=color.surface_6)
        self.frame.bind("<Configure>", self.configure)

        #Variables
        self.song = SONG()

        #Initial resolution for scaling
        self.factor = 1
        self.fx, self.fy = 1000, 500
        self.frame.wm_minsize(width=self.fx, height=self.fy)

        #INIT
        self.create_gui_structure()

        self.info = INFO(self.main_frame.get("info_frame"), 400, 200)

        self.but_wo = button_worker(self.main_frame.get("create_frame"), 800, 300, self.get_update, self.get_add)
        self.but_wo.activate()

        self.list = LIST(self.main_frame.get("notes_frame"), self.main_frame.get("note_tools"), 200, 350, self.insert,
                         self.load_note, self.delete, self.info.failure, self.list_callback)

        self.link = LINK(self.main_frame.get("link_frame"), self.link_add_remove)

        self.show = BUTTON("show", self.main_frame.get("settings_frame"), LEFT, 200, 200, "show", color.surface_2, self.show_plott)

        self.load = BUTTON("load", self.main_frame.get("load_save_frame"), TOP, 200, 75, "load", color.surface_3, self.load_song)
        self.save = BUTTON("save", self.main_frame.get("load_save_frame"), BOTTOM, 200, 75, "save", color.surface_4, self.save_song)


        #START
        self.frame.mainloop()


    def create_gui_structure(self):
        # GUI Structure
        self.main_frame = FRAME("main_frame", self, LEFT, 1000, 500, color.surface_6)

        self.main_frame.add_frame("work_frame", LEFT, 800, 500, color.surface_6, border=1)

        self.main_frame.get("work_frame").add_frame("create_frame", TOP, 800, 300, color.surface_1, border=1)

        self.main_frame.get("work_frame").add_frame("tool_frame", TOP, 800, 50, color.surface_3)

        self.main_frame.get("tool_frame").add_frame("link_frame", LEFT, 500, 50, color.surface_3, border=1)

        self.main_frame.get("tool_frame").add_frame("current_frame", RIGHT, 300, 50, color.surface_3, border=1)

        self.current_label = LABEL("current_label", self.main_frame.get("current_frame"), LEFT, 300, 50, "",
                                   color.color_text_low, color.surface_3)
        self.main_frame.get("current_frame").add_obj(self.current_label)

        self.main_frame.get("work_frame").add_frame("bottom_frame", TOP, 800, 200, color.surface_4)

        self.main_frame.get("bottom_frame").add_frame("settings_frame", LEFT, 400, 200, color.surface_4, border=1)

        self.main_frame.get("settings_frame").add_frame("load_save_frame", RIGHT, 200, 200, color.surface_4, border=0)

        self.main_frame.get("bottom_frame").add_frame("info_frame", RIGHT, 400, 200, color.surface_3, border=1)

        self.main_frame.add_frame("history_frame", RIGHT, 200, 500, color.surface_6, border=1)

        self.main_frame.get("history_frame").add_frame("notes_frame", TOP, 200, 350, color.surface_5, border=1)

        self.main_frame.get("history_frame").add_frame("note_tools", TOP, 200, 150, color.surface_4, border=1)


    def configure(self, event): # Called when Window changes
        # Resize all Widgets
        sx, sy = self.frame.winfo_width(), self.frame.winfo_height()

        if sx / self.fx < sy / self.fy:
            factor = sx / self.fx
        else:
            factor = sy / self.fy

        if factor == self.factor:
            return
        self.factor = factor
        print(factor)

        self.main_frame.resize(factor)
        self.but_wo.resize(factor)
        self.list.resize(factor)
        self.info.resize(factor)
        self.link.resize(factor)


    # For Creator:

    def get_update(self, note):
        self.current_label.re_text(note.to_text())
        if note.verify():
            self.current_label.re_color(color.color_text_high)
        else:
            self.current_label.re_color(color.color_text_low)


    def get_add(self, note):
        if note.verify():
            deep_note = deepcopy(note)
            self.song.add_note(deep_note)
            self.list.update(self.song)
            self.list_callback(None)
            self.info.success(str(deep_note) + " " + text.added)
            return True
        else:
            self.info.failure(note.report_problem())
            return False

    def insert(self, index):
        note = self.but_wo.get_note()
        if note.verify():
            deep_note = deepcopy(note)
            self.song.add_note(deep_note, pos=index)
            self.info.success(str(deep_note) + " " + text.inserted + " " + str(self.song.get_note(index + 1)))
            self.list.update(self.song)
            self.list_callback(None)
            self.but_wo.reset()
        else:
            self.info.failure(note.report_problem())
            return False

    def load_note(self, index):
        note = deepcopy(self.song.get_note(index))
        note.links = []
        self.but_wo.load(note)
        self.info.success(str(note) + " " + text.loaded)

    def delete(self, index):
        self.info.success(str(self.song.get_note(index)) + " " + text.deleted)
        self.song.del_note(index)
        self.list.update(self.song)
        self.list_callback(None)

    def list_callback(self, event):
        index = self.list.get_index()
        if index != None:
            note = self.song.get_note(index)
            self.link.note_change(note.links)
        else:
            self.link.note_change(None)

    def link_add_remove(self, id):
        index = self.list.get_index()
        if index == None:
            self.info.failure(text.prob_no_selection)
            return
        note = self.song.get_note(index)
        ammount = self.song.link_ammount(id)
        if id in note.links:
            note.remove_link(id)
            self.info.info(text.removed_link + " " + str(id) + " " + text.text_from + " " + str(note))
        else:
            if ammount == 0:
                note.add_link(id)
                self.info.success(text.added_link + " " + str(id) + " " + text.text_to + " " + str(note))
            elif ammount == 1:
                note.add_link(id)
                self.info.success(text.added_link + " " + str(id) + " " + text.text_to + " " + str(note)
                                  + ". " + text.link_done)
            else:
                self.info.failure(text.prob_many_link)
        self.list_callback(None)
        self.list.update(self.song)

    def show_plott(self):
        plott(deepcopy(self.song), grid=True)

    def save_song(self):
        csv = self.song.to_csv()
        file = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if file == "":
            return
        if os.path.exists(file):
            if not askokcancel("File already exists", "Do you want to overwrite the file?"):
                return
        with open(file, "w") as f:
            f.write(csv)
        self.info.success("Song saved to " + file)

    def load_song(self):
        if not self.song.is_empty():
            if not askokcancel("Load new song", "Do you want to discard the current song?"):
                return
        file = askopenfilename(filetypes=[("CSV", "*.csv")])
        if file == "":
            return
        with open(file, "r") as f:
            csv = f.read()
        self.song = SONG()
        self.song.from_csv(csv)
        self.list.update(self.song)
        self.info.success("Song loaded from " + file)


class LINK:

    def __init__(self, master, add_remove_cb):
        self.add_remove_cb = add_remove_cb
        self.label = LABEL("link_label", master, LEFT, 100, 50, text.label_link, color.color_text_low, color.surface_3)
        self.id = LABEL("link_id", master, LEFT, 35, 35, "0", color.color_text_high, color.surface_2)
        self.empty_frame1 = FRAME("empty1", master, LEFT, 10, 50, color.surface_3)
        self.button_frame = FRAME("up_down_frame", master, LEFT, 25, 50, color.surface_3)
        self.button_up = BUTTON("up_button", self.button_frame, TOP, 25, 24, "/\\", color.surface_3, self.up_callback)
        self.button_down = BUTTON("down_button", self.button_frame, BOTTOM, 25, 25, "\\/",
                                  color.surface_3, self.down_callback)
        self.empty_frame2 = FRAME("empty2", master, LEFT, 60, 50, color.surface_3)
        self.add = BUTTON("add_remove", master, LEFT, 120, 50, "", color.surface_3, self.add_remove)
        self.cur_id = 0
        self.cur_links = None

    def up_callback(self):
        self.cur_id += 1
        self.id.re_text(self.cur_id)
        self.update_text()

    def down_callback(self):
        if self.cur_id > 0:
            self.cur_id -= 1
            self.id.re_text(self.cur_id)
            self.update_text()

    def update_text(self):
        if self.cur_links == None:
            self.add.re_text("")
        elif self.cur_id in self.cur_links:
            self.add.re_text(text.link_but_rem)
        else:
            self.add.re_text(text.link_but_add)

    def add_remove(self):
        self.add_remove_cb(self.cur_id)

    def resize(self, factor):
        for item in [self.label, self.id, self.empty_frame1, self.button_frame, self.button_up, self.button_down,
                     self.empty_frame2, self.add]:
            item.resize(factor)

    def note_change(self, links):
        self.cur_links = links
        self.update_text()


class LIST:

    def __init__(self, master, tools, sx, sy, insert_cb, load_cb, delete_cb, problem_cb, update_cb):
        self.sx = sx
        self.sy = sy
        self.insert_cb = insert_cb
        self.load_cb = load_cb
        self.delete_cb = delete_cb
        self.problem_cb = problem_cb
        self.listbox = Listbox(master.frame, height=sy, width=sx, bg=color.surface_5, bd=0, fg=color.color_text_low,
                               selectmode=SINGLE, relief=FLAT, selectbackground=color.color_active,
                               highlightthickness=0)
        self.listbox.pack_propagate(0)
        self.listbox.pack()
        self.listbox.bind('<<ListboxSelect>>', update_cb)

        self.insert_button = BUTTON("insert", tools, TOP, 200, 70, text.insert, color.surface_4, self.insert_callback)
        self.load_button = BUTTON("load", tools, LEFT, 100, 80, text.load, color.surface_4, self.load_callback)
        self.delete_button = BUTTON("delete", tools, RIGHT, 100, 80, text.delete, color.surface_4, self.delete_callback)

    def update(self, song):
        self.listbox.delete(0, END)
        for note in song.get_notes():
            string = " " + str(note) + " "
            if len(note.links) > 0:
                string += str(note.links)
            self.listbox.insert(END, " " + string)

    def resize(self, factor):
        self.listbox.configure(width=int(factor * self.sx), height=int(factor * self.sy))
        self.insert_button.resize(factor)
        self.load_button.resize(factor)
        self.delete_button.resize(factor)

    def insert_callback(self):
        index = self.listbox.curselection()
        if len(index) == 0:
            if self.listbox.size() == 0:
                self.problem_cb(text.prob_no_item)
            else:
                self.problem_cb(text.prob_no_selection)
            return
        else:
            self.insert_cb(index[0])

    def load_callback(self):
        index = self.listbox.curselection()
        if len(index) == 0:
            if self.listbox.size() == 0:
                self.problem_cb(text.prob_no_item)
            else:
                self.problem_cb(text.prob_no_selection)
            return
        else:
            self.load_cb(index[0])

    def delete_callback(self):
        index = self.listbox.curselection()
        if len(index) == 0:
            if self.listbox.size() == 0:
                self.problem_cb(text.prob_no_item)
            else:
                self.problem_cb(text.prob_no_selection)
            return
        else:
            self.delete_cb(index[0])

    def get_index(self):
        index = self.listbox.curselection()
        if len(index) == 0:
            return None
        return index[0]



class INFO:

    def __init__(self, master, sx, sy):
        self.label = LABEL("info", master, TOP, sx, sy, "", color.text_info, color.surface_3)

    def resize(self, factor):
        self.label.resize(factor)

    def success(self, text):
        self.label.re_color(color.text_success)
        self.label.re_text(text)

    def failure(self, text):
        self.label.re_color(color.text_error)
        self.label.re_text(text)

    def info(self, text):
        self.label.re_color(color.text_info)
        self.label.re_text(text)

class WORK_FRAME:

    def __init__(self, master, sx, sy, update_methode, add_methode):
        self.note = NOTE()
        self.update = update_methode
        self.add = add_methode
        self.sx = sx
        self.sy = sy
        self.children = {}
        self.frame = Frame(master.frame,  height=sy, width=sx, bg=color.surface_1)
        self.frame.pack_propagate(0)
        self.create_structure()
        self.reset()


    def create_structure(self):
        pass


    def resize(self, factor):
        self.frame.configure(width=int(factor * self.sx), height=int(factor * self.sy))
        for item in self.children.values():
            item.resize(factor)

    def load(self, note):
        pass


    def activate(self):
        self.reset()
        self.frame.pack()

    def deactivate(self):
        self.frame.pack_forget()

    def reset(self):
        pass


class button_worker(WORK_FRAME):

    def create_structure(self):
        self.main_keys = {}
        self.sec_keys = {}

        main_label = LABEL("main_key_labal", self, TOP, 800, 30, text.label_main_note, color.color_text_low, color.surface_1)
        self.children.update({"main_key_label" : main_label})

        self.main_key_frame = FRAME("main_key_frame", self, TOP, 800, 30, color.surface_1, anchor=None)
        self.children.update({"main_key_frame" : self.main_key_frame})

        sec_label = LABEL("sec_key_label", self, TOP, 800, 30, text.label_sec_note, color.color_text_low, color.surface_1)
        self.children.update({"sec_key_label" : sec_label})

        self.sec_key_frame = FRAME("main_sec_frame", self, TOP, 800, 30, color.surface_1)
        self.children.update({"sec_key_frame" : self.sec_key_frame})

        self.blank_frame = FRAME("blank_frame", self, TOP, 800, 60, color.surface_1)
        self.lenght_label_frame = FRAME("lenght_label_frame", self, TOP, 800, 30, color.surface_1)

        lenght_label = LABEL("lenght_label", self.lenght_label_frame, LEFT, 100, 30, text.label_lenght_note, color.color_text_low, color.surface_1)
        self.children.update({"blank_frame": self.blank_frame})
        self.children.update({"lenght_label_frame" : self.lenght_label_frame})

        self.lenght_key_frame = FRAME("lenght_key_frame", self, TOP, 800, 30, color.surface_1)
        self.children.update({"lenght_key_frame" : self.lenght_key_frame})


        def temp(value):
            self.main_key_callback(value)

        for i in range(len(keys)):
            key = keys[i]
            button = BUTTON("main_"+key, self.main_key_frame, LEFT, 30, 30, key, color.surface_7, partial(temp, value=i))
            self.main_key_frame.add_obj(button)
            self.main_keys.update({key : button})

        self.pause_button = BUTTON("pause_button", self.main_key_frame, LEFT, 50, 30, text.pause_but_note, color.surface_8,
                                   self.pause_button_callback)
        self.main_key_frame.add_obj(self.pause_button)


        def temp(value):
            self.sec_key_callback(value)

        for i in range(len(keys)):
            key = keys[i]
            button = BUTTON("sec_"+key, self.sec_key_frame, LEFT, 30, 30, key, color.surface_7, partial(temp, value=i))
            self.sec_key_frame.add_obj(button)
            self.sec_keys.update({key : button})

        self.no_sec_button = BUTTON("noe_sec_button", self.sec_key_frame, LEFT, 50, 30, text.no_sec_but, color.surface_7,
                                   partial(temp, value=None))
        self.sec_key_frame.add_obj(self.no_sec_button)
        self.no_sec_button.activate()

        def temp(value):
            self.lenght_callback(value)

        self.lenght_key_frame.add_obj(BUTTON("lenght_1", self.lenght_key_frame, LEFT, 30, 30, "1/1", color.surface_7,
                                                        partial(temp, value=1)))
        self.lenght_key_frame.add_obj( BUTTON("lenght_2", self.lenght_key_frame, LEFT, 30, 30, "1/2", color.surface_7,
                                                         partial(temp, value=2)))
        self.lenght_key_frame.add_obj(BUTTON("lenght_4", self.lenght_key_frame, LEFT, 30, 30, "1/4", color.surface_7,
                                                         partial(temp, value=4)))
        self.lenght_key_frame.add_obj(BUTTON("lenght_8", self.lenght_key_frame, LEFT, 30, 30, "1/8", color.surface_7,
                                                         partial(temp, value=8)))
        self.lenght_key_frame.add_obj(FRAME("blank_button", self.lenght_key_frame, LEFT, 30, 30, color.surface_1))

        self.lenght_key_frame.add_obj(BUTTON("lenght_.", self.lenght_key_frame, LEFT, 30, 30, ".", color.surface_7,
                                                         partial(temp, value=0)))

        self.add_button = BUTTON("add_button", self, RIGHT, 120, 60, text.add_but, color.surface_7, self.add_button_callback)
        self.children.update({"add_button" : self.add_button})

    def load(self, note):
        self.reset()
        self.note = note
        if self.note.point:
            self.lenght_key_frame.get("lenght_.").activate()
        self.lenght_key_frame.get("lenght_" + str(self.note.lenght)).activate()
        if self.note.notes[0] != None:
            self.main_key_frame.get("main_" + keys[self.note.notes[0]]).activate()
        if self.note.notes[1] != None:
            self.no_sec_button.deactivate()
            self.sec_key_frame.get("sec_" + keys[self.note.notes[1]]).activate()
        if not self.note.is_note():
            self.pause_button.re_text(text.pause_but_pause)
        self.push_update()


    def get_note(self):
        return self.note


    def lenght_callback(self, value):
        if value == 0:
            self.note.point = not self.note.point
            if self.note.point:
                self.lenght_key_frame.get("lenght_.").activate()
            else:
                self.lenght_key_frame.get("lenght_.").deactivate()
        else:
            self.lenght_key_frame.get("lenght_1").deactivate()
            self.lenght_key_frame.get("lenght_2").deactivate()
            self.lenght_key_frame.get("lenght_4").deactivate()
            self.lenght_key_frame.get("lenght_8").deactivate()

            self.lenght_key_frame.get("lenght_"+str(value)).activate()
            self.note.lenght = value
        self.push_update()


    def main_key_callback(self, value):
        self.note.notes[0] = value
        for button in self.main_key_frame.get_all().values():
            button.deactivate()
        self.main_key_frame.get("main_"+keys[value]).activate()
        self.push_update()


    def sec_key_callback(self, value):
        if not self.note.is_note():
            return
        self.note.notes[1] = value
        for button in self.sec_key_frame.get_all().values():
            button.deactivate()
        if value == None:
            self.no_sec_button.activate()
        else:
            self.sec_key_frame.get("sec_" + keys[value]).activate()
        self.push_update()


    def pause_button_callback(self):
        if self.note.is_note():
            self.note.set_mode_pause()
        else:
            self.note.set_mode_note()
        if self.note.is_note():
            self.pause_button.re_text(text.pause_but_note)
        else:
            self.pause_button.re_text(text.pause_but_pause)
            for button in self.sec_key_frame.get_all().values():
                button.deactivate()
            self.no_sec_button.activate()
            self.note.notes[1] = None
        self.push_update()


    def add_button_callback(self):
        if self.add(self.note):
            self.reset()
            self.push_update()


    def push_update(self):
        self.update(self.note)



    def reset(self):
        for element in self.main_key_frame.get_all().values():
            element.deactivate()
        for element in self.sec_key_frame.get_all().values():
            element.deactivate()
        self.lenght_key_frame.get("lenght_1").deactivate()
        self.lenght_key_frame.get("lenght_2").deactivate()
        self.lenght_key_frame.get("lenght_4").deactivate()
        self.lenght_key_frame.get("lenght_8").deactivate()
        self.lenght_key_frame.get("lenght_.").deactivate()
        self.pause_button.re_text(text.pause_but_note)
        self.no_sec_button.activate()
        self.note = NOTE()
        self.note.add_note(None)
        self.note.add_note(None)
        self.push_update()



if __name__ == '__main__':
    load_settings()
    MAIN = main()