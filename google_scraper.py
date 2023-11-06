import requests, lxml, re, json, urllib.request, psycopg2, os
from bs4 import BeautifulSoup

def get_cigars():
    url = "https://cigars.p.rapidapi.com/cigars"
    page = input("Page Number: ")
    querystring = {"page":page}
    headers = {
        "X-RapidAPI-Key": "c404c0dfb7mshb5e1e6476869267p1d83fcjsne66a642aa104",
        "X-RapidAPI-Host": "cigars.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    dump = json.dumps(response.json())
    return json.loads(dump)

def get_names():
    search_names = []
    # cigars_json = get_cigars()
    # cigars_read = str(cigars_json)

    # with open("cigars.json") as cigars_json_open:
    #     cigars_read = cigars_json_open.read()

    # print("JSON: ", cigars_json)
    # print("Read: ",cigars_read)
    
    parsed_json = get_cigars()
    cigar_dictionary = parsed_json["cigars"]
    for cigar in cigar_dictionary:
        search_names.append(cigar["name"])
    print(search_names)
    return search_names

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
        print("Connectione succesful")

    conn.close()
    print("disconnected")


def get_images(search_name):
    count = 1
    while (True):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        search = """
        site:cigarpage.com OR 
site:cigarsdaily.com OR 
site:cigarsinternational.com OR 
site:foxcigar.com OR 
site:smallbatchcigar.com OR 
site:perfectcigarblend.com OR 
site:cigargod.com OR 
site:thecigarthief.com OR 
site:cigarandpipes.com OR 
site:coronacigar.com OR 
site:neptunecigar.com OR 
site:cubadoro.ch 
"""+search_name

        params = {
            "q": search,                  # search query
            "tbm": "isch",                # image results
            "hl": "en",                   # language of the search
            "gl": "us",                   # country where search comes from
            "ijn": "0"                    # page number
        }

        html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, "lxml")
        # print(html.url)

        google_images = []

        all_script_tags = soup.select("script")
        
        matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))
        
        matched_images_data_fix = json.dumps(matched_images_data)
        matched_images_data_json = json.loads(matched_images_data_fix)
        
        matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

        matched_google_images_thumbnails = ", ".join(
            re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                    str(matched_google_image_data))).split(", ")
        
        thumbnails = [
            bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
        ]

        # removing previously matched thumbnails for easier full resolution image matches.
        removed_matched_google_images_thumbnails = re.sub(
            r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

        # https://regex101.com/r/fXjfb1/4
        # https://stackoverflow.com/a/19821774/15164646
        matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

        full_res_images = [
            bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
        ]

        for thumbnail, original in zip(thumbnails, full_res_images):
            google_images.append({
                "thumbnail": thumbnail,
                "image": original
            })


            # Download original images
            # print(f'Downloading {index} image...')
            
            # opener=urllib.request.build_opener()
            # opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36')]
            # urllib.request.install_opener(opener)

            # urllib.request.urlretrieve(original, f'Bs4_Images/original_size_img_{index}.jpg')
        # print(google_images[0])
        # print(thumbnails)
        
        if len(google_images) > 0:
            return google_images[0]
        else:
            print("Try again "+ search_name)
            print(count)
            if count < 5:
                count = count+1
            else:
                None
                break

            


def get_images_by_name():
    images_dictionary=[]
    for name in get_names():
        images_dictionary.append({"name":name, "images":get_images(name)})
        print(name+" images retrieved")
        
    images_dictionary_string = json.dumps(images_dictionary, indent=4)

    def make_file(filename):
        """Creates a new file with the given filename. If the file already exists, the filename will be modified to make it unique."""

        # Get the base filename and extension.
        base_filename, extension = os.path.splitext(filename)

        # Create a new filename if the original filename already exists.
        if os.path.exists(filename):
            counter = 1
            while True:
                new_filename = f"{base_filename}_{counter}{extension}"
                if not os.path.exists(new_filename):
                    filename = new_filename
                    break
                counter += 1

        # Create the new file.
        open(filename, "w").write(images_dictionary_string)

        return filename
    make_file("images.json")
    
get_images_by_name()
print("file created")
# get_cigars()
# get_names()
# get_images("13 Cigars Torpedo")