from dataclasses import dataclass


@dataclass
class Brand:
    id: str
    name: str

@dataclass        
class Product:
    id: str
    name: str
    brand: Brand

@dataclass        
class Store:
    id: str
    name: str
    city: str

@dataclass       
class Sales:
    product: Product
    store: Store
    date: str
    quantity: int


if __name__ == '__main__':
    b = Brand('1', 'bb')
    p = Product('2', 'pp', b)
    print(b.id, p)   