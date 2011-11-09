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
    '/', 'Index'
)

app = web.application(urls, globals())
render = web.template.render('templates/', base="base")

class Index:
    def GET(self):
        cli = Client()
        query = cli.get_by_nick(nick="Lacio")
        query1 = cli.get_by_nick(nick="dSpIN")

        ALL = [int(t.id) for t in cli.all_online()]
        lac = [int(t1.online_id) for t1 in query]
        ds = [int(t1.online_id) for t1 in query1]

        LACIO = map(lambda x,y: 1 if y is x else 0, ALL, lac)
        DSPIN = map(lambda x,y: 1 if y is x else 0, ALL, ds)
        return render.index(ALL, LACIO, DSPIN)

if __name__ == "__main__":
    app.run()