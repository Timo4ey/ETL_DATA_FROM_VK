import json
from functools import wraps

import requests


class InternetCon:
    def __enter__(self, *args, **kwargs):
        print("Start connection")
        self.session = requests.session()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.session:
            self.session.close()
            print("Connections has been closed")


# @print_elapsed_time
def internet_connection(func):
    @wraps(func)
    def with_connection(self, *args, **kwargs):
        response = None
        with InternetCon() as con:
            methods = {
                "POST": con.session.post,
                "GET": con.session.get,
                "PUT": con.session.put,
                "DELETE": con.session.delete,
            }
        result = func(self, *args, **kwargs)
        method = result.get("method")
        url = result.get("url")
        body = result.get("body") if result.get("body")[0] else ""
        headers = result.get("headers")
        response = methods.get(method)(url=url, headers=headers, data=body)
        return response

    return with_connection


class BaseCreator:
    def __init__(self, link: str, *args, **kwargs):
        self.link = link
        self._body: list[dict] = [{}]
        self._headers: dict = {"Content-Type": "application/json"}
        self.req = {
            "url": self.link,
            "body": self._body,
            "headers": self._headers,
        }
        self.req_id = {
            "url": self.link,
            "body": self._body,
            "headers": self._headers,
        }

    @internet_connection
    def get(self):
        self.req["method"] = "GET"
        return self.req

    @internet_connection
    def create(self, *args, **kwargs):
        self.req["method"] = "POST"
        return self.req

    @internet_connection
    def update(self):
        if not self.body:
            raise "NO data in body"
        self.req["method"] = "PUT"
        return self.req

    @internet_connection
    def delete(self, id: dict):
        self.req["method"] = "DELETE"
        self.req["body"] = json.dumps(id)
        return self.req

    @internet_connection
    def delete_by_id(self, group_id: int):
        self.req_id["method"] = "DELETE"
        self.req_id["url"] = f"{self.link}{group_id}"
        return self.req_id

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, items: list[dict]):
        self._body = json.dumps(items)
        self.req.update({"body": self._body})

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, new_headers: dict):
        self.headers.update(new_headers)
        self.req.update({"headers": self._body})


class GroupsCreator(BaseCreator):
    fields = {"group_vk_id": 0, "group_name": ""}

    def __init__(self, link: str, *args, **kwargs):
        super().__init__(link, *args, **kwargs)
        self.link = link

    def get(self):
        return super().get().text

    def create(self, group_vk_id: int, group_name: str = ""):
        self.fields.update(
            {"group_vk_id": group_vk_id, "group_name": group_name}
        )
        self.body = self.fields
        return super().create()

    def update(
        self, group_id: int, group_vk_id: int = 0, group_name: str = ""
    ):
        self.fields.update(
            {
                "group_id": group_id,
                "group_vk_id": group_vk_id,
                "group_name": group_name,
            }
        )
        self.body = self.fields
        return super().update()

    def delete(self, group_id: int):
        return super().delete({"group_id": group_id})

    def delete_by_id(self, group_id: int):
        return super().delete_by_id(group_id)

    def retrieve_ids(self):
        data = json.loads(self.get())
        if data:
            return [x.get("group_vk_id") for x in data]
        raise "There are no added groups in DataBase"


class ContentCreator(BaseCreator):
    fields = {"content_vk_id": 0, "group_id_fk": "", "public_date": ""}

    def __init__(self, link: str, *args, **kwargs):
        super().__init__(link, *args, **kwargs)

    def get(self):
        return super().get().text

    def create(self, data):
        self.fields.update(data)
        self.body = self.fields
        return super().create()

    def create_all(self, data: list[dict, dict], *args, **kwargs) -> None:
        for item in data:
            self.fields.update(item)
            self.body = self.fields
            super().create()

    def update(self, data):
        self.fields.update()
        self.body = self.fields
        return super().update()

    def delete_by_id(self, content_id: int):
        return super().delete_by_id(content_id)

    def delete(self, group_id: int):
        return super().delete({"group_id": group_id})

    def retrieve_ids(self):
        data = json.loads(self.get())
        if data:
            return set([x.get("content_id") for x in data])
        raise "There are no added groups in DataBase"


class PostCreator(BaseCreator):
    """This object for data handlING  for POSTS"""

    fields = {}

    def __init__(self, link: str, *args, **kwargs):
        super().__init__(link, *args, **kwargs)

    def get(self):
        return super().get().text

    def create(self, data: dict, *args, **kwargs):
        self.fields.update(data)
        self.body = self.fields
        return super().create()

    def create_all(self, data: list[dict, dict], *args, **kwargs) -> None:
        for item in data:
            self.fields = item
            self.body = self.fields
            # print(self.body)
            super().create()

    def update(self, data, *args, **kwargs):
        self.fields = data
        self.body = self.fields
        return super().update()

    def delete_by_id(self, post_id: int):
        return super().delete_by_id(post_id)

    def delete(self, post_id: int):
        return super().delete({"post_id": post_id})


class CarouselCreator(BaseCreator):
    fields = {}

    def __init__(self, link: str, *args, **kwargs):
        super().__init__(link, *args, **kwargs)

    def get(self):
        return super().get().text

    def create(self, data: dict, *args, **kwargs):
        self.fields.update(data)
        self.body = self.fields
        return super().create()

    def create_all(self, data: list[dict, dict], *args, **kwargs) -> None:
        for item in data:
            self.fields = item
            self.body = self.fields
            super().create()

    def update(self, data, *args, **kwargs):
        self.fields = data
        self.body = self.fields
        return super().update()

    def delete_by_id(self, carousel_id: int):
        return super().delete_by_id(carousel_id)

    def delete(self, post_id: int):
        return super().delete({"carousel_id": post_id})


# group = Groups('http://127.0.0.1:8000/api/v1/groups/')
