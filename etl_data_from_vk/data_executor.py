from dataclasses import dataclass, field


@dataclass
class VkData:
    group_id: int = 0
    post_id: int = 0
    public_date: int = 0
    url: list = field(default_factory=list)
    text: str = ""


class DataExecuter:
    """Execute data from vk json"""

    def __init__(self, data: dict) -> None:
        self.data = data

    def get_all_links(self, data):
        for val in data:
            if val.get("type") == "x":
                return val.get("url")

    def get_data_from_vk_json(
        self, data: dict, saved_data=None
    ) -> list[VkData]:
        saved_data = VkData()
        urls = []
        for _, d in enumerate(data["attachments"]):
            saved_data.text = data.get("text", "")
            saved_data.public_date = data.get("date", 0)
            if not saved_data.post_id and d.get("photo"):
                saved_data.post_id = d.get("photo").get("id")
                saved_data.group_id = abs(d.get("photo").get("owner_id"))
            if d.get("photo"):
                urls.append(self.get_all_links(d.get("photo").get("sizes")))
        counter = 0
        url_dict = {}
        for url in urls:
            if not counter:
                url_dict.update({"url": url})
            else:
                url_dict.update({f"url{counter}": url})
            counter += 1
        saved_data.url.append(url_dict)

        return saved_data

    def get_all_data(self):
        saved = []
        for item in self.data:
            for i, _ in enumerate(item["response"]["items"]):
                if (
                    item["response"]["items"][i]["attachments"]
                    and item["response"]["items"][i]["attachments"][0].get(
                        "type"
                    )
                    != "video"
                ):
                    saved.append(
                        self.get_data_from_vk_json(
                            item["response"]["items"][i]
                        )
                    )
        self.gotten_data = saved
        return saved
