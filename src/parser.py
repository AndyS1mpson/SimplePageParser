import re
from scrapy import Selector
from items import WbSubSubcategoryItem


class WbPageParser:

    content_block_selector = ".xsubject"

    def __get_filter_name(self, selector) -> str:
        filter_info = selector.xpath('text()').get()
        if not filter_info:
            return
        return re.findall(
            r"[а-яА-ЯёЁa-zA-Z\s]+(?=\()",
            filter_info
        )[0].strip()

    def __get_num_of_goods(self, selector) -> int:
        filter_info = selector.xpath('text()').get()
        if not filter_info:
            return
        r_num_of_goods: str = re.findall(
            r"(?<=\()[0-9\s]+(?=\))",
            filter_info
        )[0]
        return int(r_num_of_goods.replace('\xa0', ''))

    def __get_filter_num(self, selector) -> int:
        return selector.css("::attr(data-value)").get()

    def parse(self, url: str, content: str) -> list:
        selector = Selector(text=content)
        sscategory_labels = selector.xpath(
            f"//div[@id='filters']"
            f"//div[contains(@class, 'xsubject')]"
            f"//fieldset[contains(@class, 'xsubject')]//label"
        )

        filters = []

        for label in sscategory_labels:
            filters.append(
                WbSubSubcategoryItem(
                    name=self.__get_filter_name(label),
                    url=url + f"&xsubject={self.__get_filter_num(label)}",
                    num_of_goods=self.__get_num_of_goods(label),
                )
            )

        return filters
