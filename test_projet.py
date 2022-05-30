from asyncio.windows_events import NULL
import unittest
import bitcoin
from flask import Flask,render_template
import app

class ConnexionTest(unittest.TestCase):

    def test_fonction_connexion(self):
        c,d= bitcoin.connexion()
        self.assertEqual(type(c),type(d))
        self.assertEqual(len(c),len(d))
    
    
    def test_menu(self):
        tester = app.app.test_client(self)
        reponse = tester.get("/")
        statuscode = reponse.status_code
        self.assertEqual(statuscode,200)
    
    def test_add(self):
        tester = app.app.test_client(self)
        reponse = tester.get("/add")
        statuscode = reponse.status_code
        self.assertEqual(statuscode,200)

    def test_graphe(self):
        tester = app.app.test_client(self)
        reponse = tester.get("/page_graphique")
        statuscode = reponse.status_code
        self.assertEqual(statuscode,200)


    def test_remove(self):
        tester = app.app.test_client(self)
        reponse = tester.get("/remove")
        statuscode = reponse.status_code
        self.assertEqual(statuscode,200)

    def test_post_remove(self):
        tester = app.app.test_client(self)
        reponse = tester.post("/remove")
        msg = reponse.data
        self.assertIsNot(msg,NULL)

    def test_post_add(self):
        tester = app.app.test_client(self)
        reponse = tester.post("/add")
        msg = reponse.data
        self.assertIsNot(msg,NULL)
