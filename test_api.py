import app
import unittest

class TestApi(unittest.TestCase):
    def setUp(self):
        """
        Setting Up app for testing
        """
        app.connex_app.testing = True
        self.app = app.connex_app.app.test_client()
    
    def test_home(self):
        """
        Testing homepage
        """
        result = self.app.get('/')
        self.assertEqual(result.status_code,200, "Home page tidak dapat ditampilkan")
        
    def test_get_director(self):
        """
        Testing Api get all director
        """
        result = self.app.get('/api/director')
        self.assertEqual(result.status_code,200, "Data directors tidak dapat ditampilkan")
    
    def test_get_movies(self):
        """
        Testing Api get all movies
        """
        result = self.app.get('/api/movies')
        self.assertEqual(result.status_code,200, "Data movies tidak dapat ditampilkan")