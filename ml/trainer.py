from keras.utils import np_utils
import numpy as np
import model as ml


root_dir = './store/images'
categories = ['asagao', 'cosmos', 'himawari', 'margaret', 'pansy']
classes = len(categories)
image_size = 120


def main():

    X_train, X_test, y_train, y_test = np.load('./store/plants.npy')

    # データを正規化
    X_train = X_train.astype('float') / 256
    X_test = X_test.astype('float') / 256
    y_train = np_utils.to_categorical(y_train, classes)
    y_test = np_utils.to_categorical(y_test, classes)

    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)


# モデルを訓練する
def model_train(X, y):

    model = ml.build_model(X.shape[1:], classes)
    model.fit(X, y, batch_size=32, epochs=30)

    # モデルを保存
    hdf5_file = './store/model.hdf5'
    model.save_weights(hdf5_file)

    return model


# モデルを評価する
def model_eval(model, X, y):

    score = model.evaluate(X, y)

    print('loss = ', score[0])
    print('accuracy = ', score[1])


if __name__ == '__main__':
    main()
