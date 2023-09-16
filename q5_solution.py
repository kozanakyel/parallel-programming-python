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
            product = Product(id=row["id"], name=row["name"], brand=brand_of_product)
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


class TAHelper:
    @staticmethod
    def calculate_7_day_rolling_average(group, col_name, sales_name):
        group[col_name] = (
            group[sales_name]
            .shift(fill_value=0)
            .rolling(window=7, min_periods=1)
            .mean()
        )
        return group

    @staticmethod
    def calculate_WMAPE(dataframe):
        """_
        NEED: require a fix issue for calculation,
        because we dont match the desired example output!!!
        """
        df = dataframe.copy()
        df["APE"] = abs((df["sales_product"] - df["MA7_P"]) / df["sales_product"]) * 100
        df["WAPE"] = df["APE"] * df["sales_product"]
        grouped = df.groupby(["product_id", "store_id", "brand_id"])

        result_df = pd.DataFrame()
        result_df["WAPE"] = grouped["WAPE"].sum()
        result_df["sales_product"] = grouped["sales_product"].sum()
        result_df["WMAPE"] = (result_df["WAPE"] / result_df["sales_product"]).fillna(0)
        result_df.reset_index(inplace=True)

        result_df = result_df.drop(["WAPE", "sales_product"], axis=1)
        result_df = result_df.sort_values(by="WMAPE", ascending=False)

        return result_df


class DataPipeline:
    def __init__(self, sales_service):
        self.sales_service = sales_service
        self.output = sales_service.sales_df.copy()
        self.ta_helper = TAHelper()
        self.output["date"] = pd.to_datetime(self.output["date"])

    def add_brand_id(self, df):
        self.output["brand_id"] = df["product"].apply(
            lambda product_id: self.sales_service.get_product_by_id(product_id).brand.id
        )

    def add_sales_product(self):
        self.output = self.output.rename(columns={"quantity": "sales_product"})

    def calculate_MA7(self, group, col_name, calc_col):
        grouped = self.output.groupby(group)
        self.output = grouped.apply(
            self.ta_helper.calculate_7_day_rolling_average, col_name, calc_col
        )
        self.output = self.output.reset_index(drop=True)

    def calculate_LAG7(self, group, col_name, calc_col):
        grouped = self.output.groupby(group)
        self.output[col_name] = grouped[calc_col].shift(periods=7)
        self.output = self.output.reset_index(drop=True)

    def add_MA7_P(self):
        self.calculate_MA7(
            group=["product", "brand_id", "store"],
            col_name="MA7_P",
            calc_col="sales_product",
        )

    def add_LAG7_P(self):
        self.calculate_LAG7(
            group=["product", "brand_id", "store"],
            col_name="LAG7_P",
            calc_col="sales_product",
        )

    def add_sales_brand(self):
        grouped = self.output.groupby(["brand_id", "store", "date"])
        result = grouped["sales_product"].sum().reset_index()
        result = result.rename(columns={"sales_product": "sales_brand"})
        self.output = self.output.merge(
            result, on=["brand_id", "store", "date"], how="left"
        )

    def add_MA7_B(self):
        self.calculate_MA7(
            group=["brand_id", "store"],
            col_name="MA7_B",
            calc_col="sales_brand",
        )

    def add_LAG7_B(self):
        self.calculate_LAG7(
            group=["brand_id", "store"], col_name="LAG7_B", calc_col="sales_brand"
        )

    def add_sales_store(self):
        grouped = self.output.groupby(["store", "date"])
        result = grouped["sales_product"].sum().reset_index()
        result = result.rename(columns={"sales_product": "sales_store"})
        self.output = self.output.merge(result, on=["store", "date"], how="left")

    def add_MA7_S(self):
        self.calculate_MA7(
            group=["product", "brand_id", "store"],
            col_name="MA7_S",
            calc_col="sales_tore",
        )

    def add_LAG7_S(self):
        self.calculate_LAG7(group=["store"], col_name="LAG7_S", calc_col="sales_store")

    def col_organize(self):
        self.output = self.output.rename(
            columns={"product": "product_id", "store": "store_id"}
        )
        col_order = [
            "product_id",
            "store_id",
            "brand_id",
            "date",
            "sales_product",
            "MA7_P",
            "LAG7_P",
            "sales_brand",
            "MA7_B",
            "LAG7_B",
            "sales_store",
            "MA7_S",
            "LAG7_S",
        ]
        self.output = self.output[col_order]

    def create_WMAPE(self):
        wmape_df = self.ta_helper.calculate_WMAPE(self.output)
        return wmape_df


class OutputService:
    def __init__(self):
        bs = BrandServices()
        ps = ProductServices(bs.brand_list)
        ss = StoreServices()
        sss = SalesService(ps.product_list, ss.store_list)
        self.pipeline = DataPipeline(sss)
        self.pipeline.add_brand_id(sss.sales_df)
        self.pipeline.add_sales_product()
        self.pipeline.add_MA7_P()
        self.pipeline.add_LAG7_P()
        self.pipeline.add_sales_brand()
        self.pipeline.add_MA7_B()
        self.pipeline.add_LAG7_B()
        self.pipeline.add_sales_store()
        self.pipeline.add_MA7_S()
        self.pipeline.add_LAG7_S()
        self.pipeline.col_organize()
        self.df = self.pipeline.output

    def get_wmape_df(self, top=Config.TOP):
        return self.pipeline.create_WMAPE().head(top)

    def create_args_parser(self):
        import argparse

        parser = argparse.ArgumentParser(description="Filter data based on date range.")
        parser.add_argument(
            "--min-date",
            type=str,
            default=Config.MIN_DATE,
            help="Start of the date range.",
        )
        parser.add_argument(
            "--max-date",
            type=str,
            default=Config.MAX_DATE,
            help="End of the date range.",
        )
        parser.add_argument(
            "--top", type=int, default=Config.TOP, help="Exceed max index."
        )
        args = parser.parse_args()
        return args

    def run(self):
        args = self.create_args_parser()
        min_date_available = pd.to_datetime(Config.MIN_DATE)
        max_date_available = pd.to_datetime(Config.MAX_DATE)
        args.min_date = pd.to_datetime(args.min_date)
        args.max_date = pd.to_datetime(args.max_date)

        if args.min_date < min_date_available or args.max_date > max_date_available:
            print(
                f"Error: Date range must be within {min_date_available} to {max_date_available}."
            )
        else:
            mask = (self.df["date"] >= args.min_date) & (
                self.df["date"] <= args.max_date
            )
            filtered_df = self.df[mask]
            filtered_df.to_csv("feature.csv", index=False)

            k = self.get_wmape_df(top=args.top)
            k.to_csv("mapes.csv", index=False)


if __name__ == "__main__":
    output_service = OutputService()
    output_service.run()
