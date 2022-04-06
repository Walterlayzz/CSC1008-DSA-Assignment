from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, widgets
from wtforms.validators import InputRequired, length, ValidationError
from flask_bcrypt import Bcrypt
import folium
import osmnx as os
from geopy.geocoders import Nominatim

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SECRET_KEY"] = "secret"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("Username already exists!")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class checkBoxField(SelectField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class rideInput(FlaskForm):
    addressFrom = StringField(validators=[InputRequired()], render_kw={"placeholder": "From"})
    destination = StringField(validators=[InputRequired()], render_kw={"placeholder": "Destination"})
    shared = checkBoxField("Label", choices=[("Shared Ride?")])
    submit = SubmitField("Book")

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.type == "Rider":
                    return redirect(url_for("dashboard"))
                elif user.type == "Driver":
                    return redirect(url_for("d_dashboard"))

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, type="")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = rideInput()
    geolocator = Nominatim(user_agent="my_request")
    # Display map after successful login
    start_coords = (1.2946226, 103.8060366) #Currently is queenstown MRT
    f_map = folium.Map(location=start_coords, zoom_start=16) #Shows map with location as queenstown MRT
    # After user has submitted address info
    if form.is_submitted:
        if form.addressFrom.data and form.destination.data is not None:
            # Geocode to convert address into coords
            location = geolocator.geocode(form.addressFrom.data + ", Singapore")
            start_coords = (location.latitude, location.longitude)
            dest = geolocator.geocode(form.destination.data + ", Singapore")
            end_coords = (dest.latitude, dest.longitude)

            # Fit to and from on map
            f_map.fit_bounds([start_coords, end_coords], padding=[15,15])
            folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
            folium.Marker(location=end_coords, popup="<b>Destination</b>", icon=folium.Icon(color="red") ).add_to(f_map)
    #Coordinates for the path
    # coords = [(1.2946226, 103.8060366), (1.29589,103.80513), (1.29679, 103.80449), (1.29747,103.80371), (1.29682,103.80314), (1.29632, 103.80348)]
    # f_map = folium.Map(location=start_coords, zoom_start=15)
    # folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
    # folium.Marker(location=end_coords, popup="<b>Destination</>", icon=folium.Icon(color="red")).add_to(f_map)
    # # Creating a path based on the coords provided
    # folium.PolyLine(coords, color="red", weight=3).add_to(f_map)
    return render_template("index.html",  f_map=f_map._repr_html_(), form=form)


@app.route("/d_dashboard", methods=["GET", "POST"])
@login_required
def d_dashboard():
    form = rideInput()
    geolocator = Nominatim(user_agent="my_request")
    # Display map after successful login
    start_coords = (1.2946226, 103.8060366) #Currently is queenstown MRT
    f_map = folium.Map(location=start_coords, zoom_start=16) #Shows map with location as queenstown MRT
    # After user has submitted address info
    if form.is_submitted:
        if form.addressFrom.data and form.destination.data is not None:
            # Geocode to convert address into coords
            location = geolocator.geocode(form.addressFrom.data + ", Singapore")
            start_coords = (location.latitude, location.longitude)
            dest = geolocator.geocode(form.destination.data + ", Singapore")
            end_coords = (dest.latitude, dest.longitude)

            # Fit to and from on map
            f_map.fit_bounds([start_coords, end_coords], padding=[15,15])
            folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
            folium.Marker(location=end_coords, popup="<b>Destination</b>", icon=folium.Icon(color="red") ).add_to(f_map)
    #Coordinates for the path
    # coords = [(1.2946226, 103.8060366), (1.29589,103.80513), (1.29679, 103.80449), (1.29747,103.80371), (1.29682,103.80314), (1.29632, 103.80348)]
    # f_map = folium.Map(location=start_coords, zoom_start=15)
    # folium.Marker(location=start_coords, popup="<b>You are here!</b>" ).add_to(f_map)
    # folium.Marker(location=end_coords, popup="<b>Destination</>", icon=folium.Icon(color="red")).add_to(f_map)
    # # Creating a path based on the coords provided
    # folium.PolyLine(coords, color="red", weight=3).add_to(f_map)
    return render_template("d_index.html",  f_map=f_map._repr_html_(), form=form)

if __name__ == "__main__":
    app.run()
