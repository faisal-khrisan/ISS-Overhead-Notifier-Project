import time
import requests as r
from datetime import datetime
import smtplib

LONGITUDE = 100.389374
LATITUDE = 6.135433
EMAIL = "faisalkhrisan@gmail.com"
PASSWORD = "glogctigebddotyq"

response = r.get (url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()["iss_position"]
longitude = float(data["longitude"])
latitude = float(data["latitude"])


def iss_position () :
    global latitude, longitude, LONGITUDE, LATITUDE

    if ( -5 <= LATITUDE - latitude <=5  )  and ( -5 <= LONGITUDE - longitude <= 5) :
        return  True
    else:
        return  False

parameter = {
    "lng": LONGITUDE,
    "lat": LATITUDE,
    "formatted": 0,
    "tzid": "Asia/Kuala_Lumpur"
}

reply = r.get(url="https://api.sunrise-sunset.org/json", params=parameter)
reply.raise_for_status()

day_data = reply.json()['results']
sunrise = day_data['sunrise']
sunset = day_data['sunset']

current_hour= datetime.now().hour
sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
sunset_hour = int(sunset.split("T")[1].split(":")[0])

while True :
    time.sleep(60)
    if sunrise_hour < current_hour < sunset_hour:
        print(" it is Morning you can not see the ISS now")

    else:
        # send me and email
        if iss_position() :
            with smtplib.SMTP ("smtp.gmail.com") as connection :
                connection.starttls()
                connection.login(user=EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject: ISS in the sky \n\n Hey Faisal,\n Look at the sky, the ISS is above you ")
