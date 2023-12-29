from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length

class AddPet(FlaskForm):
    pet_name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Pet Species", choices=[('cat', 'Cat'), ('porcupine', 'Porcupine'), ('dog', 'Dog')])
    url = StringField("Photo URL", validators=[URL(), Optional()])
    age = IntegerField("Pet Age", validators=[NumberRange(min=0, max=30), Optional()])
    notes = TextAreaField("* Notes", validators=[Optional(), Length(min=10)])

class EditPet(FlaskForm):
    url = StringField("Photo URL", validators=[URL(), Optional()])
    notes = TextAreaField("* Notes", validators=[Optional(), Length(min=10)])
    available = BooleanField('Still Available?') 