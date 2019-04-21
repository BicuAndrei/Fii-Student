import hug
from fiistudentrest.auth import login
from fiistudentrest.auth import register

app = hug.API(__name__)
hug.get('/login', api=app)(login)
hug.get('/register', api=app)(register)
