from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Bucketlist, Bucketitems
from django.contrib.auth.models import User


factory = APIRequestFactory()

# Create your tests here.


class BucketlistTest(TestCase):


    def setUp(self):
        
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.bucketlist = None
        data = {"username": "admintest", "password": "password"}
        response = self.client.post('/api/users/', data, format='json')
        self.user = User.objects.all().first()
        self.bucketlist = Bucketlist
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def _require_login(self):
        url = '/api/api-token'
        data = {"username": "admintest", "password": "password"}
        response = self.client.post(url, data, format='json')
        return response.data
      

    def _get_token(self):
    	token = self._require_login()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token['token'])
       

    def test_2_token_generation(self):
        # Test if a token has been produced using credntials
        url = '/api/api-token'
        data = {"username": "admintest", "password": "password"}
        response = self.client.post(url, data, format='json')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
      

    def test_3_page_authorization(self):
        # Check if protected page can be accessed without authorization
        response = self.client.get("/api/bucketlists/", format='json')
        self.assertEqual(response.status_code, 401)
        response = self.client.get("auto_find_instance_path()/users/", format='json')
        self.assertNotEqual(response.status_code, 401)

    def test_4_tokenAccess(self):
        # use token to access authicated page:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating
        token = self._require_login()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token['token'])
        response = self.client.get("/api/bucketlists/", format='json')
        self.assertEqual(response.status_code, 200)

    def test_5_bucketlist(self):
    	# Test Bucketlist creation
    	self._get_token()
    	data = {'name':'bucketlist1'}
    	response = self.client.post("/api/bucketlists/", data,format='json')
    	self.bucketlist = Bucketlist.objects.first()
    	self.assertEqual(response.status_code,201)
    	self.assertEqual(Bucketlist.objects.count(),1)

    	# Edit Bucketlist
    	sid = Bucketlist.objects.first().id
    	url = "/api/bucketlists/{}/".format(sid)
    	response = self.client.get(url,format='json')
    	response.data['name'] = 'new game'
    	data=response.data
    	response = self.client.put(url,data,format='json')
    	self.assertEqual(response.status_code,201)

    	# Delete bucketlist
    	response = self.client.delete(url, data)
    	self.assertEqual(Bucketlist.objects.count(),0)
    	

    def test_6_add_edit_item(self):
    	self._get_token()
    	data ={'name':'bucketlist1'}
    	item = {'name':'item'}
    	response = self.client.post("/api/bucketlists/", data,format='json')
    	
    	# create Item
    	bid = Bucketlist.objects.first().id
    	url = "/api/bucketlists/{}/items/".format(bid)
    	response = self.client.post(url, item, format='json')
    	self.assertEqual(response.status_code,201)
    	self.assertEqual(Bucketitems.objects.count(),1)

    	# edit item
    	id = Bucketitems.objects.first()
    	url += "{}/".format(id.id)
    	response = self.client.get(url, item, format='json')
    	item = response.data
    	item['done'] = False
    	response = self.client.put(url, item, format='json')
    	id = Bucketitems.objects.first()
    	self.assertEqual(response.status_code,201)

    	# Delete
    	response = self.client.delete(url, item, format='json')
    	self.assertEqual(Bucketitems.objects.count(),0)



    	


    	




















