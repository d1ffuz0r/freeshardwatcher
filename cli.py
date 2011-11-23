from json import dumps
from modules import db
from modules.bottle import Bottle, view, run,\
    static_file, post, request

app = Bottle()

@app.route('/static/:fname#.*#')
def static(fname):
    """
    return static files
    """
    return static_file(fname, root="static/")

@app.route('/')
@view('about')
def about():
    """
    about page
    """
    return {"stub": "pass"}

@app.route('/help')
@app.route('/help/')
@view('help')
def help():
    """
    help page
    """
    return {"stub": "pass"}

@app.route('/contact')
@app.route('/contact/')
@view('contact')
def contact():
    """
    contact page
    """
    return {"stub": "pass"}

@app.route('/download')
@app.route('/download/')
@view('download')
def download():
    """
    download page
    """
    return {"stub": "pass"}

@app.route('/online')
@app.route('/online/')
@view('online')
def online():
    """
    page online results
    """
    return {"stub": "pass"}

@app.route('/get', method="POST")
@app.route('/get/', method="POST")
@view('about')
def get():
    """
    get results for to nick
    """
    nick = request.forms.get("nick")
    frm = request.forms.get("from")
    to = request.forms.get("to")

    query = db.get_by_nick(nick=nick, frm=frm, to=to)
    if query:
        return dumps({"all": query["all"], "stat": query["player"]})
    else:
        return dumps({"message": "Not found"})