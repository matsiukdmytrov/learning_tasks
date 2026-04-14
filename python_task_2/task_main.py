from datetime import datetime, date, timedelta

def gel_list_of_birthdays(start_date:date, end_date:date,in_users:list[dict[str,str|date]])->list:
    ret_list = list()

    loc_date = start_date
    while loc_date <= end_date:
        for loc_user in in_users:
            if loc_user["birthday"].month == loc_date.month and loc_user["birthday"].day == loc_date.day:
                ret_list.append(loc_user["name"])
        loc_date += timedelta(days=1)

    return ret_list

def get_birthdays_per_week(in_users:list)->dict:

    weekdays_list = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

    today_date = date.today() #+ timedelta(days=2)
    today_weekday = today_date.weekday()

    if today_weekday == 5 or today_weekday == 6:
        first_date = today_date + timedelta(days=(6-today_weekday))
        last_date = today_date + timedelta(days=(7+(5-today_weekday)))
    elif today_weekday == 0:
        first_date = today_date + timedelta(days=-2)
        last_date = today_date + timedelta(days=4)
    else:
        first_date = today_date
        last_date = today_date + timedelta(days=6)

    date_dict = dict()

    loc_date = first_date
    while loc_date <= last_date:
        if loc_date.weekday() == 5 or loc_date.weekday() == 6:
            loc_date += timedelta(days=1)
            continue
        elif loc_date.weekday() == 0:
            temp_list = gel_list_of_birthdays(loc_date - timedelta(days=2),loc_date,in_users)
            temp_key = "Monday"
        else:
            temp_list = gel_list_of_birthdays(loc_date, loc_date,in_users)
            temp_key = weekdays_list[loc_date.weekday()]
        if len(temp_list) > 0:
            date_dict[temp_key] = gel_list_of_birthdays(loc_date - timedelta(days=2), loc_date, in_users)

        loc_date += timedelta(days=1)

    return date_dict

def main():
    users = [
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28).date()},
        {"name": "Ingvar", "birthday": datetime(1955, 4, 11).date()},
        {"name": "Kyi", "birthday": datetime(1955, 4, 12).date()},
        {"name": "Dave", "birthday": datetime(1955, 4, 13).date()},
        {"name": "Anna", "birthday": datetime(1955, 4, 16).date()},
        {"name": "Han", "birthday": datetime(1955, 4, 18).date()},
        {"name": "John", "birthday": datetime(1955, 4, 19).date()},
        {"name": "Colin", "birthday": datetime(1955, 4, 20).date()},
        {"name": "Jeoffrey", "birthday": datetime(1955, 4, 21).date()},
        {"name": "Sansa", "birthday": datetime(1955, 4, 23).date()},
    ]
    print(get_birthdays_per_week(users))
    return 0

if __name__ == "__main__":
    main()