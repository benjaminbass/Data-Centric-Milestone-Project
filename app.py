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
@app.route('/getcharacters')
def get_characters():
    characters = list(mongo.db.characterInfo.find())
    classes = list(mongo.db.classes.find())
    races = list(mongo.db.races.find())
    return render_template(
        "characters.html",
        characters=characters,
        classes=classes,
        races=races)


@app.route('/addcharacter')
def add_character():
    classes = list(mongo.db.classes.find())
    races = list(mongo.db.races.find())
    return render_template(
        'addcharacter.html',
        classes=classes,
        races=races)


@app.route('/insertcharacter', methods=['POST'])
def insert_character():
    characterInfo = mongo.db.characterInfo
    characterInfo.insert_one(request.form.to_dict())
    return redirect(url_for('get_characters'))


@app.route('/editcharacter/<character_id>')
def edit_character(character_id):
    classes = list(mongo.db.classes.find())
    races = list(mongo.db.races.find())
    character = mongo.db.characterInfo.find_one({"_id": ObjectId(character_id)})
    return render_template('editcharacter.html',
        character=character,
        classes=classes,
        races=races)


@app.route('/updatecharacter/<character_id>', methods=['POST'])
def update_character(character_id):
    character = mongo.db.characterInfo
    character.update({'_id': ObjectId(character_id)},
    {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'strength': request.form.get('strength'),
        'dexterity': request.form.get('dexterity'),
        'constitution': request.form.get('constitution'),
        'intelligence': request.form.get('intelligence'),
        'wisdom': request.form.get('wisdom'),
        'charisma': request.form.get('charisma'),
        'is_dead': request.form.get('is_dead'),
        'race-name': request.form.get('race-name'),
        'class-name': request.form.get('class-name')
    })
    return redirect(url_for('get_characters'))


@app.route('/delete_character/<character_id>')
def delete_character(character_id):
    mongo.db.characterInfo.remove({'_id': ObjectId(character_id)})
    return redirect(url_for('get_characters'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
