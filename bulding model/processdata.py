
# coding: utf-8

# In[17]:

import numpy as np
import pandas as pd
import re
import sys
import time


# In[82]:

cities = ["2015-boston"]
data = pd.DataFrame()
for i in xrange(len(cities)):
    print cities[i]
    f = open('/home/yanxin/test/' + cities[i] + '.html', 'rU')
    activity = 0
    user = ""
    date = ""
    race = ""
    start_time = ""
    name = ""
    gender = ""
    age = 0
    time = 0
    pace = 0
    temp = pd.DataFrame()

    g = False
    for line in f:
        race_search = re.search(r'<h1>(\w.+)<', line)
        date_search = re.search(r'start-date\">(\w.+)<', line)
        start_search = re.search(r'start-time\">(\w.+)<', line)
        act_num = re.search(r'<tr data-activity_id=\"(\d+)\">', line)
        ath_id = re.search(
            r'<a class=\"avatar avatar-athlete\" href=\"\/athletes\/(\d+)\">', line)
        ath_name = re.search(r'<img alt=\"(\w.+)\" src=', line)
        ath_gender = re.search(r'<td class=\"athlete-gender\">', line)
        ath_age = re.search(r'<td class=\"athlete-age\">(\d+)<\/td>', line)
        finish_time = re.search(
            r'<td class=\"finish-time\">(\d+):(\d+):(\d+)<\/td>', line)
        time_pace = re.search(
            r'<td class=\"finish-pace\">(\d+):(\d+)\/mi<\/td>', line)

        if date_search:
            date = date_search.group(1)
        if race_search:
            race = race_search.group(1)
        if start_search:
            start_time = start_search.group(1)
        if act_num:
            activity = int(act_num.group(1))
        if ath_id:
            user = ath_id.group(1)
        if ath_name:
            name = ath_name.group(1)
        if ath_gender:
            ath_gender2 = re.search(r'^(\w+)', next(f))
            if ath_gender2:
                gender = ath_gender2.group(1)
        if ath_age:
            age = int(ath_age.group(1))
        if finish_time:
            time = int(int(finish_time.group(1)) * 60 * 60 +
                       int(finish_time.group(2)) * 60 + int(finish_time.group(3)))
        if time_pace:
            pace = int(60 * int(time_pace.group(1)) + int(time_pace.group(2)))
            temp = temp.append(
                [[name, date, start_time, race, gender, age, user, activity, time, pace]])
    f.close()
    temp.columns = ['name', 'date', 'start_time', 'race',
                    'gender', 'age', 'user', 'activity', 'm_time', 'm_pace']
    temp = temp.drop_duplicates()
    data = data.append(temp)


goals = pd.DataFrame()
for i in xrange(len(cities)):
    g = open('/home/yanxin/test/' + cities[i] + '.html', 'rU')
    temp = re.findall(r'\[(\d+),(\w+)\]', g.read())
    g.close()
    temp = pd.DataFrame(temp).drop_duplicates()
    temp.columns = ['user', 'goal']
    goals = goals.append(temp)


combo = pd.merge(goals, data, how='inner', left_on='user', right_on='user')
combo = combo[combo['m_time'] < 36000]
combo = combo[combo['age'] < 100]
combo.to_csv("/home/yanxin/test/text_files/all_runners.csv", index=False)
all_data = combo[combo['goal'] != 'null']
all_data.to_csv("/home/yanxin/test/text_files/goal_runners.csv", index=False)
