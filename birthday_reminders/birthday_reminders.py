from datetime import datetime
import csv


def process_csv_file(filepath: str):
    """Check if someone has birthday today. If so, yield the row."""
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for date, name in reader:
            parsed_date = convert_str_to_datetime(date)
            if is_birthday(parsed_date):
                yield {'name': name, 'date': date}


def is_birthday(date: datetime.date) -> bool:
    """Check if passed date is today."""
    today = datetime.today().date()
    if today.day == date.day and today.month == date.month:
        return True


def convert_str_to_datetime(date: str) -> datetime.date:
    """Convert a string into datetime object. Pass date as d.mm.yyyy."""
    day, month, year = date.split('.')
    return datetime.strptime(f'{day}.{month}.', '%d.%m.')


if __name__ == '__main__':
    birthdays = list(process_csv_file('./birthdays.csv'))
    if len(birthdays) == 0:
        print('No one has birthday today.')
    else:
        for birthday in birthdays:
            print(f'{birthday["name"]} has birthday today! ({birthday["date"]})')
