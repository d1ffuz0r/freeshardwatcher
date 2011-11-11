import sys
sys.path.append("bottle-0.9.6-py2.7.egg")
import json
import db
from bottle import Bottle, view, run, static_file, debug

class Client(object):

    def all_online(self):
        return db.session.query(db.Online).all()

    def get_by_nick(self, nick):
        player = db.session.query(db.Player).filter_by(name=nick).first()
        if player:
            return db.session.query(db.PlayersOnline).filter_by(player_id=player.id).all()
        else:
            return None

cli = Client()
app = Bottle()

@app.route('/static/:fname#.*#')
def static(fname):
    return static_file(fname, root='static/')

@app.route('/')
@view('templates/about')
def about():
    return {"stub": "pass"}

@app.route('/help/')
@view('templates/help')
def help():
    return {"stub": "pass"}

@app.route('/contact/')
@view('templates/contact')
def contact():
    return {"stub": "pass"}

@app.route('/download/')
@view('templates/download')
def download():
    return {"stub": "pass"}

@app.route('/online/')
@view('templates/online')
def online():
    query = cli.get_by_nick(nick="dSpIN")
    ALL = map(lambda id: int(id.id), cli.all_online())
    stat = map(lambda id: int(id.online_id), query)
    DSPIN = map(lambda x: 1 if x in stat else 0, ALL)
    return {"ALL": ALL, "DSPIN": DSPIN}

@app.route('/get/:nick/')
@view('templates/about')
def get(nick):
    query = cli.get_by_nick(nick=nick)
    ALL = map(lambda id: int(id.id), cli.all_online())#[int(t.id) for t in cli.all_online()]
    stat = map(lambda id: int(id.online_id), query)#[int(t1.online_id) for t1 in query]
    ss = map(lambda x: 1 if x in stat else 0, ALL)
    return json.dumps({"all": ALL, "stat": ss})


if __name__ == "__main__":
    debug(True)
    run(app, host='localhost', port=8080, reloader=True)