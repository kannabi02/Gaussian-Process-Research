import pandas as pd
import sys
import os
import datetime


def dataloader(PATH, outfile):

    temp1 = pd.read_csv(PATH + "_p1.csv", sep = ";")
    temp2 = pd.read_csv(PATH + "_p2.csv", sep = ";")
    temp3 = pd.read_csv(PATH + "_p3.csv", sep = ";")
    temp1.replace(',','', regex=True, inplace=True)
    colname = temp1.columns
    colnames = []
    for col in colname:
        if not "Date" in col:
            if not "Time of day" in col:
                colnames.append(col)
    for colname in colnames:
            temp1[colname] = pd.to_numeric(temp1[colname],errors='coerce')
    temp2.replace(',','', regex=True, inplace=True)
    for colname in colnames:
        temp2[colname] = pd.to_numeric(temp2[colname],errors='coerce')
    temp3.replace(',','', regex=True, inplace=True)
    for colname in colnames:
        temp3[colname] = pd.to_numeric(temp3[colname],errors='coerce')
#        temp3.replace(',', '', regex=True, inplace=True)


    name = pd.concat([temp1, temp2, temp3], ignore_index=True)
    times = []
    # print(type(forecons['Date'].iloc[0]), type(forecons['Time of day'].iloc[0]), type(" "))
    for i in range(name.shape[0]):
        if isinstance(name['Date'].iloc[i], float) | isinstance(name['Date'].iloc[i], float):
            print(i)
        times.append(datetime.datetime.strptime(name['Date'].iloc[i] + " " + name['Time of day'].iloc[i],
                                                '%b %d %Y %I:%M %p'))

    sdate2020 = "2020-03-29 03:00:00"
    edate2020 = "2020-10-25 02:45:00"
    sdate2019 = "2019-03-31 03:00:00"
    edate2019 = "2019-10-27 02:45:00"
    sdate2018 = "2018-03-25 03:00:00"
    edate2018 = "2018-10-28 02:45:00"
    sdate2017 = "2017-03-26 03:00:00"
    edate2017 = "2017-10-29 02:45:00"
    sdate2016 = "2016-03-27 03:00:00"
    edate2016 = "2016-10-30 02:45:00"
    sdate2015 = "2015-03-29 03:00:00"
    edate2015 = "2015-10-25 02:45:00"
    sdates = [sdate2015, sdate2016, sdate2017, sdate2018, sdate2019, sdate2020]
    edates = [edate2015, edate2016, edate2017, edate2018, edate2019, edate2020]
    sumdatelist = pd.date_range(sdates[0], edates[0], freq="15min").format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    for i in range(1, len(sdates)):
        temp = pd.date_range(sdates[i], edates[i], freq="15min").format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        sumdatelist = sumdatelist + temp

    print(type(sumdatelist[0]), type(times[0]))
    timesnew = []
    for day in times:
        if day in sumdatelist:
            print("here")
            tempdate = datetime.datetime.strptime(day, "%Y-%m-%d %H:%M:%S")-datetime.timedelta(hours=1)
            if tempdate not in timesnew:
                timesnew.append(tempdate)
                sumdatelist.remove(day)
            else:
                timesnew.append(day)
                print("here")
            if "10-25" in tempdate:
                print("day", day," adjusted day",tempdate)
        else:
            timesnew.append(day)

    weekday = []
    weekcls = []

    for time in timesnew:
        weekday.append(time.strftime("%a"))
        weekcls.append(time.strftime("%w"))
    weekendcls = []
    for cls in weekcls:
        if cls == 0 | 6:
            weekendcls.append(1)
        else:
            weekendcls.append(0)
    name['Datetime'] = timesnew
    name['Weekday'] = weekday
    name['Weekclass'] = weekcls
    print("#dates", len(timesnew),"#uniques", name['Datetime'].nunique(), "#nans", name['Datetime'].isna().sum(), "len datetime", len(name['Datetime']))
    try:
        os.remove(outfile)
    except:
        pass
    try:
        del name['Unnamed: 0']
    except:
        pass
    name.to_csv(outfile, index=False)

if __name__ == '__main__':
    dataloader(sys.argv[1], sys.argv[2])