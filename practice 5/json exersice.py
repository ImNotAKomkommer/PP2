# 1. Subtract five days from current date

from datetime import datetime, timedelta

today = datetime.now()
five_days_ago = today - timedelta(days=5)

print("1. Five days ago:", five_days_ago)


# 2. Print yesterday, today, tomorrow

today_date = datetime.now().date()
yesterday = today_date - timedelta(days=1)
tomorrow = today_date + timedelta(days=1)

print("\n2. Yesterday:", yesterday)
print("Today:", today_date)
print("Tomorrow:", tomorrow)


# 3. Drop microseconds from datetime

current_datetime = datetime.now()
without_microseconds = current_datetime.replace(microsecond=0)

print("\n3. Current datetime:", current_datetime)
print("Without microseconds:", without_microseconds)


# 4. Calculate two date difference in seconds

date1 = datetime(2025, 3, 1, 12, 0, 0)
date2 = datetime(2025, 3, 7, 15, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("\n4. Difference in seconds:", seconds)