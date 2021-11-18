from weakref import WeakKeyDictionary
import json

class Resistor():
    def __init__(self, ohms) -> None:
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

class VoltageResistance(Resistor):
    def __init__(self, ohms) -> None:
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class Grade():
    def __init__(self) -> None:
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygen(object, metaclass=ValidatePolygon):
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygen):
    sides = 3


class BetterSerializable():
    def __init__(self, *args) -> None:
        self.args = args
        
    def serialize(self):
        return json.dumps({
            'class' : self.__class__.__name__,
            'args' : self.args,
        })

    def __repr__(self):
        return '{}{}'.format(self.__class__.__name__, self.args)

registry = {}
def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserizlize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    print(*params['args'])
    print(type(params['args']))
    return target_class(*params['args'])

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class EvenBetterPoint2D(BetterSerializable, metaclass=Meta):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.x = x
        self.y = y

class Field():
    def __init__(self) -> None:
        self.name = None
        self.internal_name = None

class FieldMeta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DataBaseRoow(metaclass=FieldMeta):
    pass


