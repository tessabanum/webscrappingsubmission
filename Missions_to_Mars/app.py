from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape")


@app.route('/')
def index():
    return """
    <html>
        <head></head>
        <body>
            <h1>We are getting close !!!</h1>
        </body>
    </html>
    """


@app.route('/scrape')
def scrape():

    data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection['mars'].update({}, data, upsert=True)

    return data
