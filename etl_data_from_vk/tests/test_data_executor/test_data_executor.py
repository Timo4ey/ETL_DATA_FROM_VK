from etl_data_from_vk.data_executor import VkData
from etl_data_from_vk.tests.conftest import get_test_data

test_data = get_test_data("test_data_executor/raw_data.json")

expected_data = get_test_data("test_data_executor/expected_data.json")[0]


class TestsDataExecuter:
    def test_get_all_links(self, executor):
        assert (
            executor.get_all_links(test_data[2]["sizes"])
            == expected_data["post"]["url"][0]
        )

    def test_get_data_from_vk_json_type_is_vk_data(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert isinstance(result, VkData)

    def test_get_data_from_vk_json_group_id(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert result.group_id == expected_data["post"]["group_id"]

    def test_get_data_from_vk_json_post_id(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert result.post_id == expected_data["post"]["post_id"]

    def test_get_data_from_vk_json_public_date(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert result.public_date == expected_data["post"]["public_date"]

    def test_get_data_from_vk_json_url(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert result.url[0].get("url") == expected_data["post"]["url"][0]

    def test_get_data_from_vk_json_text(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[0]["response"]["items"][0]
        )
        assert result.text == expected_data["post"]["text"]

    def test_get_data_from_vk_json_url_carousels(self, executor):
        result = executor.get_data_from_vk_json(
            test_data[1]["response"]["items"][0]
        )
        assert list(result.url[0].values()) == expected_data["carousel"]["url"]
