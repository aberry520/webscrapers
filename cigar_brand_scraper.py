import requests, lxml, re, json, urllib.request, psycopg2, os
from bs4 import BeautifulSoup
cigar_brand_dictionary=[]
def get_brands():
    url = "https://cigars.p.rapidapi.com/brands"
    page = input("Page Number: ")
    querystring = {"page":page}
    headers = {
        "X-RapidAPI-Key": "c404c0dfb7mshb5e1e6476869267p1d83fcjsne66a642aa104",
        "X-RapidAPI-Host": "cigars.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    dump = json.dumps(response.json())
    parsed_json = json.loads(dump)
    parsed_cbd = parsed_json["brands"]
    for brand in parsed_cbd:
        cigar_brand_dictionary.append({"brandId":brand["brandId"],"name":brand["name"]})

def connectDB():
    try:
        conn = psycopg2.connect(
            host="dpg-cl0j56bjdq6s73dumo10-a.ohio-postgres.render.com",
            port=5432,
            user="austinberry",
            password="vewEQRLd9gTDvJ6p9xw1HkTb34iXCbA3",
            database="humid_oro",
        )
    except psycopg2.Error as e:
        print("Error connecting to database:")
        print(e)
    else:
        print("Connected to database")

    return conn

def add_apostrophe_after_apostrophe(string):
  """Adds an apostrophe after an apostrophe in a string.

  Args:
    string: The string to add the apostrophe to.

  Returns:
    A string with an apostrophe added after every apostrophe.
  """

  new_string = ""
  for char in string:
    if char == "'":
      new_string += "''"
    else:
      new_string += char
  return new_string

def postDB():
    conn = connectDB()
    cur = conn.cursor()
    print("posting to DB")
    print(cigar_brand_dictionary)
    for brand in cigar_brand_dictionary:
        cur.execute(f"""INSERT INTO cigar_brand VALUES 
('{add_apostrophe_after_apostrophe(brand["name"])}', {brand["brandId"]})""")
        print(brand["name"]," inserted")
    conn.commit()
    conn.close()
    print("disconnected")

connectDB()
get_brands()
postDB()
