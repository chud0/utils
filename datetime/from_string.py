from datetime import datetime
from dateutil.relativedelta import relativedelta


def parse_dt_str(date_str, date_fmt="%d.%m.%Y %H:%M"):
    return datetime.strptime(date_str, date_fmt)


def td_from_bd(date_str):
    return relativedelta(datetime.now(), parse_dt_str(date_str))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="date in format: 'day.month.year hour:minute'")
    args = parser.parse_args()

    delta = td_from_bd(args.date)
    print("{} yaer(s), {} month(s), {} day(s)".format(delta.years, delta.months, delta.days))
