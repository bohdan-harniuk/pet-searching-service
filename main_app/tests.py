from django.test import TestCase
from django.test.client import Client

class UserMethodTests(TestCase):
    
    def test_login(request):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        response.status_code
        
        response = c.get('/user/(?P<user_id>[0-9]+)/settings/')
        response.content