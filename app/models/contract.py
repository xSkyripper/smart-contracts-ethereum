from app import db

user_contract_assoc = db.Table('contracts_users',
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Contract(db.Model):
    __table_args__ = dict(sqlite_autoincrement=True)
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(15), index=True)
    description = db.Column(db.String(512), index=True)
    ethereum_addr = db.Column(db.String(512), unique=True, index=True)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)

