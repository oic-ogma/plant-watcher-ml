import model as ml
import data_processor as dp
from flask import Flask, make_response, jsonify, request
import os

categories = ['asagao', 'cosmos', 'himawari', 'margaret', 'pansy']
classes = len(categories)
image_size = 120

api = Flask(__name__)


@api.route('/get_plant', methods=['POST'])
def main():

    post_file = request.files['image']

    X = dp.image_convert(post_file, image_size)

    model = ml.build_model(X.shape[1:], classes)

    if not os.path.exists('./store/model.hdf5'):
        # dockerでの実行に必要(実行時のカレントディレクトリがずれてるため)
        model.load_weights('/home/ml/store/model.hdf5')
    else:
        model.load_weights('./store/model.hdf5')

    predict = model.predict_proba(X)
    predict_key = dp.sort_predict_key(predict[0], 3)

    plants = []

    for y in predict_key:
        plants.append(categories[y])

    result = {
        "data": {
            "plant": plants
        }
    }

    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):

    return make_response(jsonify({'error': 'Not found'}), 404)


@api.errorhandler(400)
def bad_request(error):

    return make_response(jsonify({'error': 'Nothing post data'}), 400)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8000)
