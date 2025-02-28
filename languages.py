class ENGLSIH:
    keys = ["G", "G#", "A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G2", "G#2", "A2", "Bb2", "B2",
            "C2", "C#2", "D2", "Eb2", "E2", "F2", "F#2", "G3"]

    label_main_note = "Main note:"
    label_sec_note = "Secondary note:"
    label_lenght_note = "Lenght:"
    label_link = "Link:"

    pause_but_note = "note"
    pause_but_pause = "pause"

    no_sec_but = "none"
    add_but = "-> ADD"
    link_but_add = "-> Add Link"
    link_but_rem = "<- Remove Link"

    text_at = "at"
    text_with = "with"
    text_of_lenght = "of lenght"
    text_from = "from"
    text_to = "to"

    delete = "delete"
    load = "load"
    insert = "insert above"

    added = "added"
    inserted = "inserted above"
    loaded = "loaded into editor"
    deleted = "deleted"
    removed_link = "Removed link"
    added_link = "Added Link"
    link_done = "Link complete"

    prob_note_ammount = "Please select at least one note"
    prob_equal_note = "You cannot select the same note twice"
    prob_many_pause = "Please select only one note for a pause"
    prob_no_lenght = "Please select a lenght"
    prob_no_selection = "Please select an item from the list to execute this action"
    prob_no_item = "The list must contain at least one item for this action to work"
    prob_many_link = "This link is already connected to two items"


class GERMAN:
    keys = ["G", "G#", "A", "Hb", "H", "C", "C#", "D", "Eb", "E", "F", "F#", "G2", "G#2", "A2", "Hb2", "H2",
            "C2", "C#2", "D2", "Eb2", "E2", "F2", "F#2", "G3"]

    label_main_note = "Hauptnote:"
    label_sec_note = "Beinote:"
    label_lenght_note = "Länge:"
    label_link = "Verbindung:"

    pause_but_note = "Note"
    pause_but_pause = "Pause"

    no_sec_but = "Nichts"
    add_but = "-> Hinzufügen"
    link_but_add = "-> Verbinden"
    link_but_rem = "<- Entfernen"

    text_at = "auf"
    text_with = "mit"
    text_of_lenght = "der Länge"
    text_from = "von"
    text_to = "to"

    delete = "Löschen"
    load = "Laden"
    insert = "Oben einfügen"

    added = "hinzugefügt"
    inserted = "eingefügt über"
    loaded = "in den Editor geladen"
    deleted = "gelöscht"
    removed_link = "Verbindung entfernt:"
    added_link = "Verbindung hinzugefügt:"
    link_done = "Verbindung vollständig"

    prob_note_ammount = "Bitte minedestens eine Note wählen"
    prob_equal_note = "Die gleiche Note kann nicht zwei mal ausgewählt werden"
    prob_many_pause = "Bitte nur einen Notenwert für die Pause wählen"
    prob_no_lenght = "Bitte wählen sie eine Länge"
    prob_no_selection = "Bitte wählen sie für diese Aktion einen Eintrag aus der Liste"
    prob_no_item = "Die Liste muss für diese Aktion mindestens einen Eintrag haben"
    prob_many_link = "Diese Verbindung ist bereits mit zwei Einträgen verbunden"



def load_language(language):
    global text
    languages = {
        "english" : ENGLSIH,
        "german" : GERMAN
    }
    return languages[language]()