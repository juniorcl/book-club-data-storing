# -------------------------------------------------------------------
#   IMPORTS
#
# - Import re 
# -------------------------------------------------------------------
import re
import requests

import pandas as pd

from bs4        import BeautifulSoup
from airflow    import DAG
from datetime   import datetime, timedelta
from sqlalchemy import create_engine

from airflow.operators.python_operator import PythonOperator


# -------------------------------------------------------------------
#   CONFIG
#
# - Import re 
# -------------------------------------------------------------------
default_args = {
    'owner': 'Book Store',
    'start_date': datetime(2021, 11, 26),
    'email': "clebiomojunior@gmail.com",
    'email_on_failure':True,
    'email_on_retry':True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past':False
}


# -------------------------------------------------------------------
#   FUNCIONS
#
# - Import re 
# -------------------------------------------------------------------
def webscraping():

    url = 'https://books.toscrape.com/' # defining url
    r = requests.get(url) # getting the text

    soup = BeautifulSoup(r.text, 'html.parser') # creating the soup object

    # dict to store the books informations
    dict_product = {
        'scraping_time': [],
        'category': [],
        'title': [],
        'price': [],
        'star_rating': [],
        'description': [],
        'upc': [],
        'type': [],
        'price_excl_tax': [],
        'price_incl_tax': [],
        'tax': [],
        'availability': [],
        'number_reviews': []
    }


    list_categories = soup.find('ul', class_='').find_all('a', class_='') # getting book categories


    for l in list_categories:
        
        category_url = url.replace('index.html', '') + l['href'].replace('../', '')
        r_ = requests.get(category_url, 'html.parser')

        soup_ = BeautifulSoup(r_.text)
        pages_of_ = 'Page 1 of 1' if soup_.find('li', class_='current') is None else soup_.find('li', class_='current').text

        number_of_pages = re.search(r'\w+\s(\d+)\s\w{2}\s(\d+)', pages_of_)
        max_num_page= int(number_of_pages.group(2))


        for i in range(1, max_num_page + 1):

            pages_link = category_url if i == 1 else category_url.replace('index', f'page-{i}')
            r__ = requests.get(pages_link)
            
            soup__ = BeautifulSoup(r__.text, 'html.parser')
            book_list = soup__.find_all('div', class_="image_container")


            for b in book_list:

                # Book Link
                book_link = b.find('a')['href']
                complete_book_link = 'http://books.toscrape.com/' + book_link.replace('../../../', 'catalogue/')

                # Book Page
                r___ = requests.get(complete_book_link)
                book_page = BeautifulSoup(r___.text, 'html.parser')

                # first block of info
                first_block = book_page.find('div', class_="col-sm-6 product_main")
                
                title = first_block.find('h1').text
                price = first_block.find('p', class_='price_color').text
                num_star = first_block.find('p', class_='star-rating')['class'][1]

                # second block of info
                description_block = book_page.find('article', class_='product_page')
                product_description = None if description_block.find('p', class_='') is None else description_block.find('p', class_='').text
                
                product_information_block = book_page.find_all('td', class_='')

                # book informations
                upc = product_information_block[0].text
                product_type = product_information_block[1].text
                price_excl_tax = product_information_block[2].text
                price_incl_tax = product_information_block[3].text
                tax = product_information_block[4].text
                availability = product_information_block[5].text
                number_reviews = product_information_block[6].text
                
                # Storing into dict
                dict_product['scraping_time'].append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                dict_product['category'].append(l.text)
                dict_product['title'].append(title)
                dict_product['price'].append(price)
                dict_product['star_rating'].append(num_star)
                dict_product['description'].append(product_description)
                dict_product['upc'].append(upc)
                dict_product['type'].append(product_type)
                dict_product['price_excl_tax'].append(price_excl_tax)
                dict_product['price_incl_tax'].append(price_incl_tax)
                dict_product['tax'].append(tax)
                dict_product['availability'].append(availability)
                dict_product['number_reviews'].append(number_reviews)

    return pd.DataFrame(dict_product)


def data_cleaning(**context):

    # using data product from webscraping function
    df_product = context['task_instance'].xcom_pull(task_ids='webscraping')

    # extract the category name
    df_product['category'] = df_product['category'].str.extract(r'(\w+\s?\w+\s?\w+)')
    df_product['category'] = df_product['category'].str.replace(' ', '_')
    df_product['category'] = df_product['category'].str.lower()

    # repacing star rating from string to integer
    df_product['star_rating'] = df_product['star_rating'].replace({'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5})

    # type to lower
    df_product['type'] = df_product['type'].str.lower()

    # extracting number
    df_product['price'] = df_product['price'].str.extract(r'(\d+.\d+)')
    df_product['price'] = df_product['price'].astype(float)

    df_product['price_excl_tax'] = df_product['price_excl_tax'].str.extract(r'(\d+.\d+)')
    df_product['price_excl_tax'] = df_product['price_excl_tax'].astype(float)

    df_product['price_incl_tax'] = df_product['price_incl_tax'].str.extract(r'(\d+.\d+)')
    df_product['price_incl_tax'] = df_product['price_incl_tax'].astype(float)

    df_product['tax'] = df_product['tax'].str.extract(r'(\d+.\d+)')
    df_product['tax'] = df_product['tax'].astype(float)

    # available
    df_product['availability_stock'] = df_product['availability'].str.extract(r'(\w+\s\w+) \(\d+ \w+\)')
    df_product['availability_stock'] = df_product['availability_stock'].str.lower().str.replace(' ', '_')

    df_product['availability_number'] = df_product['availability'].str.extract(r'\w+ \w+ \((\d+) \w+\)')
    df_product['availability_number'] = df_product['availability_number'].astype(int)

    # number of reviwes
    df_product['number_reviews'] = df_product['number_reviews'].astype(int)

    # drop columns
    df_product = df_product.drop(columns=['availability'])

    return df_product


def inserting(**context):

    # using data product from webscraping function
    df_product = context['task_instance'].xcom_pull(task_ids='data_cleaning')

    # connecting with bookclub_dp.sqlite
    engine = create_engine('sqlite:////opt/airflow/db', echo=False)
    conn = engine.connect()

    # inserting
    df_product.to_sql('book', con=conn, if_exists='append', index=False)


# -------------------------------------------------------------------
#   DAG
#
# - Import re 
# -------------------------------------------------------------------
with DAG(
    dag_id='webscraping_store', default_args=default_args,
    schedule_interval= '0 17 * * *', catchup=False,
    tags=['webscraping','bookstore']) as dag:

    task_1 = PythonOperator(
        task_id='webscraping',
        python_callable=webscraping)

    task_2 = PythonOperator(
        task_id='data_cleaning',
        python_callable=data_cleaning,
        provide_context=True)
    
    task_3 = PythonOperator(
        task_id='inserting',
        python_callable=inserting,
        provide_context=True)

    task_1 >> task_2 >> task_3