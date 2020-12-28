from datetime import datetime, timedelta


days_to_subtract = 30
date = (datetime.today() - timedelta(days=days_to_subtract)).strftime("%d:%m:%Y")

print(date)