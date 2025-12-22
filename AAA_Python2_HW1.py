import json
import keyword


class ColorizeMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'repr_color_code'):
            cls.repr_color_code = ColorizeMixin.repr_color_code

    def __str__(self) -> str:
        if hasattr(self, 'price') and self.price:
            return (f'\033[0;{self.repr_color_code}m{self.title} '
                    f'| {self.price} ₽\033[0m')
        return f'\033[0;{self.repr_color_code}m{self.title} | 0 ₽\033[0m'


class Attributes:
    def __init__(self, data):
        for key, value in data.items():
            if key == 'price':
                continue
            if keyword.iskeyword(key):
                key = key + '_'
            if isinstance(value, dict):
                value = Attributes(value)
            setattr(self, key, value)


class Advert(ColorizeMixin, Attributes):
    repr_color_code = 33

    def __init__(self, data):
        if 'title' not in data:
            raise ValueError('There is no field "title".')
        super().__init__(data)
        self.price = data.get('price', 0)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError('Price must be >= 0.')
        self._price = value


if __name__ == '__main__':
    example_1 = '''{
        "title": "iPhone X",
        "price": 100,
        "location": {
            "address": "город Самара, улица Мориса Тореза, 50",
            "metro_stations": ["Спортивная", "Гагаринская"]
            }
        }'''
    phone = json.loads(example_1)
    phone_ad = Advert(phone)
    print(phone_ad)
    print(phone_ad.location.address)
    print(phone_ad.price)

    example_2 = '''{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs"
        }'''
    dog = json.loads(example_2)
    dog_ad = Advert(dog)
    print(dog_ad)
    print(dog_ad.class_)
