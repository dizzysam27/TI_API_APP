import requests

# client_id = '2f2b1cc3-8e25-4704-8fba-6264aae0a0bc'
# token_url = "https://api.mouser.com/api/v1/search/keyword?apiKey="+client_id

class MouserInfo():

    def __init__(self, key):

        token_url = "https://api.mouser.com/api/v1/search/keyword?apiKey="+key

        data = {
        "SearchByKeywordRequest": {
            "keyword": "TCAN1162DMTRQ1",
            "records": 0,
            "startingRecord": 0,
            "searchOptions": "string",
            "searchWithYourSignUpLanguage": "string"
        }
        }

        access_token_response = requests.post(token_url, json = data, verify=False, allow_redirects=False)
        print('Access Token Status: ',access_token_response.status_code)

        mouser_product_info = access_token_response.text

        try:
            mouser_product_info = mouser_product_info.replace("null","True")
        except:
            pass
        try:
            mouser_product_info = mouser_product_info.replace("true","True")
        except:
            pass
        try:
            mouser_product_info = mouser_product_info.replace("false","False")
        except:
            pass

        mouser_product_info = eval(mouser_product_info)

        # print(mouser_product_info['SearchResults']['Parts'])

        order_info_keys = []
        order_info_values = []

        for i in range(len(mouser_product_info['SearchResults'])):

            for key in mouser_product_info['SearchResults'].keys():
                order_info_keys.append(key)

            for value in mouser_product_info['SearchResults'].values():
                order_info_values.append(value)

        for i in range(len(order_info_keys)):
            print(order_info_keys[i], ":", order_info_values[i])