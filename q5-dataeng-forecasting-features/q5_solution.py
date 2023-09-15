from dataclasses import dataclass
import numpy as np
import pandas as pd
import os
import abc
from datetime import datetime


@dataclass
class Brand:
    id: int
    name: str


@dataclass
class Product:
    id: int
    name: str
    brand: Brand


@dataclass
class Store:
    id: int
    name: str
    city: str


@dataclass
class Sales:
    product: Product
    store: Store
    date: datetime
    quantity: int


class Config:
    OS_ABS_PATH = os.getcwd()
    DATA_PATH = "/q5-dataeng-forecasting-features/input_data/data"
    DATA_FOLDER = OS_ABS_PATH + DATA_PATH
    MIN_DATE = "2021-01-08"
    MAX_DATE = "2021-05-30"
    TOP = 5




class FileReader(abc.ABC):
    @abc.abstractmethod
    def create_list(self):
        return NotImplementedError

    @abc.abstractmethod
    def create_df(self):
        return NotImplementedError

    def read_data(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(os.path.join(Config.DATA_FOLDER, filename))


class BrandServices(FileReader):
    def __init__(self):
        self.brand_df = self.create_df()
        self.brand_list = self.create_list()

    def create_list(self):
        brand_list = []
        for index, row in self.brand_df.iterrows():
            brand = Brand(id=row["id"], name=row["name"])
            brand_list.append(brand)
        return brand_list

    def create_df(self):
        return super().read_data("brand.csv")


class ProductServices(FileReader):
    def __init__(self, brand_list):
        self.brand_list = brand_list
        self.product_df = self.create_df()
        self.product_list = self.create_list()

    def create_list(self):
        product_list = []
        for index, row in self.product_df.iterrows():
            brand_of_product = self.get_brand_by_name(row["brand"])
            product = Product(
                id=row["id"], name=row["name"], brand=brand_of_product
            )
            product_list.append(product)
        return product_list

    def create_df(self):
        return super().read_data("product.csv")

    def get_brand_by_name(self, name):
        for brand in self.brand_list:
            if brand.name == name:
                return brand
        return None


class StoreServices(FileReader):
    def __init__(self):
        self.store_df = self.create_df()
        self.store_list = self.create_list()

    def create_list(self):
        store_list = []
        for index, row in self.store_df.iterrows():
            store = Store(id=row["id"], name=row["name"], city=row["city"])
            store_list.append(store)
        return store_list

    def create_df(self):
        return super().read_data("store.csv")


class SalesService(FileReader):
    def __init__(self, product_list, store_list):
        self.product_list = product_list
        self.store_list = store_list
        self.sales_df = self.create_df()
        self.sales_list = self.create_list()

    def create_list(self):
        sales_list = []
        for index, row in self.sales_df.iterrows():
            product_of_sales = self.get_product_by_id(row["product"])
            store_of_sales = self.get_store_by_id(row["store"])
            sales = Sales(
                product=product_of_sales,
                store=store_of_sales,
                date=row["date"],
                quantity=row["quantity"],
            )
            sales_list.append(sales)
        return sales_list

    def create_df(self):
        df = super().read_data("sales.csv")
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        return df

    def get_store_by_id(self, id):
        for store in self.store_list:
            if store.id == id:
                return store
        return None

    def get_product_by_id(self, id):
        for product in self.product_list:
            if product.id == id:
                return product
        return None



class TAService:
    @staticmethod
    def calculate_7_day_rolling_average(group, col_name, sales_name):
        group[col_name] = group[sales_name].shift(fill_value=0).rolling(window=7, min_periods=1).mean()
        return group

class OutputService:
    def __init__(self, sales_service):
        self.sales_service = sales_service

    def add_brand_id(self, df):
        self.output = df.copy()
        self.output["brand_id"] = df["product"].apply(
            lambda product_id: self.sales_service.get_product_by_id(product_id).brand.id
        )
        
    def add_sales_product(self):
        self.output = self.output.rename(columns={'quantity': 'sales_product'})

    def add_MA7_P(self):     
        self.output['date'] = pd.to_datetime(self.output['date'])
        grouped = self.output.groupby(['product', 'brand_id', 'store'])
        self.output = grouped.apply(TAService.calculate_7_day_rolling_average, 'MA7_P', 'sales_product')
        self.output = self.output.reset_index(drop=True)
        
    def add_LAG7_P(self):
        grouped = self.output.groupby(['product', 'brand_id', 'store'])
        self.output['LAG7_P'] = grouped['sales_product'].shift(periods=7)
        self.output = self.output.reset_index(drop=True)
        
    def add_sales_brand(self):
        grouped = self.output.groupby(['brand_id', 'store', 'date'])
        result = grouped['sales_product'].sum().reset_index()
        result = result.rename(columns={'sales_product': 'sales_brand'})
        self.output = self.output.merge(result, on=['brand_id', 'store', 'date'], how='left')

    def add_MA7_B(self):     
        self.output['date'] = pd.to_datetime(self.output['date'])
        grouped = self.output.groupby(['brand_id', 'store'])
        self.output = grouped.apply(TAService.calculate_7_day_rolling_average, 'MA7_B', 'sales_brand')
        self.output = self.output.reset_index(drop=True)
        
    def add_LAG7_B(self):
        grouped = self.output.groupby(['brand_id', 'store'])
        self.output['LAG7_B'] = grouped['sales_brand'].shift(periods=7)
        self.output = self.output.reset_index(drop=True)
        
    def add_sales_store(self):
        grouped = self.output.groupby(['store', 'date'])
        result = grouped['sales_product'].sum().reset_index()
        result = result.rename(columns={'sales_product': 'sales_store'})
        self.output = self.output.merge(result, on=['store', 'date'], how='left')

    def add_MA7_S(self):     
        self.output['date'] = pd.to_datetime(self.output['date'])
        grouped = self.output.groupby(['product', 'brand_id', 'store'])
        self.output = grouped.apply(TAService.calculate_7_day_rolling_average, 'MA7_S', 'sales_store')
        self.output = self.output.reset_index(drop=True)
        
    def add_LAG7_S(self):
        grouped = self.output.groupby(['store'])
        self.output['LAG7_S'] = grouped['sales_store'].shift(periods=7)
        self.output = self.output.reset_index(drop=True)
    
    def col_organize(self):
        self.output = self.output.rename(columns={'product': 'product_id', 
                                                  'store': 'store_id'})
        col_order = ['product_id','store_id','brand_id','date','sales_product',
                     'MA7_P','LAG7_P','sales_brand','MA7_B','LAG7_B',
                     'sales_store','MA7_S','LAG7_S']
        self.output = self.output[col_order]
        
    def calculate_WMAPE(self):
        df = self.output.copy()
        df['APE'] = abs((df['sales_product'] - df['MA7_P']) / df['sales_product']) * 100
        df['WAPE'] = df['APE'] * df['sales_product']
        grouped = df.groupby(['product_id', 'store_id', 'brand_id'])

        result_df = pd.DataFrame()
        result_df['WAPE'] = grouped['WAPE'].sum()
        result_df['sales_product'] = grouped['sales_product'].sum()
        result_df['WMAPE'] = (result_df['WAPE'] / result_df['sales_product']).fillna(0)

        result_df = result_df.drop(['WAPE', 'sales_product'], axis=1)
        result_df = result_df.sort_values(by='WMAPE', ascending=False)
        return result_df

if __name__ == "__main__":
    bs = BrandServices()
    ps = ProductServices(bs.brand_list)
    ss = StoreServices()
    sss = SalesService(ps.product_list, ss.store_list)
    out = OutputService(sss)
    out.add_brand_id(sss.sales_df)
    out.add_sales_product()
    out.add_MA7_P()
    out.add_LAG7_P()
    out.add_sales_brand()
    out.add_MA7_B()
    out.add_LAG7_B()
    out.add_sales_store()
    out.add_MA7_S()
    out.add_LAG7_S()
    out.col_organize()
    r = out.calculate_WMAPE()
    print(r.head(10))
    print(out.output.head(10))
