from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
from scrape_mars import scrape as scrape_data

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape")


@app.route('/')
def index():
    # data =  mongo.db.mars.find().sort({'_id': -1}).limit(1)
    data =  mongo.db.mars.find_one()

    print(data)
    
    data['title'] = 'Mission to Mars'
    return render_template('index.html', **data)


@app.route('/scrape')
def scrape():

    data = scrape_data()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.insert_one(data)

    return render_template('index.html', **{"title": "Mission to Mars"})
