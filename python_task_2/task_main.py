import sys
import datetime

def gel_list_of_birthdays(start_date:datetime.date, end_date:datetime.date,in_users:list[dict[str,str|datetime.date]])->list:
    retlist = list()

    loc_date = start_date
    while loc_date <= end_date:
        for loc_user in in_users:
            if loc_user["birthday"].month == loc_date.month and loc_user["birthday"].day == loc_date.day:
                retlist.append(loc_user["name"])
        loc_date = loc_date + datetime.timedelta(days=1)

    return retlist

def get_birthdays_per_week(in_users:list)->dict:

    weekdays_list = list()
    weekdays_list.append("Monday")
    weekdays_list.append("Tuesday")
    weekdays_list.append("Wednesday")
    weekdays_list.append("Thursday")
    weekdays_list.append("Friday")

    today_date = datetime.date.today() + datetime.timedelta(days=2)
    today_weekday = today_date.weekday()

    if today_weekday == 5 or today_weekday == 6:
        first_date = today_date + datetime.timedelta(days=(6-today_weekday))
        last_date = today_date + datetime.timedelta(days=(7+(5-today_weekday)))
    elif today_weekday == 0:
        first_date = today_date + datetime.timedelta(days=-2)
        last_date = today_date + datetime.timedelta(days=4)
    else:
        first_date = today_date
        last_date = today_date + datetime.timedelta(days=6)

    date_dict = dict()
    for weekday in weekdays_list:
        date_dict[weekday] = list()

    loc_date = first_date
    while loc_date <= last_date:
        if loc_date.weekday() == 5 or loc_date.weekday() == 6:
            loc_date = loc_date + datetime.timedelta(days=1)
            continue
        elif loc_date.weekday() == 0:
            date_dict["Monday"] = gel_list_of_birthdays(loc_date - datetime.timedelta(days=2),loc_date,in_users)
        else:
            date_dict[weekdays_list[loc_date.weekday()]] = gel_list_of_birthdays(loc_date, loc_date,in_users)
        loc_date = loc_date + datetime.timedelta(days=1)

    return date_dict

def main():
    users = list()

    users.append({"name": "Bill Gates", "birthday": datetime.datetime(1955, 10, 28).date()})
    users.append({"name": "Ingvar", "birthday": datetime.datetime(1955, 4, 11).date()})
    users.append({"name": "Kyi", "birthday": datetime.datetime(1955, 4, 12).date()})
    users.append({"name": "Dave", "birthday": datetime.datetime(1955, 4, 13).date()})
    users.append({"name": "Anna", "birthday": datetime.datetime(1955, 4, 16).date()})
    users.append({"name": "Han", "birthday": datetime.datetime(1955, 4, 18).date()})
    users.append({"name": "John", "birthday": datetime.datetime(1955, 4, 19).date()})
    users.append({"name": "Colin", "birthday": datetime.datetime(1955, 4, 20).date()})
    users.append({"name": "Jeoffrey", "birthday": datetime.datetime(1955, 4, 21).date()})
    users.append({"name": "Sansa", "birthday": datetime.datetime(1955, 4, 23).date()})

    print(get_birthdays_per_week(users))
    return 0

if __name__ == "__main__":
    sys.exit(main())