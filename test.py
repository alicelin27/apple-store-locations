from pyquery import PyQuery as pq
import requests
import csv

all_locations_html = requests.get("https://www.apple.com/retail/storelist/")
all_locations = pq(all_locations_html.content)

keys = ["Name", "Street", "Locality", "Region", "Postal Code", "Latitude", "Longitude", "URL"]
information = dict()

for key in keys:
    information[key] = []

for link in all_locations('a'):
    if "retail" in link.attrib['href']:
        if link.attrib['href'] == "/retail/":
            break

        full_link = "https://www.apple.com" + link.attrib['href']
        information["URL"].append(full_link)
        location_html = requests.get(full_link)
        location = pq(location_html.content)
        if (location("h1").text())[6:] == "Park Visitor Center":
            information["Name"].append("Apple " + (location("h1").text())[6:])
        else:
            information["Name"].append((location("h1").text())[6:])
        full_address = location("address").text()
        street = full_address.splitlines()[0]
        information["Street"].append(street)
        full_address = full_address.splitlines()[len(full_address.splitlines()) - 1]
        locality = full_address.split(",")[0]
        information["Locality"].append(locality)
        full_address = full_address.split(",")[1]
        region = full_address.split(" ")[1]
        information["Region"].append(region)
        postalCode = full_address.split(" ")[2]
        information["Postal Code"].append(postalCode)

        slug = link.attrib['href'][8:-1]
        print(slug)
        location_lat_long = requests.get(
            "https://www.apple.com/rsp-web/store-detail?storeSlug=" + slug + "&locale=en_US")
        lat_long = location_lat_long.json()
        information["Latitude"].append(lat_long["geolocation"]["latitude"])
        information["Longitude"].append(lat_long["geolocation"]["longitude"])

print(information)

file = open("apple_locations.csv", "w")

writer = csv.writer(file)
writer.writerow(keys)
limit = len(information["Name"])
for r in range(limit):
    info = []
    for x in information:
        info.append(information[x][r])
    writer.writerow(info)

file.close()
