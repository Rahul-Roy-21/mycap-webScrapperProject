import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import sqlconnect as sc

# Function to Insert a Row of Data into the .csv File
def write_to_file(hotel_info):
    f = open('oyo_rooms.csv',mode='a',newline='')
    writer_obj = csv.writer(f)

    if f.tell() == 0:
        writer_obj.writerow(["HOTEL_NAME","STREET","DISTANCE","RATING",
            "REVIEW_COUNT","REVIEW_SUMMARY","FINALPRICE","PREVIOUS_PRICE","PCTAGE_OFF"])
    
    writer_obj.writerow(hotel_info)


city, max_pages, dbname = "kolkata",3, 'oyo.db'

for i in range(max_pages):
    oyo_url = 'https://www.oyorooms.com/hotels-in-{}/?page={}'.format(city, str(i+1))
    
    payload = {'keyword':'degas','pageSize':'24','offset':'0'}
    headers={
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Referer':'http://www.sothebys.com/en/search-results.html?keyword=degas',
        "User-Agent":"Mozilla/5.0"
    }

    response = requests.get(url=oyo_url, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, features='html.parser')

        allHotels = soup.find_all('div', class_="hotelCardListing")

        for hotel in allHotels:
            hotel_info = []

            hotelName = hotel.find('h3', class_="listingHotelDescription__hotelName").text.strip()
            street = hotel.find('span', {'itemprop':'streetAddress'}).text.strip()
            dist = hotel.find('span', {'class':'listingHotelDescription__distanceText'}).text.strip()
            hotel_info.extend([hotelName, street, dist])
            
            try:
                rating = hotel.find('meta', {'itemprop':'ratingValue'})['content']
                reviews = hotel.find('meta', {'itemprop':'reviewCount'})['content']
                rating_summary = hotel.find_all('span', {'class':'hotelRating__ratingSummary'})[1].text.strip()
            except:
                rating, reviews = "NEW", 0
                rating_summary = "No Reviews Yet"
            hotel_info.extend([rating, reviews, rating_summary])
                
            finalprice = hotel.find('span', {'class':'listingPrice__finalPrice'}).text.strip()[1:]
            slashedprice = hotel.find('span', {'class':'listingPrice__slashedPrice'}).text.strip()[1:]
            pctoff =  hotel.find('span', {'class':'listingPrice__percentage'}).text.strip()[:2]
            hotel_info.extend([finalprice, slashedprice, pctoff])

            # Creating the .csv File
            print(hotel_info)
            write_to_file(hotel_info)

            # Creating and Inserting to the database
            sc.connect(dbname)
            sc.insert_row(dbname, tuple(hotel_info))

    else:
        print('NO RESPONSE !!')
        exit()
    
# SHOW THE DATABASE dbname Once Everything's Done !!
print("~"*40)
print("Table oyo_rooms from {}".format(dbname), end="\n"+"~"*40)
sc.show_db(dbname)