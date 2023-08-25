import requests
class Order_Info():

    def __init__(self, product_num, token):

        self.product_num = product_num
        self.token = token

    def call_info(self):
        
        self.data_url = 'https://transact.ti.com/v2/store/products/' + self.product_num
        self.api_call_headers = {'Authorization': 'Bearer ' + self.token}
        self.api_call_response = requests.get(self.data_url, headers=self.api_call_headers, verify=False)

        self.product_order_info = self.api_call_response.text

        true_to_True = self.product_order_info.replace("null","True")
        true_to_True = true_to_True.replace("true","True")

        print(type(true_to_True))
        
        return eval(true_to_True)
    
class Search_by_GPN():

    def __init__(self, token, gpn):

        self.token = token
        self.gpn = gpn
        
    def find_all_opns_from_gpn(self, currency):

        api_call_headers = {'Authorization': 'Bearer ' + self.token}
        url_post = 'https://transact.ti.com/v2/store/products?gpn='+ self.gpn +'&currency=' + str(currency) + '&exclude-evms=true&page=0&size=20'

        api_call_response = requests.get(url_post, headers=api_call_headers)

        # print(api_call_response.text)
        product_order_info = api_call_response.text
        # print(product_order_info)

        try:
            product_order_info = product_order_info.replace("null","True")
        except:
            pass
        try:
            product_order_info = product_order_info.replace("true","True")
        except:
            pass
        try:
            product_order_info = product_order_info.replace("false","False")
        except:
            pass
        
        product_order_info = eval(product_order_info)
        
        order_info_keys = []
        order_info_values = []

        for key in product_order_info.keys():
            order_info_keys.append(key)

        for value in product_order_info.values():
            order_info_values.append(value)

        return order_info_values[0]

    




























# class Place_Order():

#     def Place_Saved_Part_Order():

#         access_token_response = requests.post('https://transact.ti.com/v2/store/orders/test', verify=False, allow_redirects=False, auth=('l8g9S577exxtpmCSGC56mnBsT2REZN7a', 'CROP7wM4aXq3A6Oz'))
#         print('Access Token Status: ',access_token_response.status_code)

# Place_Order.Place_Saved_Part_Order()