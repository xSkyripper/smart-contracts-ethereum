from app.models import *

class UserRepository(object):
    def __init__(self):
        pass

    def get_users(self):
        return User.query.all()

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()