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
                **kwargs)
            db.session.add(c)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_dict(self):
        return dict(
            id=self.id,
            tax=self.tax,
            type=self.type,
            description=self.description,
            ethereum_addr=self.ethereum_addr)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)

