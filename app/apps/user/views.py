from flask import Blueprint, render_template, redirect, request, jsonify, g, url_for
from app import app
from forms import LoginForm
from models import User
from flask.ext.login import login_user, logout_user, current_user
from app.apps.utils.encode import sha512
from app import lm
from urlparse import urlparse

mod = Blueprint('user', __name__,
                template_folder='templates',
                url_prefix='/user')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == "POST":
        try:
            # user = User.query.filter_by(email=form.email.data, password=sha512(form.password.data))[-1]
            user = User.query.filter_by(email=form.email.data, password=form.password.data)[-1]
            login_user(user, remember=True)
            return redirect('/')
        except:
            return render_template('user/login.html', form=form)

    return render_template('user/login.html', form=form)


@mod.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


@mod.route('/data/')
def data():
    users = User.query.all()
    json = {}
    data = [];
    for user in users:
        data.append((
            user.id,
            user.name,
            user.email
        ))
    json['data'] = data

    return jsonify(json=json)


''' feito no js
@mod.route("/getPlotCSV")
def getPlotCSV():
    users = User.query.all()

    csv = 'ID,NAME,EMAIL\n'
    for user in users:
        csv += str(user.id) + ',' + user.name + ',' + user.email + '\n' 

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})
'''