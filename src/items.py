from dataclasses import dataclass
from exceptions import EmptyProductFieldError


@dataclass
class BaseItem:
    def __post_init__(self):
        """
        Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if (method := getattr(self, f"validate_{name}", None)):
                setattr(self, name, method(getattr(self, name), field=field))


@dataclass
class WbSubSubcategoryItem(BaseItem):
    """
    Wildberries subsubcategory (filter) information:
        name: name of filter,
        link: link to the page with the product of the filter,
        num_of_goods: number of products with the filter
        type: item type
    """
    name: str
    url: str
    num_of_goods: int
    type: str = "wb_subsubcategory"

    def validate_name(self, name: list, **_) -> list:
        if not name:
            raise EmptyProductFieldError("Empty name")
        return name

    def validate_num_of_goods(self, num_of_goods: list, **_) -> list:
        if not num_of_goods:
            raise EmptyProductFieldError("Empty number of goods")
        return num_of_goods