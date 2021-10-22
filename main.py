from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_IATA = "DEN"

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    try:
        if destination["lowestPrice"] > flight.price:
            notification_manager.send_message(
                f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} "
                f"to {flight.destination_city}-{flight.destination_airport} "
                f"from {flight.out_date} to {flight.return_date}"
            )

            notification_manager.send_emails(
                message=f"Subject:Low price alert!\n\n"
                        f"Only {flight.price}USD to fly from {flight.origin_city}-{flight.origin_airport} "
                        f"to {flight.destination_city}-{flight.destination_airport} "
                        f"from {flight.out_date} to {flight.return_date}\n"
                        f"https://www.google.com/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}"
                        f".{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            )
    except AttributeError:
        pass
