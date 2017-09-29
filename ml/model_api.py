import model as ml
import data_processor as dp
from flask import Flask, make_response, jsonify, request

categories = ['asagao', 'cosmos', 'himawari', 'margaret', 'pansy']
classes = len(categories)
image_size = 120

api = Flask(__name__)


@api.route('/get_plant', methods=['POST'])
def main():

    file = request.files['image']

    X = dp.image_convert(file, image_size)

    model = ml.build_model(X.shape[1:], classes)
    model.load_weights('./store/model.hdf5')

    predict = model.predict(X)

    plants = []

    for i, p in enumerate(predict):
        y = p.argmax()

        plants.append(categories[y])

    result = {
        "data": {
            "plant": plants[0]
        }
    }

    return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):

    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api.run(host='127.0.0.1', port=3000)
