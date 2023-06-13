from etl_data_from_vk.data_converters import (
    CarouselDataChecker,
    CarouselDataFormat,
    CarouselProperAndUnique,
    ContentDataChecker,
    ContentDataFormat,
    ContentProperAndUnique,
    ContentUniqueChecker,
    PostDataChecker,
    PostsDataFormat,
    PostsProperAndUnique,
)
from etl_data_from_vk.tests.conftest import get_test_data

expected_data = get_test_data("test_data_converters/expected_data.json")


class TestsContentDataFormat:
    def test_public_date(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = ContentDataFormat.convert_to_format(data[0])
        assert result["public_date"] == expected_data[0]["post"]["public_date"]

    def test_content_vk_id(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = ContentDataFormat.convert_to_format(data[0])
        assert result["content_vk_id"] == expected_data[0]["post"]["post_id"]

    def test_content_group_id_fk(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = ContentDataFormat.convert_to_format(data[0])
        assert result["group_id_fk"] == expected_data[0]["post"]["group_id"]


class TestsPostsDataFormat:
    def test_public_url(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = PostsDataFormat.convert_to_format(data[0])
        assert result["url"] == expected_data[0]["post"]["url"]

    def test_text(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = PostsDataFormat.convert_to_format(data[0])
        assert result["text"] == expected_data[0]["post"]["text"]

    def test_text_post(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = PostsDataFormat.convert_to_format(data[0])
        assert result["content_fk"] == expected_data[0]["post"]["post_id"]


class TestsCarouselDataFormat:
    def test_text(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = CarouselDataFormat.convert_to_format(data[1])
        assert result["text"] == expected_data[0]["carousel"]["text"]

    def test_text_carousel(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = CarouselDataFormat.convert_to_format(data[1])
        assert result["content_fk"] == expected_data[0]["carousel"]["post_id"]

    def test_text_url(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = CarouselDataFormat.convert_to_format(data[1])
        assert result["url"] == expected_data[0]["carousel"]["url"]

    def test_text_url1(self, executor_for_convert):
        data = executor_for_convert.get_all_data()
        result = CarouselDataFormat.convert_to_format(data[1])
        assert result["url1"] == expected_data[0]["carousel"]["url1"]


class TestsContentDataChecker:
    def test_is_two_links(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = ContentDataChecker.is_properly(data)
        assert result is True

    def test_is_less_then_one_link(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = ContentDataChecker.is_properly(data)
        assert result is False


class TestsContentUniqueChecker:
    def test_post_id_in_list(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = ContentUniqueChecker.is_unique(
            data, [expected_data[0]["post"]["post_id"]]
        )
        assert result is False

    def test_post_id_not_in_list(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = ContentUniqueChecker.is_unique(data, [12345789])
        assert result is True


class TestsContentProperAndUnique:
    def test_proper_and_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = ContentProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is True

    def test_not_proper_and_is_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = ContentProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is False

    def test_proper_and_is_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = ContentProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["carousel"]["post_id"]]
        )
        assert result is False

    def test_not_proper_and_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = ContentProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["post"]["post_id"]]
        )
        assert result is False


class TestsPostDataChecker:
    def test_is_two_links(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = PostDataChecker.is_properly(data)
        assert result is False

    def test_is_less_then_one_link(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = PostDataChecker.is_properly(data)
        assert result is True


class TestsPostsProperAndUnique:
    def test_proper_and_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = PostsProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is True

    def test_not_proper_and_is_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = PostsProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is False

    def test_proper_and_is_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = PostsProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["post"]["post_id"]]
        )
        assert result is False

    def test_not_proper_and_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = PostsProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["post"]["post_id"]]
        )
        assert result is False


class TestsCarouselDataChecker:
    def test_is_two_links(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = CarouselDataChecker.is_properly(data)
        assert result is False

    def test_is_less_then_one_link(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = CarouselDataChecker.is_properly(data)
        assert result is True


class TestsCarouselProperAndUnique:
    def test_proper_and_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = CarouselProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is True

    def test_not_proper_and_is_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = CarouselProperAndUnique().is_properly(
            data=data, content_ids=[12345789]
        )
        assert result is False

    def test_proper_and_is_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[1]
        result = CarouselProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["carousel"]["post_id"]]
        )
        assert result is False

    def test_not_proper_and_not_unique(self, executor_for_convert):
        data = executor_for_convert.get_all_data()[0]
        result = CarouselProperAndUnique().is_properly(
            data=data, content_ids=[expected_data[0]["post"]["post_id"]]
        )
        assert result is False
