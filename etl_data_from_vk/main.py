import time

import schedule

from etl_data_from_vk.data_converters import (
    CarouselDataChecker,
    CarouselDataFormat,
    ContentDataChecker,
    ContentDataFormat,
    MainDataFilter,
    PostDataChecker,
    PostsDataFormat,
)
from etl_data_from_vk.data_executor import DataExecuter
from etl_data_from_vk.service import (
    CarouselCreator,
    ContentCreator,
    GroupsCreator,
    PostCreator,
)
from etl_data_from_vk.vk_data_request import get_data_from_vk


def main():
    LINK: str = "http://172.17.0.1:8000/api/v1/"
    vk_data: dict = None

    group = GroupsCreator(f"{LINK}groups/")

    vk_data = get_data_from_vk(group.retrieve_ids())

    bs = DataExecuter(vk_data)
    data = bs.get_all_data()

    content = MainDataFilter(
        data, checker=ContentDataChecker, format_=ContentDataFormat
    ).get_proper_data()

    posts = MainDataFilter(
        data, checker=PostDataChecker, format_=PostsDataFormat
    ).get_proper_data()

    carousel = MainDataFilter(
        data, checker=CarouselDataChecker, format_=CarouselDataFormat
    ).get_proper_data()

    content_creator = ContentCreator(f"{LINK}content/")
    post_creator = PostCreator(f"{LINK}posts/")
    carousel_creator = CarouselCreator(f"{LINK}carousel/")

    content_creator.create_all(content)
    post_creator.create_all(posts)
    carousel_creator.create_all(carousel)


schedule.every(4).minutes.do(main).tag("hourly-tasks", "friend")

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
