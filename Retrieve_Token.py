import requests

class Authenticate():

    def __init__(self, client_id, client_secret):

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://transact.ti.com/v1/oauth/accesstoken"
        
    def authenticate_token(self):

        data = {'grant_type': 'client_credentials'}
        access_token_response = requests.post(self.token_url, data=data, verify=False, allow_redirects=False, auth=(self.client_id, self.client_secret))
        print('Access Token Status: ',access_token_response.status_code)

        if access_token_response.status_code == 200:

            access_token_response_dict = eval(access_token_response.text)
            self.token = access_token_response_dict.get('access_token')
            print('Access Token : ',self.token)

            return self.token
        
        else:
            print("Invalid Login")
            self.token = 0
            return self.token