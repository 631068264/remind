#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 16/11/4 10:53
@annotation = '' 
"""
from celery import Celery


# celery -A base worker -Q mail-remind,sms-remind -l INFO


class MyCelery(Celery):
    ignore_task = ".tasks"

    def gen_task_name(self, name, module):
        if module.endswith(self.ignore_task):
            module = module[:-len(self.ignore_task)]
        return super(MyCelery, self).gen_task_name(name, module)


app = MyCelery('remind',
               backend="redis://localhost:6379",
               broker='amqp://guest@localhost:5672//',
               include=['base.mail_util', 'base.sms_util'],
               )

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=1,
    # result_expires=3600,
    ignore_result=True,
    # timezone="UTC",
    # timezone="Asia/Shanghai",
    # enable_utc=True,
)

# celery -A proj worker -Q feeds,celery
# remind_exchange = {
#     'exchange': 'remind',
#     'exchange_type': 'direct',
# }

# app.conf.task_routes = (
#     Queue('mail_remind', routing_key='mail_remind'),
#     Queue('sms_remind', routing_key='sms_remind'),
# )

app.conf.task_routes = {
    "base.mail_util.*": {
        "queue": "mail_remind",
        "routing_key": "mail_remind",
        # **remind_exchange,
    },
    "base.sms_util.*": {
        "queue": "sms_remind",
        "routing_key": "sms_remind",
        # **remind_exchange,
    },
}

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': 2.0,
#         'args': (16, 16)
#     },
# }

# app.config_from_object('celeryconfig')

# if __name__ == '__main__':
#     app.start()
# # app.conf.humanize(with_defaults=False, censored=True)
