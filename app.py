from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPet, EditPet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet-shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'helloimasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    pets = Pet.query.all()
    return render_template('home-page.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPet()
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo_url = form.url.data or None
        age = form.age.data
        notes = form.notes.data
        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{name} was added")
        return redirect('/')
    else:
        return render_template("add-pet-form", form=form)
    
@app.route('/pet/<int:id>')
def display_pet(id):
    pet = Pet.query.get_or_404(id)
    return render_template('display-pet.html', pet=pet)

@app.route('/pet/<int:id>/edit', methods=['GET', 'POST'])
def edit_pet(id):
    pet = Pet.query.get_or_404(id)
    form = EditPet()
    if form.validate_on_submit():
        pet.photo_url = form.url.data or None
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect(f'/pet/{id}')
    else:
        return render_template('edit-pet.html', pet=pet, form=form)
    
@app.route('/delete/<int:id>')
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return redirect('/')