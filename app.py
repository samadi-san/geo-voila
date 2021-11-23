# from flask import Flask
# from cluster_price_range import kmean_cluster

# app = Flask(__name__)

# @app.route("/api/flask/cluster_price_range/<int:5>", methods=["GET"])
# def flask(id):
#     return kmean_cluster()
#     # return cluster_price_range.cluster_price_range(5)


# if __name__ == "__main__":
#     app.run(host= '0.0.0.0')
    
from flask import Flask
from flask import send_from_directory, request
from cluster_price_range import kmean_cluster, price_range,get_location, price_priority_map
import json

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_object('config')

@app.route('/hello', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/map', methods=['GET'])
def get_price_map():
    folder = app.config['IMAGE_FOLDER']
    
    lat = request.args.get('lat')
    long = request.args.get('long')
    
    return json.dumps({'results':  request.url_root + price_priority_map(folder, (lat, long))})

@app.route('/cluster', methods=['GET', 'POST'])
def get_cluster():
    return json.dumps({'results':  list(kmean_cluster())})



@app.route('/price_range', methods=['GET'])
def show_prices_range():
    return json.dumps({'results':  request.url_root + price_range()})

@app.route('/img/<path:filename>') 
def send_file(filename): 
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/location', methods = ['GET'])
def new_location():
    return json.dumps({'results':  get_location()})

# @app.route('/map', methods=['GET'])
# def price_priority_map():
#     print('/map')
#     return json.dumps({'results':  request.url_root + price_priority_map()})


if __name__ == '__main__':
    app.run(host='geo-spatial-data-analysis.herokuapp.com')