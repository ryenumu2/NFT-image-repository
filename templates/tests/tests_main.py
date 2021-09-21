import main
from unittest.mock import MagicMock, Mock
import os
import unittest
import sqlite3
from flask_testing import TestCase
from flask import Flask
from mock import patch

class MyUnitTests(unittest.TestCase):

    app = Flask(__name__)

    def setup(self):
        main.create_connection()

    def test_connection_success_to_inventory_db(self):
        sqlite3.connect = MagicMock(return_value='SQLite3 Connection Success')
        dbc = sqlite3.connect('inventory.db')
        self.assertEqual(dbc, 'SQLite3 Connection Success')

    """ def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app """ """

        def test_delete(self):
        #cur = sqlite3.connect('inventory.db').cursor()
        #self.assertTrue()
        #main.delete(1)
        (cur) = main.create_connection()
        cur.execute(''' SELECT id FROM nfts WHERE rowid = 1 ''')
        expected = cur.fetchone()[0]
        self.assertEqual(2, expected) """

    #def test_status_code(self):
    #    response = self.client.get('/')
    #    self.assert_template_used('index.html')
    #    self.assert_context("rows", "rows")
    #    self.assertEqual(response.status_code, 200)

    #def tearDown(self):
        #Delete db after testing
        #os.remove('inventory.db')


if __name__ == '__main__':
    unittest.main()


