import requests
from flask import render_template, Flask, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from werkzeug.utils import redirect
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL

from cafeApiManager import ApiManager

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe city location ', validators=[DataRequired()])
    country = StringField('Cafe country location ', validators=[DataRequired()])
    map_url = StringField('Cafe map link', validators=[DataRequired(), URL(message='Must be a valid URL')])
    img_url = StringField('Cafe image link', validators=[DataRequired(), URL(message='Must be a valid URL')])
    seats = StringField('Cafe number of seats e.g. +20', validators=[DataRequired()])
    has_toilet = SelectField("has toilet", choices=["true", "false"], validators=[DataRequired()])
    has_wifi = SelectField("has wifi", choices=["true", "false"], validators=[DataRequired()])
    has_sockets = SelectField("has sockets", choices=["true", "false"], validators=[DataRequired()])
    can_take_calls = SelectField("can take calls", choices=["true", "false"], validators=[DataRequired()])
    coffee_price = StringField('coffee price e.g. 7$', validators=[DataRequired()])
    open = StringField("Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating",
                                choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating",
                              choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability",
                               choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])

    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
def home():
    api_manager = ApiManager()
    all_data = api_manager.get_all()
    country_unique_vals = []
    for item in all_data["cafes"]:
        country_unique_vals.append(item["country"])
    country_unique_set = list(set(country_unique_vals))
    if request.method == 'POST':
        response = request.form.to_dict()
        if response:
            if len(response) == 1 and response["country"] == 'All':
                return render_template("index.html", cafees=all_data["cafes"], countries=country_unique_set)
            if response["country"] == 'All':
                response.pop("country")
            for k, v in response.items():
                if k != "country":
                    response[k] = 1
            filtered_data = api_manager.get_filtered_data(response)
            return render_template("index.html", cafees=filtered_data["cafes"], countries=country_unique_set)
    return render_template("index.html", cafees=all_data["cafes"], countries=country_unique_set)


@app.route("/cafe", methods=["GET", "POST"])
def cafe():
    cafe_id = request.args.get("id")
    api_manager = ApiManager()
    cafe_data = api_manager.get_cafe_by_id(cafe_id)
    full_map_link = unshorten_url(cafe_data["cafe"]["map_url"])
    name_location_map = full_map_link.split("/")[5:7]
    try:
        loc_xy = name_location_map[1].split(",")[:2]
        name_location_map[1] = f"{loc_xy[0]},{loc_xy[1]}"
    except IndexError:
        pass
    cafe_data["cafe"]["name_location_map"] = name_location_map
    if cafe_data:
        return render_template("cafe.html", cafe=cafe_data["cafe"])


@app.route("/add_cafe", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    api_manager = ApiManager()
    if form.validate_on_submit():
        response = api_manager.add_cafe(name=form.cafe_name.data,
                                        map_url=form.map_url.data,
                                        img_url=form.img_url.data,
                                        loc=form.location.data,
                                        country=form.country.data,
                                        sockets=form.has_sockets.data,
                                        toilet=form.has_toilet.data,
                                        wifi=form.has_wifi.data,
                                        calls=form.can_take_calls.data,
                                        seats=form.seats.data,
                                        coffee_price=form.coffee_price.data)

        return render_template("add_cafe.html", form=form, api_response=response)
    return render_template("add_cafe.html", form=form)


def unshorten_url(url):
    req = requests.head(url, allow_redirects=True).url
    return requests.head(req, allow_redirects=True).url


if __name__ == '__main__':
    app.run(debug=True)
