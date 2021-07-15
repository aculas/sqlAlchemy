from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)
# this needs to be configured before the db and it has to connect to a database that exists
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "1234567"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def list_pets():
    """Shows list of all pets in db"""
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)


@app.route("/", methods=["POST"])
def create_pet():
    name = request.form["name"]
    species = request.form["species"]
    hunger = request.form["hunger"]
    hunger = int(hunger) if hunger else None

    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()
    # do not render template as it duplicates the pet
    # return "YOU SENT YOUR DATA"
    return redirect(f"/{new_pet.id}")


@app.route("/<int:pet_id>")
def show_pet(pet_id):
    """Show details about a single pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('details.html', pet=pet)


# This will show the pet name when their id is used with \(pet_id)
#    return f"<h1>{pet.name}</h1>"

@app.route("/species/<species_id>")
def show_pets_by_species(species_id):
    pets = Pet.get_by_species(species_id)
    return render_template('species.html', pets=pets, species=species_id)
