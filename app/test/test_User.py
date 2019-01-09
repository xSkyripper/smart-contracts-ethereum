from app.models import User, Role
from app import db
import app
import unittest


class TestUser(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add(self):
        """Check if the database add function works as expected."""
        # Generate a user and add it to the database
        print("Testing User add ...")
        role = Role.query.filter_by(name='User').first()
        new_gov_id = 41231231
        added_user = User(
                gov_id = new_gov_id,
                first_name = "John",
                last_name = "Doe",
                email = "johndoe@email.com",
                ethereum_id = 12341234,
                password = "password",
                role = role)
        try:
            db.session.add(added_user)
            db.session.commit()
        except:
            db.session.rollback()

        # Query the database for the user with the ID previously added
        db_user = User.query.get(new_gov_id)

        # The two users should always be equal.
        self.assertEqual(added_user, db_user)


    def test_eq(self):
        """Check if the __eq__ function works as expected."""
        # Create two identical users
        print("Testing user __eq__ ...")
        user_role = Role.query.filter_by(name='User').first()
        user1 = User.query.get(1)
        user2 = User.query.get(2)
        # Get __eq__ result
        areEqual = (user1 == user2)
        
        # Should always return true
        self.assertEqual(areEqual, True)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestUser('test_add'))
    suite.addTest(TestUser('test_eq'))
    return suite

def run_tests():
    print("Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    return unittest.TextTestRunner(verbosity=2).run(suite)