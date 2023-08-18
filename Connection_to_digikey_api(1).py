import requests

digikey_client_id = "ljXW2AAvWc3EbORa841OhnrBTTgF0h22"
digikey_client_secret = "jTECZeL0nkf0a4Tj"
digikey_request_url = 'https://api.digikey.com/v1/oauth2/authorize?response_type=code&client_id=ljXW2AAvWc3EbORa841OhnrBTTgF0h22&redirect_uri=https%3A%2F%2Fwww.ti.com%2Fdigikey_callback%2F'
digikey_token_url = "https://api.digikey.com/v1/oauth2/token"

# webbrowser.open('https://api.digikey.com/v1/oauth2/authorize?response_type=code&client_id=ljXW2AAvWc3EbORa841OhnrBTTgF0h22&redirect_uri=https%3A%2F%2Fwww.ti.com%2Fdigikey_callback%2F')

#getting the access token for the first time
head={'Content-Type':'application/x-www-form-urlencoded&'}
data={'code':'XXmqpQXp','client_id':digikey_client_id,'client_secret':digikey_client_secret,'redirect_uri':'https://www.ti.com/digikey_callback/','grant_type':'authorization_code'}
access_token_response = requests.post(digikey_token_url, data, head)
print(access_token_response.text)
token_response=eval((access_token_response.text).strip())
accesstoken=token_response['access_token']
refreshtoken=token_response['refresh_token']

# refreshtoken="vmgcmGH3lVc93c49nNUYM7AaQDESrKeY"
# #getting the access token any  other time
# head={'Content-Type':'application/x-www-form-urlencoded&'}
# data={'client_id':digikey_client_id,'client_secret':digikey_client_secret,'refresh_token':refreshtoken,'grant_type':'refresh_token'}
# access_token_response = requests.post(digikey_token_url, data, head)
# print(access_token_response.text)
# token_response=eval((access_token_response.text).strip())
# accesstoken=token_response['access_token']
# refreshtoken=token_response['refresh_token']
# accesstoken='ewytC0wR6l7HuDXNCiaSQUpAEGh5'

# digikey_header={"X-DIGIKEY-Client-Id":digikey_client_id, "Authorization":"Bearer "+accesstoken}
# api_call_response = requests.get('https://api.digikey.com/Search/v3/Products/TLV9002IDR', headers=digikey_header)
# digikey_product_info=api_call_response.text
# try:
#     digikey_product_info = digikey_product_info.replace("null","True")
# except:
#     pass
# try:
#     digikey_product_info = digikey_product_info.replace("true","True")
# except:
#     pass
# try:
#     digikey_product_info = digikey_product_info.replace("false","False")
# except:
#     pass
# product_info = eval(digikey_product_info)
# print(product_info['StandardPricing'][-1])