import unittest
from app import app, db 

# this test will automatically test the login functionality
class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app 
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True  
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove() 
            db.drop_all() 

    def test_login(self):
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()