import hug
from fiistudentrest.auth import login
from fiistudentrest.auth import register

app = hug.API(__name__)
app.http.add_middleware(hug.middleware.CORSMiddleware(app))
hug.get('/login', api=app)(login)
hug.get('/register', api=app)(register)
