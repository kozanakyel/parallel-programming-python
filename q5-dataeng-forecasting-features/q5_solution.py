from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
import abc


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


class Config:
    OS_ABS_PATH = os.getcwd()
    DATA_PATH = "/q5-dataeng-forecasting-features/input_data/data"
    DATA_FOLDER = OS_ABS_PATH + DATA_PATH


class SalesService:
    pass


class TechnicalAnalysisService:
    ...


class FileReader(abc.ABC):
    @abc.abstractmethod
    def create_list():
        return NotImplementedError

    def read_data(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(os.path.join(Config.DATA_FOLDER, filename))


class BrandServices(FileReader):
    def __init__(self):
        self.brand_list = self.create_list()

    def create_list(self):
        brand_list = []
        df = super().read_data("brand.csv")
        for index, row in df.iterrows():
            brand = Brand(id=str(row["id"]), name=row["name"])
            brand_list.append(brand)
        return brand_list


class ProductServices(FileReader):
    def __init__(self, brand_list):
        self.brand_list = brand_list
        self.product_list = self.create_list()

    def create_list(self):
        product_list = []
        df = super().read_data("product.csv")
        for index, row in df.iterrows():
            brand_of_product = self.get_brand_by_name(row["brand"])
            product = Product(
                id=str(row["id"]), name=row["name"], brand=brand_of_product
            )
            product_list.append(product)
        return product_list

    def get_brand_by_name(self, name):
        for brand in self.brand_list:
            if brand.name == name:
                return brand
        return None


class StoreServices(FileReader):
    def __init__(self):
        self.store_list = self.create_list()

    def create_list(self):
        store_list = []
        df = super().read_data("store.csv")
        for index, row in df.iterrows():
            store = Store(id=str(row["id"]), name=row["name"], city=row["city"])
            store_list.append(store)
        return store_list


class OutputService:
    ...


if __name__ == "__main__":
    bs = BrandServices()
    ps = ProductServices(bs.brand_list)
    ss = StoreServices()
    print(ss.store_list)
