from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL


app = Flask(__name__)


# setting secret key
app.secret_key = 'your secret key'

# database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'terravista'

# Intialize MySQL
mysql = MySQL(app)

bcrypt = Bcrypt(app)

from app.controllers import default