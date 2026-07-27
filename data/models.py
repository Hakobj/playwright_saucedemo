from dataclasses import dataclass

@dataclass(frozen=True)     # frozen = immutable; test data shouldn't mutate mid-run
class User:
    username: str
    password: str

@dataclass(frozen=True)
class Product:
    name: str
    price: str
