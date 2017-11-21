import model as ml
import data_processor as dp
from flask import Flask, make_response, jsonify, request
import os
import base64

categories = dp.get_plants_name('ja')
classes = len(categories)
image_size = 120

api = Flask(__name__)


@api.route('/get_plant', methods=['POST'])
def main():

    post_file = request.data

    dir_name = 'temp_img'
    file_name = dp.make_random_str(5)+'.png'
    file_path = dir_name + '/' + file_name

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    with open(file_path, 'wb') as f:
        f.write(base64.decodebytes(post_file))

    read_file = open(file_path, 'rb')

    X = dp.image_convert(read_file, image_size)

    read_file.close()
    os.remove(file_path)

    model = ml.build_model(X.shape[1:], classes)
    model.load_weights(os.path.join(os.path.dirname(__file__), 'store/model.hdf5'))

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
