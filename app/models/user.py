from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager
# from app.models.contract import user_contract_assoc, Contract


class Permission(object):
    USER = 0x01
    ADMIN = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, 'main', True),
            'Admin': (Permission.ADMIN,'admin', False),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


class User(UserMixin, db.Model):
    __table_args__ = dict(sqlite_autoincrement=True)
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    gov_id = db.Column(db.String(16), unique=True, index=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    ethereum_id = db.Column(db.String(512), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(permissions=Permission.ADMIN).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMIN)

    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake users for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        roles = Role.query.all()

        seed()
        for i in range(count):
            u = User(
                gov_id=fake.ssn(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                ethereum_id=fake.pystr(min_chars=40, max_chars=40),
                password='password',
                role=choice(roles),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def to_dict(self, with_contracts=False):
        contracts = []
        if with_contracts:
            contracts = [contract.id for contract in self.contracts]

        return dict(
            id=self.id,
            gov_id=self.gov_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            ethereum_id=self.ethereum_id,
            contracts=contracts)

    def __repr__(self):
        return '<User \'%s\'>' % self.full_name()

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def __eq__(self, other):
    """Overrides the default implementation"""
    if isinstance(other, User):
        return (self.id == other.id
            and self.gov_id == other.gov_id
            and self.first_name == other.first_name
            and self.last_name == other.last_name
            and self.email == other.email
            and self.ethereum_id == other.ethereum_id
            and self.contracts == contracts)
    return False

