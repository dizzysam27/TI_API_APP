import requests

class Get_Digikey_Authentication_Token():

    # def __init__(self, ):
        
    #     self.digikey_client_id = digikey_client_id
    #     self.digikey_client_secret = digikey_client_secret
    #     self.code = code

        
    
    def Get_Authentication_Token_First(self,digikey_client_id, digikey_client_secret, code):

        head={'Content-Type':'application/x-www-form-urlencoded&'}
        data={'code':code,'client_id':digikey_client_id,'client_secret':digikey_client_secret,'redirect_uri':'https://www.ti.com/digikey_callback/','grant_type':'authorization_code'}
        access_token_response = requests.post("https://api.digikey.com/v1/oauth2/token", data, head)
        token_response=eval((access_token_response.text).strip())
        accesstoken=token_response['access_token']
        print(accesstoken)
        refreshtoken=token_response['refresh_token']
        return accesstoken

class Renew_Digikey_Authentication_Token():

    def __init__(self, digikey_client_id, digikey_client_secret, refreshtoken):
        
        self.digikey_client_id = digikey_client_id
        self.digikey_client_secret = digikey_client_secret
        self.refreshtoken = refreshtoken

        self.Renew_Authentication_Token()

    def Renew_Authentication_Token(self):
        head={'Content-Type':'application/x-www-form-urlencoded&'}
        data={'client_id':self.digikey_client_id,'client_secret':self.digikey_client_secret,'refresh_token':self.refreshtoken,'grant_type':'refresh_token'}
        access_token_response = requests.post("https://api.digikey.com/v1/oauth2/token", data, head)
        print(access_token_response.text)
        token_response=eval((access_token_response.text).strip())
        accesstoken=token_response['access_token']
        refreshtoken=token_response['refresh_token']
        accesstoken='ewytC0wR6l7HuDXNCiaSQUpAEGh5'