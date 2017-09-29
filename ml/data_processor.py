from PIL import Image
import numpy as np


def image_convert(file, img_size):

    X = []

    img = Image.open(file)
    img = img.convert('RGB')
    img = img.resize((img_size, img_size))

    in_data = np.asarray(img)

    X.append(in_data)

    X = np.array(X)

    return X
