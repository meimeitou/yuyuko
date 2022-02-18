
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField,\
    FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *
from app.model import db
from flask_bootstrap import SwitchField
from flask import Blueprint,render_template

app = Blueprint(
    'home',
    __name__,
    template_folder='../templates',
    static_folder='../static')

class ExampleForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    date = DateField(
        description="We'll never share your email with anyone else.")  # add help text with `description`
    # add HTML attribute with `render_kw`
    datetime = DateTimeField(
        render_kw={'placeholder': 'this is a placeholder'})
    datetime_local = DateTimeLocalField()
    time = TimeField()
    floating = FloatField()
    integer = IntegerField()
    decimal_slider = DecimalRangeField()
    integer_slider = IntegerRangeField(render_kw={'min': '0', 'max': '4'})
    email = EmailField()
    url = URLField()
    search = SearchField()
    telephone = TelField()
    image = FileField(render_kw={'class': 'my-class'},
                      validators=[Regexp('.+\.jpg$')])  # add your class
    option = RadioField(
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select = SelectField(
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select_multiple = SelectMultipleField(
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    bio = TextAreaField()
    title = StringField()
    secret = PasswordField()
    remember = BooleanField('Remember me')
    submit = SubmitField()


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    confirm = SwitchField('Confirmation')
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code/Exchange')
    number = StringField('Number')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()


class ContactForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
    emails = FieldList(StringField("Email"), min_entries=3)
    im_accounts = FieldList(FormField(IMForm), min_entries=2)


@app.route('/')
def index():
    return render_template('index.html')
