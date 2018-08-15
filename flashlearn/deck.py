from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect

from flashlearn.db import connect

bp = Blueprint('deck', __name__)

engine = connect()


@bp.route('/deck/create', methods=['GET'])
def create_page():

    return render_template('deck/create.html')


@bp.route('/deck/create', methods=['POST'])
def save():

    name = request.form.get('name')

    sql = "INSERT INTO `deck` (`name`) VALUES ( '" + str(name) + "');"

    engine.execute(sql)

    return redirect('/')
