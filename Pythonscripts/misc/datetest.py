import datetime

StartDate = "20130101"

Date = datetime.datetime.strptime(StartDate, "%Y%m%d")

EndDate = Date + datetime.timedelta(days=1)

print EndDate.strftime('%Y%m%d')
