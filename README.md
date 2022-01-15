# Book Club Data Storing

Data engineering design to collect and process data from website.

<div align="center">
    <img src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=928&q=80" width='100%' height='320' alt="image">
</div>

<br>

> The company is fictional and its story was taken from the website [Seja Um Data Scientist](https://sejaumdatascientist.com/o-projeto-de-data-engineering-para-o-seu-portfolio/). The website [Books to Scrape](https://books.toscrape.com/) used to data collection for this project is made for training and learning webscraping.

## 1.0 Business Problem

Book Club is a book exchange startup. The business model works based on the exchange of books by users, each book registered by the user, gives the right to an exchange, but the user can also buy the book, if the user does not want to offer another book in exchange.

One of the most important tools for this business model to be profitable is the recommendation. An excellent recommendation increases the volume of exchanges and sales on the site. However, Book Club does not collect or store the books submitted by users.

Books for exchange are uploaded by users themselves through a button "Upload", they are visible on the site, along with their stars, which represent how much users liked the book or not. However, the company does not collect or store this data in a database.

Therefore, data must be collected directly from the company's website and stored in a database for consultation.

## 2.0 Business Assumptions

For this company the data is important to improve the book recommendation. However, the company doesn't collect the data to process and implement data for analysis or data science projects.

A recommendation system can facilitate recommending books for sale or for exchange. This can facilitate a greater number of visits within the site, and in this way create a greater number of visitors. That's why it is important to have constant data collection for analysis and creation of data science projects.

## 3.0 Solution Strategy

The strategy is focused on collecting, transforming and loading (ETL) the data from the website and storage it into a database.

The data is collected using the BeatifulSoup library. This library allows the data collection directly from the HTML website. After data collection, the data will be stored and organized into SQLite database. Finally, the schedule to run the scripts is made by the Airflow.

## 4.0 Conclusions

The project is about of creation a database with all the books and their informations. The ETL script is executed every day to collect and update the data of the SQLite database.

However, some improvements must be implemented in the future. Change the database from SQLite to MySQL in Docker.

## 5.0 Lessons Learned

* Creation of a SQLite database.

* Implementation of the Airflow in Docker.

* Creation of ETL scripts.

## 6.0 Next Steps

* Implementation of a MySQL database using Docker.

* Connect Airflow and MySQL to collect and insert into new database.

<!--
## 4.0 Top 3 Data Insights

## 5.0 Machine Learning Applied

## 6.0 Machine Learning Performance

## 7.0 Business Results

## 8.0 Conclusions

## 9.0 Lessons Learned

## 10.0 Next Steps
>