import unittest
from bitcoin import connexion

class ConnexionTest(unittest.TestCase):

    def test1(self):
        c,d= connexion()
        self.assertEqual(type(c),type(d))
    

        
