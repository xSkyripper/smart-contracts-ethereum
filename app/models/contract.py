from app import db

user_contract_assoc = db.Table('contracts_users',
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Contract(db.Model):
    __table_args__ = dict(sqlite_autoincrement=True)
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    amount_due = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512), index=True)
    ethereum_addr = db.Column(db.String(512), unique=True, index=True)
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
                amount_due=randint(1, 100),
                name=fakse.first_name(),
                type=fake.ssn(),
                description=fake.pystr(min_chars=40, max_chars=80),
                ethereum_addr=fake.pystr(min_chars=40, max_chars=40),
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
            amount_due=self.amount_due,
            name=self.name,
            description=self.description,
            ethereum_addr=self.ethereum_addr,
            users=users)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)

