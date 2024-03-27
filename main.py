import requests
#  most popular way for python developers to work with APIs
from datetime import datetime as dt
import smtplib
import time

MY_LAT = 35.819640
MY_LNG = -78.823020
my_email = "fakeemail43066@gmail.com"
my_password = "chtf fklg uscx lwbj"


response = requests.get(url="http://api.open-notify.org/iss-now.json")
#  response.status_code --> gives a response code

response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


def iss_close():
    lat_diff = MY_LAT - iss_latitude
    long_diff = MY_LNG - iss_longitude
    if -5 < lat_diff < 5 and -5 < long_diff < 5:
        return True

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()

data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(sunset)

hour_now = dt.now().hour

while True:
    time.sleep(60) #executes the code every 60 seconds
    if iss_close() and hour_now >= sunset or hour_now <=sunrise:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="juhigulati5@gmail.com",
                msg="Subject:ISS Above you!\n\nLook up!")

