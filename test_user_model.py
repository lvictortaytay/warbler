"""User model tests."""

# to run test:  python3 -m unittest test_user_model.py


import os
import bcrypt
from unittest import TestCase

from models import db, User, Message, Follows , Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warblertest"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr_function(self):
        """does the repr function work as expected?"""


        u = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.__repr__(u), f"<User #{u.id}: {u.username}, {u.email}>")


    def test_is_Following(self):
        """this test will detect when USER1 is following USER2 in the is_following function"""


        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD4"
        )

        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        
        f = Follows(user_being_followed_id = u2.id , user_following_id = u1.id)

        db.session.add(f)
        db.session.commit()

        self.assertEqual(u1.is_following(u2),True)


    def test_is_Following2(self):
        """this will test if user1 is not following user2"""

        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD4"
        )

        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.is_following(u2),False)


    def test_is_Followed_by(self):
        """will this detect when user1 is followed by user2"""

        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD4"
        )

        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()



        f = Follows(user_being_followed_id = u2.id , user_following_id = u1.id)

        db.session.add(f)
        db.session.commit()

        self.assertEqual(u2.is_followed_by(u1),True)


    def test_is_Followed_by2(self):
        """test to detect if user1 is not followed by user2"""

        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        u2 = User(
            email="user2@test.com",
            username="user2",
            password="HASHED_PASSWORD4"
        )

        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.is_followed_by(u2),False)


    # def test_user_signup(self):
    #         """this will test if a user is created with the valid credentials"""



    #         User.signup("random" , "random1@test.com" , "password1" ,"wxwex.sdx.com" )

    #         db.session.commit()

    #         users = User.query.all()
    #         usernames = []
    #         for user in users:
    #             usernames.append(user.username)

    #         self.assertIn("random" , usernames)


    # def test_user_signup2(self):
    #     """test if signup fails to create user if not all credentials met"""
    #     try:
    #         User.signup("random" , "random1@test.com" , "password1")
    #     except:
    #         self.assertRaises(TypeError)
        

        # db.session.commit()

        # users = User.query.all()
        # usernames = []
        # for user in users:
        #     usernames.append(user.username)


    # def test_user_authenticate(self):
    #     """test if user_authenticate give back a user with the right credentials"""


    #     u1 = User(
    #         email="test2@test.com",
    #         username="testuser2",
    #         password="HASHED_PASSWORD2"
    #     )
    #     db.session.add(u1)
    #     db.session.commit()

    #     self.assertEqual(User.authenticate(u1.username, "HASHED_PASSWORD2"),u1)

    # def test_user_authenticate2(self):
    #     """this test if the User.authenticate will fail if it is not passed in a username"""
    #     u1 = User(
    #         email="test2@test.com",
    #         username="testuser2",
    #         password="HASHED_PASSWORD2"
    #     )
    #     db.session.add(u1)
    #     db.session.commit()
        

    #     try:
    #         self.assertEqual(User.authenticate( u1.username , u1.password), u1)
    #     except:
    #         self.assertRaises(ValueError)

 


class UserMessagesTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_liked_message(self):
        """test if a liked message is stored in the database"""

        randomList = [1,2,3]
        self.assertIn(1 ,randomList)
        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        u2 = User(
            email="test2233@test.com",
            username="testuser3",
            password="HASHED_PASSWORD3"
        )
        db.session.add(u1)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()
        users = User.query.all()
        uM = Message(text = "hello world" , user_id = u2.id)
        db.session.add(uM)
        db.session.commit()
        likedMessage = Likes(user_id = u2.id , message_id = uM.id)
        db.session.add(likedMessage)
        db.session.commit()
        allMessages = Likes.query.all()
        allUserIds = []
        for likedId in allMessages:
            allUserIds.append(likedId.user_id)
        self.assertIn(u2.id,allUserIds)
    

    def test_message_stored(self):
        """test if there is a text in a message"""

        u1 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u1)
        db.session.commit()
        uM = Message(text = "hello world" , user_id = u1.id)
        db.session.add(uM)
        db.session.commit()

        self.assertIn("hello world" , uM.text)

    







class RoutingAndViewFunctionTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    








    