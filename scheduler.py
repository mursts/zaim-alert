#! /usr/bin/env python
# coding: utf-8

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12)
#@sched.scheduled_job('interval', minutes=1)
def zaim_lunch_alert():
    print('This is Zaim alert.')

sched.start()


