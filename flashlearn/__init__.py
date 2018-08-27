import os

from flask import Flask
from flask_cors import CORS
# from flask import make_response


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # app.config.from_pyfile('../flashcard.cfg')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import deck
    app.register_blueprint(deck.bp)
    app.add_url_rule('/deck/', endpoint='index')

    from . import flashcard
    app.register_blueprint(flashcard.bp)
    app.add_url_rule('/flashcard/', endpoint='index')


    from . import learn
    app.register_blueprint(learn.bp)
    app.add_url_rule('/learn/', endpoint='index')


    # test CORS
    @app.route('/hello/', methods=['GET', 'POST'])
    def hello():
        # Without cors-flask package
        # r = make_response('Hello, cross-origin Flashlearn!')
        # r.headers.set('Access-Control-Allow-Origin', "http://localhost:3000")
        # return r

        return 'Hello, cross-origin Flashlearn!'




    return app
