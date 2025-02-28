MODE_NOTE = 0
MODE_PAUSE = 1

lng = None

class NOTE:

    def __init__(self):
        self.notes = []
        self.mode = MODE_NOTE
        self.lenght = None
        self.point = False
        self.links = []
        self.index = None

    def add_note(self, note):
        self.notes.append(note)

    def remove(self, note):
        self.notes.remove(note)

    def set_mode_note(self):
        self.mode = MODE_NOTE

    def set_mode_pause(self):
        self.mode = MODE_PAUSE

    def set_lenght(self, lenght, point):
        self.lenght = lenght
        self.point = point

    def set_index(self, index):
        self.index = index

    def add_link(self, link):
        self.links.append(link)

    def remove_link(self, link):
        self.links.remove(link)

    def is_linked(self, link):
        return link in self.links

    def is_note(self):
        return self.mode == MODE_NOTE

    def verify(self):
        n_notes = 0
        for note in self.notes:
            if note != None:
                n_notes += 1
            if self.notes.count(note) > 1:
                return False

        if self.mode == MODE_PAUSE and n_notes > 1:
            return False

        return n_notes > 0 and self.lenght != None

    def to_csv(self):
        final = ""
        if self.mode == MODE_NOTE:
            final += "N"
        else:
            final += "P"
        final += ";" + str(self.lenght)
        if self.point:
            final += ";1;"
        else:
            final += ";0;"
        final += ",".join([str(note) for note in self.notes if note != None]) + ";"
        final += ",".join([str(link) for link in self.links])
        return final

    def from_csv(self, csv):
        data = csv.split(";")
        if data[0] == "N":
            self.mode = MODE_NOTE
        else:
            self.mode = MODE_PAUSE
        self.lenght = int(data[1])
        if data[2] == "1":
            self.point = True
        else:
            self.point = False
        self.notes = [int(note) if note != "" else None for note in data[3].split(",")]
        self.links = [int(link) for link in data[4].split(",") if link != ""]

    def to_text(self):
        final = ""
        if self.mode == MODE_NOTE:
            final += lng.pause_but_note + " "
            for note in self.notes:
                if note != None:
                    final += lng.keys[note] + " / "
                else:
                    final += "? / "
            if len(self.notes) > 0:
                final = final[:-2]
        else:
            final += lng.pause_but_pause + " "
            if len(self.notes) != 0:
                final += lng.text_at + " "
                if len(self.notes) == 0:
                    final += "?"
                elif self.notes[0] == None:
                    final += "?"
                else:
                    final += lng.keys[self.notes[0]]

        if self.lenght != None:
            final += " " + lng.text_of_lenght + " 1/" + str(self.lenght)
            if self.point:
                final += "."
        return final

    def report_problem(self):
        n_notes = 0
        for note in self.notes:
            if note != None:
                n_notes += 1
            if self.notes.count(note) > 1 and note != None:
                return lng.prob_equal_note

        if self.mode == MODE_PAUSE and n_notes > 1:
            return lng.prob_many_pause

        if n_notes == 0:
            return lng.prob_note_ammount
        if self.lenght == None:
            return lng.prob_no_lenght

    def __str__(self):
        final = "[" + str(self.index) + "]: "
        if self.mode == MODE_NOTE:
            final += "N"
        else:
            final += "P"
        final += " (1/" + str(self.lenght)
        if self.point:
            final += "."
        final += ") "
        for note in self.notes:
            if note != None:
                final += lng.keys[note] + " | "
        final = final[:-2]
        return final


