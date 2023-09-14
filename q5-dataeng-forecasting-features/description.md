**Question**

You will be given some time series sales data including product, categories and stores. Please write a python script that calculates the following features. It would be a bonus if you can employ OOP principles (using class definitions, inheritence, data abstraction) whereever possible in your implementation.

Product Features:
- Moving average of sales of the product in the past 7 days (MA7_P)
- Lag features: sales of the product on the same day last week (LAG7_P)
Brand aggregations:
- Moving average of total sales of all the products from the same brand and store group in the past 7 days (MA7_B)
- Lag features: total sales for the same brand and store group on the same day last week  (LAG7_B)
Store aggregations:
- Moving average of sales from the same store in the past 7 days (MA7_S)
- Lag features: total sales for the same store on the same day last week  (LAG7_S)


First output will be the dataframe with the following schema: 
"features.csv"
- [product_id,store_id,brand_id,date,sales_product,MA7_P,LAG7_P,sales_brand,MA7_B,LAG7_B,sales_store,MA7_S,LAG7_S]

Second output will be the dataframe that contains WMAPE info for each product-brand-store group calculated based on MA7_P (forecast) with sales_product (actual) values. Please see  https://en.wikipedia.org/wiki/WMAPE for metric definition.
- [product_id,store_id,brand_id,WMAPE]

Please feel free to use any relevant python libraries and built-in functions (pandas, numpy, etc.) for your implementation.


**Input Data Format**

brand.csv: 
- id: id of the brand
- name: brand name

product.csv
- id: identifier of the product
- name: name of the product
- brand: brand of the product

store.csv
- id: identifier of the store
- name: name of the store
- city: city that the store is located in

sales.csv
- product: identifier of the product (id column in product.csv)
- store: identifier of the store (id column in store.csv)
- date: date of sale
- quantity: sales quantity of the specified product in the specified store

**Arguments**

Your script should take following arguments from command line and process the data (inclusive) based on given date range.
- "--min-date": start of the date range. type:str, format:"YYYY-MM-DD", default:"2021-01-08"
- "--max-date": end of the date range. type:str, format:"YYYY-MM-DD", default:"2021-05-30"
- "--top": number of rows in the WMAPE output. type:int, default:5

Expected command and output:
- The first output should be sorted by product_id, brand_id, store_id, date in ascending order and contain all products.
- The second output should be sorted by WMAPE in descending order and contain top N products given as --top argument.

```
$ python3 solution.py --min-date 2021-01-08 --max-date 2021-05-30 --top 5

--Output1 to be written to: features.csv--
[product_id,store_id,brand_id,date,sales_product,MA7_P,LAG7_P,sales_brand,MA7_B,LAG7_B,sales_store,MA7_S,LAG7_S]
...
...
0,0,0,2021-01-08,10,11.42857143,6,40,28.57142857,21,63,46,39
0,0,0,2021-01-09,10,12,19,24,31.28571429,29,41,49.42857143,48
...
...

--Output2 to be written to: mapes.csv--
[product_id,store_id,brand_id,WMAPE]
1,0,0,0.708686
3,2,0,0.630778
2,3,1,0.607483
..
..
```

**Explanation of Features**

Example for product_id: 0, brand_id:0, store_id:0
- sales_product (2021-01-08): 10 => total sales of product-brand-store in the corresponding date (2021-01-08)
- MA7_P (2021-01-08): 11.43 => average of sales of product-brand-store in the past 7 days - avg of sales_product between [2021-01-01 - 2021-01-07]
- LAG7_P (2021-01-08): 6 => value of sales_product before 7 days (2021-01-01)

- sales_brand (2021-01-08): 40 => total sales of brand-store in the corresponding date (2021-01-08)
- MA7_B (2021-01-08): 28.57 => average of sales of brand-store in the past 7 days - avg of sales_brand between [2021-01-01 - 2021-01-07]
- LAG7_B (2021-01-08): 21 => value of sales_brand before 7 days (2021-01-01)

- sales_store (2021-01-08): 63 => total sales of store in the corresponding date (2021-01-08)
- MA7_S (2021-01-08): 46 => average of sales of product-brand-store in the past 7 days - avg of sales_store between [2021-01-01 - 2021-01-07]
- LAG7_S (2021-01-08): 39 => value of sales_store before 7 days (2021-01-01)

