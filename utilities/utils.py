
def convert_to_date_format(dt):
    return dt.strftime('%Y-%m-%d')

# Function to subtract one year
def subtract_year(dt,years):
    try:
        return dt.replace(year=dt.year - years)
    except ValueError:
        # This handles the case where the original date is February 29 (leap year)
        return dt.replace(month=2, day=28, year=dt.year - 1)

