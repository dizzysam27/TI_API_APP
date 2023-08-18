import requests
class Info():

    def __init__(self, product_num, token):

        self.product_num = product_num
        self.token = token

    def call_info(self):
        
        self.data_url = 'https://transact.ti.com/v1/products/' + self.product_num
        self.api_call_headers = {'Authorization': 'Bearer ' + self.token}
        self.api_call_response = requests.get(self.data_url, headers=self.api_call_headers, verify=False)

        self.product_info = self.api_call_response.text
        try:
            self.product_info = self.product_info.replace("null","True")
        except:
            pass
        try:
            self.product_info = self.product_info.replace("true","True")
        except:
            pass
        try:
            self.product_info = self.product_info.replace("false","False")
        except:
            pass




        self.product_info_dict = eval(self.product_info)
        # print(self.product_info_dict)
        
        return self.product_info_dict
    
    def find_Identifier(self):
        self.Identifier = self.product_info_dict.get('Identifier')
        return self.Identifier
    

