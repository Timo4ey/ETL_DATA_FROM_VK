import json
from time import sleep

import requests

from etl_data_from_vk.config import vk_access_token
from etl_data_from_vk.my_logs_file import print_elapsed_time


@print_elapsed_time
def get_data_from_vk(list_of_indexes) -> json:
    output = []
    """Getting posts from vk"""
    for x in list_of_indexes:
        url = "https://api.vk.com/method/"
        method_wall = "wall.get"
        v = "5.131"
        params_wall = {
            "owner_id": x * -1,
            "access_token": vk_access_token,
            "count": 1,
            "v": v,
        }
        req_wall = requests.get(
            url + method_wall, params=params_wall, allow_redirects=False
        )
        req_wall.close

        sleep(0.5)
        output.append(req_wall.json())
    return output
