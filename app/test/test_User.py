# from app.models import User as UserModel
# from app import db

# class TestUser(unittest.TestCase):
#     def test_add(self):
#         """Check if the database add function works as expected."""
#         # Generate a user and add it to the database
#         role = Role.query.filter_by(name='User').first()
#         user_id = 987654321
#         added_user = User(
#                 gov_id = user_id,
#                 first_name = "John",
#                 last_name = "Doe",
#                 email = "johndoe@email.com",
#                 ethereum_id = 12341234,
#                 password = "password",
#                 role = role,
#                 **kwargs)
#         try:
#             db.session.add(added_user)
#             db.session.commit()

#         # Query the database for the user with the ID previously added
#         got_user = User.query.get(int(user_id))

#         # The two users should always be equal.
#         self.assertEqual(added_user, got_user)


#     def test_eq(self):
#         """Check if the __eq__ function works as expected."""
#         # Create two identical users
#         user1 = User(
#                 gov_id = 987654321,
#                 first_name = "John",
#                 last_name = "Doe",
#                 email = "johndoe@email.com",
#                 ethereum_id = 12341234,
#                 password = "password",
#                 role = role,
#                 **kwargs)
#         user2 = User(
#                 gov_id = 987654321,
#                 first_name = "John",
#                 last_name = "Doe",
#                 email = "johndoe@email.com",
#                 ethereum_id = 12341234,
#                 password = "password",
#                 role = role,
#                 **kwargs)

#         # Get __eq__ result
#         areEqual = (user1 == user2)
        
#         # Should always return true
#         self.assertEqual(areEqual, true)