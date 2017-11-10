from keras.utils import np_utils
from keras.callbacks import TensorBoard
import data_processor as dp
import numpy as np
import model as ml
import os


categories = dp.get_plants_name()
classes = len(categories)


def main():

    X_train, X_test, y_train, y_test = np.load('./store/plants.npy')

    # データを正規化
    X_train = X_train.astype('float') / 256
    X_test = X_test.astype('float') / 256
    y_train = np_utils.to_categorical(y_train, classes)
    y_test = np_utils.to_categorical(y_test, classes)

    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)
    model_save(model)


def model_train(X, y):

    model = ml.build_model(X.shape[1:], classes)

    path = './store/tb_logs'

    if not os.path.exists(path):
        os.makedirs(path)

    tb = TensorBoard(log_dir=path)

    model.fit(X, y, batch_size=32, epochs=30, callbacks=[tb])

    return model


def model_eval(model, X, y):

    score = model.evaluate(X, y)

    print('loss = ', score[0])
    print('accuracy = ', score[1])


def model_save(model):

    hdf5_file = './store/model.hdf5'

    if not os.path.exists(hdf5_file):
        model.save_weights(hdf5_file)
        print("Saved.")


if __name__ == '__main__':
    main()
