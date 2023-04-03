from copy import copy
from ctypes import Union

import datetime
import time
import re
from pytz import timezone
from dateutil.relativedelta import relativedelta


def get_last_month_date():
    today = datetime.date.today()
    first_day_of_month = today.replace(day=1)
    last_month = first_day_of_month - datetime.timedelta(days=1)
    first_day_of_last_month = last_month.replace(day=1)

    first_day_of_previous_month = datetime.datetime(
        first_day_of_last_month.year,
        first_day_of_last_month.month - 1,
        1,
        tzinfo=timezone('UTC'))

    return first_day_of_previous_month


class VkValidation:
    default_date_before = datetime.datetime(2023, 1, 1, tzinfo=timezone('UTC'))

    def __init__(self, *, date_before=None, date_after=None):
        """
        :param date_before: min date for get post
        :param date_after: max date for get post
        """

        self.date_before = date_before or self.default_date_before
        self.date_after = date_after or datetime.datetime(2023, 2, 1, tzinfo=timezone('UTC'))

    def is_before_self_date(self, date: int) -> bool:
        """Check that date from post more that self date before"""

        format_post_date = self.date_before.strftime('%d.%m.%Y')

        time_stamp_date_before = time \
            .mktime(datetime.datetime.
                    strptime(format_post_date, '%d.%m.%Y')
                    .timetuple())

        return time_stamp_date_before < date

    def is_after_self_date(self, date: int) -> bool:
        """Check that date from post more that self date before"""

        format_post_date = self.date_after.strftime('%d.%m.%Y')

        time_stamp_date_before = time \
            .mktime(datetime.datetime.
                    strptime(format_post_date, '%d.%m.%Y')
                    .timetuple())

        return time_stamp_date_before > date

    @staticmethod
    def keyword_in_text_post(*, keywords: tuple, current_text: str) -> bool:
        return any([VkValidation.text_contains_in_text_post(
            current_text=current_text,
            searching_item=keyword.keyword)
            for keyword in keywords])

    @staticmethod
    def text_contains_in_text_post(*, current_text: str, searching_item: str) -> bool:
        """Check that current text contains in post
        :param current_text: text that def is searching item
        :param searching_item: some text, for example may be named of analysed item
        """

        if len(current_text) == 0:
            return False
        if searching_item in current_text:
            return True

        separate_search_item = searching_item.lower().split()
        lower_current_text = current_text.lower()
        regex_text = r''.join([re.escape(txt)[:-3]
                               + '.*' if len(txt) > 6
                               else re.escape(txt) + '.* '
                               for txt in separate_search_item])
        return True if re.search(regex_text, re.escape(lower_current_text)) else False
