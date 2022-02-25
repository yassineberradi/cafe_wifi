import requests as requests

ALL_DATA_ENDPOINT = "http://127.0.0.1:5000/all"
SEARCH_ENDPOINT = "http://127.0.0.1:5000/search"
FILTER_ENDPOINT = "http://127.0.0.1:5000/filter"
CAFFE_BY_ID_ENDPOINT = "http://127.0.0.1:5000/cafe"
ADD_CAFE_ENDPOINT = "http://127.0.0.1:5000/add"


class ApiManager:
    def __init__(self):
        self.all_endpoint = ALL_DATA_ENDPOINT
        self.search_endpoint = SEARCH_ENDPOINT
        self.filter_endpoint = FILTER_ENDPOINT
        self.cafe_by_id_endpoint = CAFFE_BY_ID_ENDPOINT
        self.add_cafe_endpoint = ADD_CAFE_ENDPOINT

    def get_all(self):
        response = requests.get(url=self.all_endpoint).json()
        return response

    def get_search(self, arg):
        param = {
            "loc": arg
        }
        response = requests.get(url=self.search_endpoint, params=param).json()
        return response

    def get_filtered_data(self, dict_filtered):
        response = requests.get(url=self.filter_endpoint, params=dict_filtered).json()
        return response

    def get_cafe_by_id(self, cafe_id):
        param = {
            "id": cafe_id
        }
        response = requests.get(url=self.cafe_by_id_endpoint, params=param).json()
        return response

    def add_cafe(self, name, map_url, img_url, loc, country, sockets, toilet, wifi, calls, seats, coffee_price):
        param = {
            "name": name,
            "map_url": map_url,
            "img_url": img_url,
            "loc": loc,
            "country": country,
            "sockets": sockets,
            "toilet": toilet,
            "wifi": wifi,
            "calls": calls,
            "seats": seats,
            "coffee_price": coffee_price
        }
        response = requests.post(url=self.add_cafe_endpoint, params=param).json()
        return response
