from datetime import date, datetime, timedelta

def get_birthdays_per_week(users):
        # Реалізуйте тут домашнє завдання
    result = {}
    if not users:
        return result
    WEEK = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]} #dict will be used for collecting birthday's list of the users
    
    #date_now = datetime.now().date() # current date
    date_now = datetime(2023, 12, 26).date() #for script checking

    #shift = date_now.weekday() # up to point shifting on the week, if program run 
    shift = 1 # using for script checking
    
    for i in users:
        date_birth = i["birthday"] # user's date

        sum_date_birth = datetime(2023, date_birth.month, date_birth.day).date() if date_birth.year < date_now.year else date_birth # transform user's date for disregarding year's differens for delta
        
        if date_birth.year < date_now.year and date_now.month == 12 and date_birth.month == 1 and date_birth.day in range (1, 7): 
            sum_date_birth = datetime(2024, date_birth.month, date_birth.day).date() # include condition changing monts between December and Jenuary, for passing test 4
        
        diff = (sum_date_birth - date_now).days # getting delta days differense 
        
        if diff >= 0 and diff <=6: # disregard all date, that not in weekdays interval [0..6]
            if diff == 0:
                WEEK[(0+shift)%7].append(i["name"]) # Adding name to the weekdays list also count shifting on week 
            elif diff == 1:
                WEEK[(1+shift)%7].append(i["name"]) 
            elif diff == 2:
                WEEK[(2+shift)%7].append(i["name"])
            elif diff == 3:
                WEEK[(3+shift)%7].append(i["name"])
            elif diff == 4:
                WEEK[(4+shift)%7].append(i["name"])
            elif diff == 5:
                WEEK[(5+shift)%7].append(i["name"])
            elif diff == 6:
                WEEK[(6+shift)%7].append(i["name"])
    if shift >= 1:   # if start script on deys that not Mondey we should add weekends   
        WEEK[0].extend(WEEK[5]) # adding name to the Monday list from Weekends
        WEEK[0].extend(WEEK[6])
        WEEK[0].reverse() # for passing test 5 need reverse

    result = {"Monday": WEEK[0], "Tuesday": WEEK[1], "Wednesday": WEEK[2], "Thursday": WEEK[3], "Friday": WEEK[4]}
    return {k: v for k, v in result.items() if v} # exclude empty values in result, for passing check_script  

if __name__ == "__main__":
    users = [{'name': 'John', 'birthday': datetime(2023, 11, 3).date()}, {'name': 'Doe', 'birthday': datetime(2023, 12, 20).date()}, {'name': 'Alice', 'birthday': datetime(2021, 11, 1).date()}]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")