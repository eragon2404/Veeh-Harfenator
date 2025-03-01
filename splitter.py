from PIL import Image

def split(img):
    """
    Splits the image vertically into two images with A4 format
    :param img: Image object
    :return: Tuple of Image objects
    """
    size = (img.width, img.height)
    a4_relational = 1.4142

    a4_size = (size[0], int(size[0] / a4_relational))

    img1 = img.crop((0, 0, size[0], a4_size[1]))
    # Pads the image to fit A4 format
    img2 = Image.new("1", a4_size, 1)
    img2.paste(img.crop((0, a4_size[1], size[0], size[1])), (0, 0))

    return img1, img2