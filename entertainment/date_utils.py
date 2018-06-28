from datetime import datetime


class DateUtils(object):

    @staticmethod
    def parsing_date(text):
        for fmt in ('%Y-%m-%d', '%Y - %m - %d', '%d.%m.%Y', '%d/%m/%Y'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')
