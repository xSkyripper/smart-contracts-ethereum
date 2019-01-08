from app import db

user_contract_assoc = db.Table('contracts_users',
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Contract(db.Model):
    __table_args__ = dict(sqlite_autoincrement=True)
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    tax = db.Column(db.Integer, index=True)
    type = db.Column(db.String(15), index=True)
    description = db.Column(db.String(512), index=True)
    ethereum_addr = db.Column(db.String(512), unique=True, index=True)
    abi = db.Column(db.BLOB)
    users = db.relationship('User', secondary=user_contract_assoc,
                            lazy='subquery', backref=db.backref('contracts', lazy=True))

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake contracts for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice, randint
        from faker import Faker

        fake = Faker()

        seed()
        for i in range(count):
            c = Contract(
                tax=randint(1, 100),
                type=fake.ssn(),
                description=fake.pystr(min_chars=40, max_chars=80),
                ethereum_addr=fake.pystr(min_chars=40, max_chars=40),
                abi=bytes(fake.pystr(min_chars=80, max_chars=120), 'UTF-8'),
                **kwargs)
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_dict(self, with_users=False):
        users = []
        if with_users:
            users = [user.id for user in self.users]

        return dict(
            id=self.id,
            tax=self.tax,
            type=self.type,
            description=self.description,
            ethereum_addr=self.ethereum_addr,
            abi=self.abi.decode('UTF-8'),
            users=users)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)

