#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 13:41:32 2024

@author: francescavasta
"""

#load the necessary libraries
import csv
import requests #this library is necessary to obtain the HTML content of the webpage you want to scrape.
from bs4 import BeautifulSoup

#1 WE OBTAIN THE HTML USING REQUEST
#2 WE CREATE A BEAUTIFOUL SOUP OBJECT 
#3 WE APPLY THE BEAUTIFUL SOUP METHODS

#THE METHODS ARE 
#soup.find() : Find the first occurrence of a tag.
#soup.find_all() : Find all occurrences of a tag. 
#ci sono 50 pagine e dobbiamo creare un for loop

#it is useful to put the url in a variable 
base_url = "https://books.toscrape.com/catalogue/"
start_url = "https://books.toscrape.com/catalogue/page-1.html"

# define a function to obtain the HTML content of the webpage
def get_soup(url):
    response = requests.get(url) ##with "requests.get we obtain the HTML content of the webpage 
    #we want to scrape
    return BeautifulSoup(response.text, 'html.parser') #we use the library BeautifulSoup to create a 
#Beautifulsoup object
#'html.parser': This is the parser used by BeautifulSoup. 
#It’s a built-in Python parser that converts the HTML into a BeautifulSoup object (or a parse tree) 
#for easy navigation


# define function to obtain the details of the book from the specific-book webpage
def get_book_details(book_url):
    soup = get_soup(book_url)

    # Title
    title = soup.find('h1').text

    # Rating as n. Of stars (we want to extract the second class, as it displays the n. of stars)
    rating = soup.find('p', class_='star-rating')['class'][1]

    # Price
    price = soup.find('p', class_='price_color').text

    # Available quantity
    availability = soup.find('p', class_='instock availability').text.strip()
    quantity = availability.split('(')[1].split(' ')[0]

    # Genre
    genre = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

    # Book description
    description_tag = soup.find('div', id='product_description')
    if description_tag:
        description = description_tag.find_next('p').text.strip()
    else:
        description = 'No description available'

    return {
        'title': title,
        'rating': rating,
        'price': price,
        'quantity': quantity,
        'genre': genre,
        'description': description
    }


###Details of the code:
#Title (h1): extracted from <h1> of the specific book page, which contains the title of the book
#Rating (p with class star-rating): extracted from the second class of <p class="star-rating">, 
#which indicates the number of stars (es. "Three").
#Price (p with classe price_color): extracted from the tag <p class="price_color">.
#Available quantity (p with class instock availability): extracted from the text which comes after the "availability" icon. 
#The exact quantity available is obtained by doing operations on the string, to extract only the number.
#Genre (breadcrumb): extracted from the list breadcrumb, in particular it is the third (li), 
#which displays the category of the book.
#description of the book (div with id product_description): the description is the text which comes after the tag div.


# Example of using book_url function on a single book webpage
book_url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
book_details = get_book_details(book_url)
print(book_details)

# defining the function which allows us to extract from the homepage and following pages all the links to the specific book pages.
def get_books_on_page(url):
    soup = get_soup(url) ## Funzione per ottenere il contenuto HTML di una pagina
    books = soup.find_all('h3')
    book_links = [base_url + book.find('a')['href'].replace('../../../', '') for book in books]
    return book_links

# function which iterates on all homepage pages and which is necessary to collect the details of the books.
def scrape_all_books(): 
    page_num = 1
    all_books = []

    while True:
        print(f"Scraping page {page_num}...")
        page_url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        book_links = get_books_on_page(page_url) #finds all the link to the specific books which are located on the homepage and calls the function get_book_details to collect details.
        
        if not book_links:
            break
        
        for book_link in book_links:
            book_details = get_book_details(book_link)# extract all the details of the book from the book page
            all_books.append(book_details)

        page_num += 1
    
    return all_books

# Scraping
books = scrape_all_books() #this main function iterates on all the pages (from 1 to 50) and collects the details of all books

# Print result (will be also saved as CSV)
for book in books:
    print(book)

# print the result of the first book
print(books)

# save all the details of all books as CSV file
import csv

with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)

print("Scraping completato e dati salvati su 'books.csv'")
