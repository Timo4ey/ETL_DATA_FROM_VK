from abc import ABC, abstractmethod
from datetime import datetime

from etl_data_from_vk.data_executor import VkData


class DataChecker(ABC):
    """Check -> data.url if url == n than --> smth"""

    @abstractmethod
    def is_properly(self, data: VkData) -> bool:
        pass


class DataFormat(ABC):
    """Convert data to a specific format"""

    def __init__(self, data: VkData) -> None:
        self.data = data

    @staticmethod
    def convert_to_format(self) -> dict:
        pass


class DataFilter(ABC):
    """Get data and special checker to filters data and return dict of
    values"""

    def __init__(
        self, data: VkData, checker: DataChecker, format_: DataFormat
    ) -> None:
        self.data = data
        self.checker = checker
        self.format_ = format_
        self.gotten_data: list[dict] = None

    @abstractmethod
    def get_proper_data(self) -> list[dict]:
        pass


class ContentDataFormat(DataFormat):
    @staticmethod
    def convert_to_format(data: VkData) -> dict:
        return {
            "public_date": str(datetime.utcfromtimestamp(data.public_date)),
            "content_vk_id": data.post_id,
            "group_id_fk": data.group_id,
        }


class PostsDataFormat(DataFormat):
    @staticmethod
    def convert_to_format(data: VkData) -> dict:
        return {
            "url": data.url[0].get("url"),
            "text": data.text,
            "content_fk": data.post_id,
        }


class CarouselDataFormat(DataFormat):
    @staticmethod
    def convert_to_format(data: VkData) -> dict:
        carousel = {
            "text": data.text,
            "content_fk": data.post_id,
        }
        carousel.update(data.url[0])
        return carousel


class ContentDataChecker(DataChecker):
    @staticmethod
    def is_properly(data: VkData) -> bool:
        return len(data.url[0]) >= 2


class ContentUniqueChecker(DataChecker):
    @staticmethod
    def is_unique(data: VkData, content_ids: set) -> bool:
        return data.post_id not in content_ids


class ContentProperAndUnique(ContentDataChecker, ContentUniqueChecker):
    @classmethod
    def is_properly(cls, data: VkData, content_ids: set) -> bool:
        return super().is_properly(data) and super().is_unique(
            data, content_ids
        )


class PostDataChecker(DataChecker):
    @staticmethod
    def is_properly(data: VkData) -> bool:
        return len(data.url[0]) == 1


class PostsProperAndUnique(PostDataChecker, ContentUniqueChecker):
    @classmethod
    def is_properly(cls, data: VkData, content_ids: set) -> bool:
        return super().is_properly(data) and super().is_unique(
            data, content_ids
        )


class CarouselDataChecker(DataChecker):
    @staticmethod
    def is_properly(data: VkData) -> bool:
        return len(data.url[0]) > 1


class CarouselProperAndUnique(CarouselDataChecker, ContentUniqueChecker):
    @classmethod
    def is_properly(cls, data: VkData, content_ids: set) -> bool:
        return super().is_properly(data) and super().is_unique(
            data, content_ids
        )


class MainDataFilter(DataFilter):
    def __init__(
        self, data: VkData, checker: DataChecker, format_: DataFormat
    ) -> None:
        super().__init__(data, checker, format_)
        self.gotten_data: list[dict] = []

    def get_proper_data(self) -> list[dict]:
        for item in self.data:
            if self.checker.is_properly(item):
                self.gotten_data.append(self.format_.convert_to_format(item))
        return self.gotten_data
