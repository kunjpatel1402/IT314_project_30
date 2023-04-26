from datetime import datetime

# Get the current time in ISO format
current_time = datetime.utcnow().isoformat()

# Parse the ISO formatted string into a datetime object
dt = datetime.fromisoformat(current_time)

# Get the year from the datetime object
year = dt.year

# Print the year
print(year)

month = dt.month
print(month)