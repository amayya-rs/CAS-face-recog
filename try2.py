from datetime import datetime

currtime = datetime.now()
latetime = currtime.replace(hour = 7, minute = 30, second = 0, microsecond =0)
late = False
if currtime > latetime:
    print("late")
