import glob
import data_processor as dp
import numpy as np
from PIL import Image
from sklearn import model_selection

root_dir = "./store/images"
categories = dp.get_plants_name('en')
image_size = 120

X = []  # 画像データ
Y = []  # ラベルデータ

for index, category in enumerate(categories):

    image_dir = root_dir + "/" + category
    files = glob.glob(image_dir + "/*.jpg")

    print("- " + category + "を処理中")

    for i, f in enumerate(files):
        image = Image.open(f)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))

        data = np.asarray(image)

        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

# 学習データとテストデータを分ける
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)

np.save("./store/plants.npy", xy)

print("done.", len(Y))
