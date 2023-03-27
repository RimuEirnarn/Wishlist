from os import environ
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

load_dotenv(join(dirname(__file__), '.env'))

client = MongoClient(environ.get("MONGODB_URI"))
database = client[environ.get("DB_NAME")]
wishlist = database.wishlist

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    content = request.form['content']
    bucket_id = wishlist.count_documents({})+1
    wishlist.insert_one({
        'bucket_id': bucket_id,
        'content': content,
        'isDone': False
    })
    return jsonify({'status': 'success', 'message': "Wishlist created", "bucket_id": bucket_id})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    bucket_id = int(request.form['bucket_id'])
    wishlist.update_one({
        'bucket_id': bucket_id
    }, {
        '$set': {
            'isDone': True
        }
    })
    return jsonify({'status': "success", "message": "Done staging"})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets = list(wishlist.find({}, {'_id': False}))
    return jsonify({'status': "success", 'message': "Fetch buckets", "buckets": buckets})


@app.route("/delete", methods=["POST"])
def bucket_delete():
    bucket_id = int(request.form['bucket_id'])
    wishlist.delete_one({
        'bucket_id': bucket_id
    })
    return jsonify({"status": "success", "message": "Wishlist deleted"})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
