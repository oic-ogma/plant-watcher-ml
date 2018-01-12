import os
import json
import string
import random
import numpy as np
from PIL import Image

def image_convert(file, img_size):

    X = []

    img = Image.open(file)
    img = crop_center(img)
    img = img.convert('RGB')
    img = img.resize((img_size, img_size))

    in_data = np.asarray(img)

    X.append(in_data)

    X = np.array(X)

    X = X.astype('float') / 256

    return X


# 上位num件の予測結果のkeyを降順で返す
def sort_predict_key(data, num):

    sort_data_key = np.argsort(data)[-1::-1]
    y = sort_data_key[:num]

    return y


def get_plants_name(lang):

    f = open(os.path.join(os.path.dirname(__file__), 'store/plant.json'), 'r', encoding='utf-8')
    json_data = json.load(f)
    categories = json_data[lang]

    return categories


def make_random_str(num):

    chars = string.ascii_letters + string.digits
    s = ''
    random_str = s.join([random.choice(chars) for i in range(num)])

    return random_str


def crop_center(file):

    img = file
    img_width, img_height = img.size

    return img.crop(((img_width - img_width) // 2, 
                    (img_height - img_width) // 2, 
                    (img_width + img_width) // 2, 
                    (img_height + img_width) // 2))
