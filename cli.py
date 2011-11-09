import db

class Client(object):

    def all_online(self):
        return db.session.query(db.Online).all()

    def get_by_nick(self, nick):
        player = db.session.query(db.Player).filter_by(name=nick).first()
        if player:
            return db.session.query(db.PlayersOnline).filter_by(player_id=player.id).all()
        else:
            return None