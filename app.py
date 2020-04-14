import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Character'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_characters')
def get_characters():
    return render_template("characters.html", characters=mongo.db.characterInfo.find(), classes=mongo.db.classes.find(), races=mongo.db.races.find())


@app.route('/addcharacter')
def add_character():
    classes = list(mongo.db.classes.find())
    races = list(mongo.db.races.find())
    return render_template(
        'addcharacter.html',
        classes=classes,
        races=races)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
