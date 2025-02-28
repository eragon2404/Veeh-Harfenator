
class DARK_THEME:
    surface_1 = "#151515"
    surface_2 = "#202020"
    surface_3 = "#303030"
    surface_4 = "#353535"
    surface_5 = "#404040"
    surface_6 = "#454545"
    surface_7 = "#353535"
    surface_8 = "#606060"
    color_active = "#5050BB"
    color_click = "#7070CC"

    color_text_low = "#999999"
    color_text_high = "#ffffff"

    text_success = "#00aa00"
    text_error = "#cc8800"
    text_neutral = "#888888"
    text_info = "#4444cc"

class LIGHT_THEME:
    surface_1 = "#ffffff"
    surface_2 = "#ffffff"
    surface_3 = "#ffffff"
    surface_4 = "#ffffff"
    surface_5 = "#ffffff"
    surface_6 = "#ffffff"
    surface_7 = "#bbbbbb"
    surface_8 = "#909090"
    color_active = "#70FF70"
    color_click = "#80DD80"

    color_text_low = "#333333"
    color_text_high = "#000000"

    text_success = "#00aa00"
    text_error = "#ffaa00"
    text_neutral = "#888888"
    text_info = "#0000ff"


def load_theme(theme):
    themes = {
        "light" : LIGHT_THEME,
        "dark" : DARK_THEME
              }
    return themes[theme]()