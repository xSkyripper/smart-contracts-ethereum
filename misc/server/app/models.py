from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

contracts = db.Table('contracts',
    db.Column('contract_id', db.Integer, db.ForeignKey('contract.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    gov_id = db.Column(db.String(15), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    ethereum_id = db.Column(db.String(512), unique=True, nullable=False)
    contracts = db.relationship('Contract', secondary=contracts, lazy='subquery',
                                backref=db.backref('users', lazy=True))

    def __repr__(self):
        return "<User %r>" % str(self.__dict__)


class Contract(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15), unique=False, nullable=True)
    description = db.Column(db.String(512), unique=False, nullable=True)
    ethereum_addr = db.Column(db.String(512), unique=True, nullable=False)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)