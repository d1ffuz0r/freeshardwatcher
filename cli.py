import sys
sys.path.append("web.py-0.37-py2.7.egg")
import json
import db
import web

class Client(object):

    def all_online(self):
        return db.session.query(db.Online).all()

    def get_by_nick(self, nick):
        player = db.session.query(db.Player).filter_by(name=nick).first()
        if player:
            return db.session.query(db.PlayersOnline).filter_by(player_id=player.id).all()
        else:
            return None

urls = (
    '/', 'Index',
    '/get/(.*)/', 'GetStat'
)

app = web.application(urls, globals())
render = web.template.render('templates/', base="base")
cli = Client()

class Index:
    def GET(self):
        query = cli.get_by_nick(nick="Lacio")
        query1 = cli.get_by_nick(nick="dSpIN")

        ALL = [int(t.id) for t in cli.all_online()]
        lac = [int(t1.online_id) for t1 in query]
        ds = [int(t1.online_id) for t1 in query1]

        LACIO = map(lambda x: 1 if x in lac else 0, ALL)
        DSPIN = map(lambda x: 1 if x in ds else 0, ALL)
        return render.index(ALL, LACIO, DSPIN)

class GetStat:
    def GET(self, nick):
        query = cli.get_by_nick(nick=nick)
        ALL = map(lambda id: int(id.id), cli.all_online())#[int(t.id) for t in cli.all_online()]

        stat = map(lambda id: int(id.online_id), query)#[int(t1.online_id) for t1 in query]

        ss = map(lambda x: 1 if x in stat else 0, ALL)

        return json.dumps({"all": ALL, "stat": ss})


if __name__ == "__main__":
    app.run()