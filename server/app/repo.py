from app.models import *
from app.decorators.LoggingAspect import before, after

class UserRepository(object):
    def __init__(self):
        pass

    @before
    @after
    def get_users(self):
        return User.query.all()
    
    @before
    @after
    def add_user(self, user):
        db.session.add(user)
        db.session.commit()