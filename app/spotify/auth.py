import base64
import datetime
import requests

class SpotifyAuth(object):
	access_token = None
	access_token_expires = datetime.datetime.now()
	access_token_expired = True
	client_id = None
	client_secret = None
	token_url = 'https://accounts.spotify.com/api/token'

	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret

	def authenticate_token(self):
		token_url = self.token_url
		token_data = self.get_token_data()
		token_headers = self.get_token_headers()

		response = requests.post(token_url, data=token_data, headers=token_headers)

		if response.status_code not in range(200, 299):
			return False

		data = response.json()

		now = datetime.datetime.now()
		self.access_token = data['access_token']
		expires_in = data['expires_in']
		self.access_token_expires = now + datetime.timedelta(seconds=expires_in)
		self.access_token_expired = self.access_token_expires < now

		return True

	def get_access_token(self):
		token = self.access_token
		expires = self.access_token_expires
		now = datetime.datetime.now()
		if expires < now or token is None:
			self.authenticate_token()
			return self.get_access_token()

		return token

	def get_client_credentials(self):
		client_id = self.client_id
		client_secret = self.client_secret

		if client_secret is None or client_id is None:
			raise Exception('You must set client_id and client_secret')

		client_credentials = f'{client_id}:{client_secret}'
		client_credentials_encoded = base64.b64encode(client_credentials.encode('ascii'))

		return client_credentials_encoded.decode('ascii')

	def get_token_headers(self):
		client_credentials_encoded = self.get_client_credentials()

		return {
			'Content-Type': 'application/x-www-form-urlencoded',
			'Authorization': f'Basic {client_credentials_encoded}'
		}

	def get_token_data(self):
		return {
			'grant_type': 'client_credentials'
		}