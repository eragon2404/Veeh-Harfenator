from PIL import Image, ImageDraw, ImageFont
from song import SONG

size = 2000
max_note = 24
border_x = 1
border_y = 50
max_notes_per_site = 10

sizes = {1: 20, 2: 15, 4: 15, 8: 10}

lng = None

def plott(song, grid=False):
    """
    Plots the song
    :param song: Song object
    :param grid: Show grid
    """
    links = prepare_links(song.get_notes())
    sites = calc_notes(song)
    index = 0
    for site in sites:
        plott_site(site, grid, links, index)
        index += len(site)

def plott_site(entrys, grid, links, start_index):
    """
    Plots a site
    :param entrys: List of notes
    :param grid: Show grid
    """
    image = Image.new("1", (size, size), 1)
    draw = ImageDraw.Draw(image)

    # Grid
    if grid:
        draw_grid(draw, len(entrys))

    # Links
    for link in links:
        y1 = None
        y2 = None
        if link[0] >= start_index and link[0] < start_index + len(entrys):
            y1 = calc_y(len(entrys), link[0] - start_index)
            draw.line(((link[2], y1), (link[4], y1)), width=3)
            # arrow head
            sign = 1 if link[2] > link[4] else -1
            note = entrys[link[0] - start_index]
            buff = sizes[note.lenght]
            buff *= 1.5 if note.mode == 0 else 0.75

            draw.polygon((
                (link[2] - sign * buff, y1),
                (link[2] - sign * (buff +20), y1 - 10),
                (link[2] - sign * (buff +15), y1),
                (link[2] - sign * (buff +20), y1 + 10)
            ), fill=0)

        if link[1] >= start_index and link[1] < start_index + len(entrys):
            y2 = calc_y(len(entrys), link[1] - start_index)
            draw.line(((link[4], y2), (link[3], y2)), width=3)

        if y1 != None or y2 != None:
            if y1 == None:
                y1 = 0
            if y2 == None:
                y2 = size
            draw.line(((link[4], y1), (link[4], y2)), width=3)


    # Vert lines
    for ey in range(len(entrys) - 1):
        n1 = entrys[ey]
        n2 = entrys[ey + 1]
        y1 = calc_y(len(entrys), ey)
        y2 = calc_y(len(entrys), ey + 1)
        x1 = calc_x(n1.notes[0])
        x2 = calc_x(n2.notes[0])
        draw.line(((x1, y1), (x2, y2)), width=5)

    # Notes and horizontal lines
    for ey in range(len(entrys)):
        notes = entrys[ey].notes
        y = calc_y(len(entrys), ey)
        for i in range(len(notes) - 1):
            ex1 = notes[i]
            ex2 = notes[i + 1]
            if ex1 == None or ex2 == None:
                continue
            draw.line(((calc_x(ex1), y), (calc_x(ex2), y)), width=3)
        draw_note(draw, entrys[ey], y)
    image.show()


def prepare_links(notes):
    """
    Prepares the links
    :param notes: List of notes

    """
    links = []
    for i, note in enumerate(notes):
        for link in note.links:
            if link != None:
                for j in range(len(links)):
                    if links[j][0] == link:
                        links[j][1].append(i)
                        break
                else:
                    links.append([link, [i]])
    dependencies = []
    for i in range(len(links)):
        dependencies.append([])
        for j in range(len(links)):
            if i == j:
                continue
            if links[j][1][0] >= links[i][1][0] and links[j][1][0] <= links[i][1][1]:
                # link i upper is within link j
                dependencies[i].append(j)
    # sort links by dependencies
    result = []
    while len(result) < len(links):
        lowest = min([len(dependencies[i]) for i in range(len(dependencies))])
        for i in range(len(links)):
            if i in result:
                continue
            if len(dependencies[i]) == lowest:
                result.append(i)
                for j in range(len(dependencies)):
                    if i in dependencies[j]:
                        dependencies[j].remove(i)
                break

    final_links = []
    # form: [(i_start, i_end, x_start, x_end, x_out)]
    extremes = []
    for note in notes:
        positions = [calc_x(i) for i in note.notes if i != None]
        extremes.append([min(positions), max(positions)])

    BUFFER = 15
    for i in result:
        link = links[i][1]
        local_min = min([extremes[i][0] for i in range(link[0], link[1] + 1)])
        local_max = max([extremes[i][1] for i in range(link[0], link[1] + 1)])
        # choose left or right
        if local_min >= size - local_max:
            # left
            x_start = min([calc_x(note) for note in notes[link[0]].notes if note != None])
            x_end = min([calc_x(note) for note in notes[link[1]].notes if note != None])
            x_out = min(local_min - BUFFER, x_start - BUFFER*5, x_end - BUFFER*5)
            if x_out < BUFFER:
                x_out = BUFFER
            for e in range(link[0], link[1] + 1):
                extremes[e][0] = x_out
        else:
            # right
            x_start = max([calc_x(note) for note in notes[link[0]].notes if note != None])
            x_end = max([calc_x(note) for note in notes[link[1]].notes if note != None])
            x_out = max(local_max + BUFFER, x_start + BUFFER*5, x_end + BUFFER*5)
            if x_out > size - BUFFER:
                x_out = size - BUFFER
            for e in range(link[0], link[1] + 1):
                extremes[e][1] = x_out
        final_links.append((link[0], link[1], x_start, x_end, x_out))

    return final_links



