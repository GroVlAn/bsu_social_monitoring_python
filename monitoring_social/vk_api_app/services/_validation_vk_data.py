from ctypes import Union

from datetime import datetime
import time
import re

from dateutil.relativedelta import relativedelta


class VkValidation:
    default_date_before = datetime.now() \
                  - relativedelta(months=1) \
                  - relativedelta(days=datetime.now().day - 1)

    def __init__(self, *, date_before=None, date_after=None):
        """
        :param date_before: min date for get post
        :param date_after: max date for get post
        """

        self.date_before = date_before or self.default_date_before
        self.date_after = date_after or datetime.now()

    def is_before_self_date(self, date: int) -> bool:
        """Check that date from post more that self date before"""

        format_post_date = self.date_before.strftime('%d.%m.%Y')
        print(format_post_date)
        time_stamp_date_before = time \
            .mktime(datetime.
                    strptime(format_post_date, '%d.%m.%Y')
                    .timetuple())

        return time_stamp_date_before < date

    def is_after_self_date(self, date: int) -> bool:
        """Check that date from post more that self date before"""

        format_post_date = self.date_after.strftime('%d.%m.%Y')
        print(format_post_date)
        time_stamp_date_before = time \
            .mktime(datetime.
                    strptime(format_post_date, '%d.%m.%Y')
                    .timetuple())

        return time_stamp_date_before > date

    @staticmethod
    def text_contains_in_text_post(*, current_text: str, searching_item: str):
        """Check that current text contains in post
        :param current_text: text that def is searching item
        :param searching_item: some text, for example may be named of analysed item
        """

        separate_current_text = current_text.lower().split()
        lower_searching_item = searching_item.lower()
        regex_text = r''.join([txt[:-3] + '.* ' if len(txt) > 6 else txt + ' ' for txt in separate_current_text])

        return re.search(regex_text, lower_searching_item)
