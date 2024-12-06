import pandas as pd

##Read csv
def load_data():
    brands_url = "https://drive.google.com/file/d/1m1ThDDIYRTTii-rqM5SEQjJ8McidJskD/view?usp=sharing"
    orderlines_url = "https://drive.google.com/file/d/1FYhN_2AzTBFuWcfHaRuKcuCE6CWXsWtG/view?usp=sharing"
    orders_url = "https://drive.google.com/file/d/1Vu0q91qZw6lqhIqbjoXYvYAQTmVHh6uZ/view?usp=sharing"
    products_url = "https://drive.google.com/file/d/1afxwDXfl-7cQ_qLwyDitfcCx3u7WMvkU/view?usp=sharing"

    def read_url(share_url):
        return pd.read_csv("https://drive.google.com/uc?export=download&id="+share_url.split("/")[-2])

    brands_df = read_url(brands_url)
    orderlines_df = read_url(orderlines_url)
    orders_df = read_url(orders_url)
    products_df = read_url(products_url)
    return brands_df, orderlines_df, orders_df, products_df