def draw_note(draw, note, y):
    """
    Draws a note
    :param draw: draw object
    :param note: Note
    :param y: y position
    """


    size = sizes[note.lenght]
    if note.lenght == 1 or note.lenght == 2:
        hollow = True
    else:
        hollow = False

    for n in note.notes:
        if n == None:
            continue
        x = calc_x(n)
        if note.mode == 0:
            draw_ellipse(draw, x, y, size, hollow)
        else:
            draw_rect(draw, x, y, size, hollow)

        if note.point:
            draw.circle((x+size*1.5, y+size), 5, fill=0)


def draw_ellipse(draw, x, y, size, hollow=False):
    """
    Draws an ellipse
    :param draw: draw object
    :param x: x position
    :param y: y position
    :param size: size
    :param hollow: hollow
    """
    stretch = 1.5
    if hollow:
        draw.ellipse(((x - size*stretch, y - size), (x + size*stretch, y + size)), outline=0, fill=1, width=5)
    else:
        draw.ellipse(((x - size*stretch, y - size), (x + size*stretch, y + size)), fill=0)

def draw_rect(draw, x, y, size, hollow=False):
    """
    Draws a rectangle
    :param draw: draw object
    :param x: x position
    :param y: y position
    :param size: size
    :param hollow: hollow
    """
    stretch = 0.75
    if hollow:
        draw.rectangle(((x - size*stretch, y - size), (x + size*stretch, y + size)), outline=0, fill=1, width=5)
    else:
        draw.rectangle(((x - size*stretch, y - size), (x + size*stretch, y + size)), fill=0)

def draw_grid(draw, count_y):
    """
    Draws the grid
    :param draw: draw object
    :param count_y: count of y lines
    """
    font = ImageFont.truetype(font="arial.ttf", size=30)
    for i in range(max_note + 1):
        x = calc_x(i)
        draw.line(((x, 0), (x, size)))
    draw.rectangle(((0, 25), (size, 60)), fill="white")
    for i in range(max_note + 1):
        x = calc_x(i)
        text_size = draw.textlength(lng.keys[i], font=font)
        draw.text((x - text_size/2, 25), lng.keys[i], font=font)
    for i in range(count_y):
        y = calc_y(count_y, i)
        draw.line(((0, y), (size, y)))



def calc_notes(song):
    """
    Splits the notes into sites
    :param song: Song
    :return: List of sites
    """
    notes = song.get_notes()
    site_count = int(len(notes) / max_notes_per_site) + 1
    result = [None for _ in range(site_count)]
    for i in range(len(result)):
        count = int(len(notes)/site_count)
        site_count -= 1
        result[i] = notes[:count]
        del(notes[:count])
    return result


def calc_x(index):
    return int(size / (max_note + border_x * 2) * (border_x + index))

def calc_y(lenght, index):
    return int((size - 2 * border_y) / (lenght + 1) * (index + 1) + border_y)


class test:
    def get_notes(self):
        return [i for i in range(153)]


if __name__ == '__main__':
    print(plott(test()))