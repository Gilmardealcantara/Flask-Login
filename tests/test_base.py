from app import app
from flask.ext.testing import TestCase


class BaseTestCase(TestCase):

    def create_app(self):
        app.testing = True
        app.debug = True
        return app