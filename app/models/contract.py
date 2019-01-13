from app import db, web3
from app.ethereum import Manager as SCManager

user_contract_assoc = db.Table('contracts_users',
    db.Column('contract_id', db.Integer, db.ForeignKey('contracts.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Contract(db.Model):
    __table_args__ = dict(sqlite_autoincrement=True)
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(512), index=True)
    amount_due = db.Column(db.Integer, index=True)
    ethereum_addr = db.Column(db.String(64), unique=True, index=True)
    users = db.relationship('User', secondary=user_contract_assoc,
                            lazy='subquery', backref=db.backref('contracts', lazy=True))

    @staticmethod
    def generate_fake(count=10, **kwargs):
        """Generate a number of fake contracts for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice, randint
        from faker import Faker
        from app.config import Config
        import os.path

        fake = Faker()
        seed()

        payment_contract_meta = dict(name='Payment', filename='Payment.sol')
        payment_contract_owner = os.getenv('ETH_CONTRACT_OWNER')
        assert payment_contract_owner is not None, "Set the owner; export ETH_CONTRACT_OWNER='...'"
        payment_contract_path = os.path.join(Config.ROOT_DIR,
                                             'etc/contracts',
                                             payment_contract_meta['filename'])
        payment_contract_amount_due_base = 1000000000000000000
        scm = SCManager(web3)

        for i in range(count):
            amount_due = payment_contract_amount_due_base + i * payment_contract_amount_due_base

            contract_eth_addr = scm.create_contract(
                payment_contract_owner,
                payment_contract_path,
                payment_contract_meta['name'],
                amount_due)

            c = Contract(
                name='{} {}'.format(payment_contract_meta['name'], i + 1),
                description=fake.pystr(min_chars=40, max_chars=80),
                amount_due=amount_due,
                ethereum_addr=contract_eth_addr,
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
            name=self.name,
            description=self.description,
            amount_due=self.amount_due,
            ethereum_addr=self.ethereum_addr,
            users=users)

    def __repr__(self):
        return "<Contract %r>" % str(self.__dict__)

