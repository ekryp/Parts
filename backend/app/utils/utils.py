import os, sys
import traceback
from datetime import datetime, timedelta, date
from dateutil.parser import parse
import pytz
import calendar

import pandas as pd
import parsedatetime
import logging
import json

from pydruid.utils.having import Having
from sqlalchemy import create_engine

from app import User
from app.configs import Configuration
from app.models.basemodel import get_session
from app.models.ekryp_user_session import UserSession

logged_in_users = {}

class Utils:
    @staticmethod
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except Exception as e:
            print(e)
            return False
        return True


def dttm_from_timtuple(d):
    return datetime(
        d.tm_year, d.tm_mon, d.tm_mday, d.tm_hour, d.tm_min, d.tm_sec)


def get_granularity(granularity_type, date_str, valueOnly=False):
    try:
        date_value = parse(date_str).replace(tzinfo=pytz.UTC)
        granularity_value = date_value.isoformat()
        granularity_value = date_value.strftime("%Y-%m-%d")

        if valueOnly:
            # Granularity value style change for comapring
            date_obj = pd.Timestamp(date_value)
            if granularity_type == "year":
                granularity_value = date_obj.year
            elif granularity_type == "quarter":
                granularity_value = date_obj.quarter
            elif granularity_type == "month":
                granularity_value = date_obj.month
            elif granularity_type == "week":
                granularity_value = date_obj.week
            elif granularity_type == "day":
                granularity_value = date_obj.dayofyear
        else:
            if granularity_type == "year":
                granularity_value = str(date_value.year)
            elif granularity_type == "quarter":
                print(date_value)
                granularity_value = str(get_quarter_by_month(date_value.month)) + " " +str(date_value.year)
            elif granularity_type == "month":
                granularity_value = str(calendar.month_abbr[date_value.month]) + " "+str(date_value.year)
            elif granularity_type == "week":
                week_end_day = date_value - timedelta(days=(date_value.weekday() + 1) % 7) + timedelta(days=6)
                granularity_value =  week_end_day.strftime('%Y-%m-%d')

        return granularity_value

    except Exception as e:
        print(e)
        print (str(date_str) + ' Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
        return str(date_str)

def get_quarter_by_month(month):
    # TODO parameterize these months and associate this at partner mappings level Quarters Fisical Year definition
    if month in [1,2,3]:
        return "Q1"
    elif month in [4,5,6]:
        return "Q2"
    elif month in [7,8,9]:
        return "Q3"
    elif month in [10,11,12]:
        return "Q4"

def get_date_range(interval_type, interval_value):
    from_dttm = datetime.now()
    to_dttm = datetime.now()
    if(interval_type == "last_week"):
        from_dttm = from_dttm - timedelta(days=7)
    elif(interval_type == "this_week"):
        from_dttm = from_dttm - timedelta(days=from_dttm.weekday())
    elif(interval_type == "last_month"):
        from_dttm = from_dttm - timedelta(days=30)
    elif(interval_type == "this_month"):
        from_dttm = from_dttm - timedelta(days=(from_dttm.day-1))
    elif(interval_type == "current_quarter"):
        from_dttm = get_first_day_of_the_quarter(from_dttm)
    elif(interval_type == "last_quarter"):
        from_dttm = get_first_day_of_the_quarter(from_dttm-timedelta(days=92))
        to_dttm = get_last_day_of_the_quarter(to_dttm-timedelta(days=92))
    elif(interval_type == "previous_x_days"):
        from_dttm = from_dttm - timedelta(days=int(interval_value))
    elif(interval_type == "custom"):
        from_dttm = datetime.strptime(interval_value["from_date"], "%Y-%m-%d")
        to_dttm = datetime.strptime(interval_value["to_date"], "%Y-%m-%d")
    else:
        print("Error: Invalid interval type")
        raise NameError("Interval type not valid")
    res = dict()
    res['from_dttm'] = datetime.strftime(from_dttm, "%Y-%m-%d")
    res['to_dttm'] = datetime.strftime(to_dttm, "%Y-%m-%d")
    return res


def get_quarter_by_date(date):
    return int((date.month - 1) / 3 + 1)

def get_first_day_of_the_quarter(date):
    quarter = get_quarter_by_date(date)
    return datetime(date.year, 3 * quarter - 2, 1)

def get_last_day_of_the_quarter(date):
    quarter = get_quarter_by_date(date)
    month = 3 * quarter
    remaining = int(month / 12)
    return datetime(date.year + remaining, month % 12 + 1, 1) + timedelta(days=-1)


def get_df_from_sql_query(query, db_connection_string):
    engine = create_engine(db_connection_string, connect_args=Configuration.ssl_args, echo=False)
    return pd.read_sql_query(query,engine)

class AutoVivification(dict):
    """Implementation of perl's autovivification feature. For nested defaultdict()"""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


def parse_human_datetime(s):
    """
    Returns ``datetime.datetime`` from human readable strings

    >>> from datetime import date, timedelta
    >>> from dateutil.relativedelta import relativedelta
    >>> parse_human_datetime('2015-04-03')
    datetime.datetime(2015, 4, 3, 0, 0)
    >>> parse_human_datetime('2/3/1969')
    datetime.datetime(1969, 2, 3, 0, 0)
    >>> parse_human_datetime("now") <= datetime.now()
    True
    >>> parse_human_datetime("yesterday") <= datetime.now()
    True
    >>> date.today() - timedelta(1) == parse_human_datetime('yesterday').date()
    True
    >>> year_ago_1 = parse_human_datetime('one year ago').date()
    >>> year_ago_2 = (datetime.now() - relativedelta(years=1) ).date()
    >>> year_ago_1 == year_ago_2
    True
    """
    try:
        dttm = parse(s)
    except Exception:
        try:
            cal = parsedatetime.Calendar()
            dttm = dttm_from_timtuple(cal.parse(s)[0])
        except Exception as e:
            logging.exception(e)
            raise ValueError("Couldn't parse date string [{}]".format(s))
    return dttm

def calc_operational_json(customer_asset_identifier):
    # Getting operational days from database for the customer asset identifier
    operational_days_query = "SELECT day, operational_hours as op_hrs FROM product_operational_days where id='" + \
                             customer_asset_identifier + '\''
    operational_days_df = get_df_from_sql_query(query=operational_days_query,
                                                db_connection_string=Configuration.EKRYP_DATA_DB_URI)
    operational_days_json = json.loads(operational_days_df.to_json(orient="records"))
    return operational_days_json

def calc_operational_age(customer_asset_identifier, installed_date, to_date_obj):
    # Change it as per requirement. If partial days are to be ignored then set it to e.g. 4
    # If set to 0 then any day with more than 0 operational hours will be operational day
    min_hours_in_day = 0

    operational_days_json = calc_operational_json(customer_asset_identifier)

    count_op_days = 0

    # List of operational days by index 0 to 6
    op_days_list = []
    for c in operational_days_json:
        if c['op_hrs'] and c['op_hrs'] > min_hours_in_day :
            count_op_days += 1
            op_days_list.append(1)
        else :
           op_days_list.append(None)

    # Calculating operational days for the customer asset identifier based on installed date
    date_start = installed_date
    date_end = to_date_obj
    op_age = 0
    if (date_end - date_start).days < 8: # If date range within a week
        while date_start <= date_end:
            if op_days_list[(date_start.isoweekday() % 7)]:
                op_age += op_days_list[(date_start.isoweekday() % 7)]
            date_start += timedelta(days=1)
        return op_age
    else: # If date range is for more than a week
        start_days_till_sun = 0
        start_days_delta = []
        if date_start.isoweekday() != 1:
            while date_start.isoweekday() < 7:
                start_days_delta.append(date_start.isoweekday() % 7)
                date_start += timedelta(days=1)
                start_days_till_sun += 1
        end_days_till_sun = 0
        end_days_delta = []

        if date_end.isoweekday() != 1:
            while date_end.isoweekday() > 1:
                end_days_delta.append(date_end.isoweekday() % 7)
                date_end -= timedelta(days=1)
                end_days_till_sun += 1
        date_end -= timedelta(days=1)
        if len(end_days_delta) > 0:
            end_days_delta.append(end_days_delta[len(end_days_delta) - 1] - 1)
        no_of_weeks = (date_end - date_start).days / 7
        op_age = no_of_weeks * count_op_days
        delta_list = start_days_delta + end_days_delta

        for op in delta_list:
            if op_days_list and op_days_list[op]:
                op_age += op_days_list[op]
        return round(op_age)

class DimSelector(Having):
    def __init__(self, **args):
        # Just a hack to prevent any exceptions
        Having.__init__(self, type='equalTo', aggregation=None, value=None)

        self.having = {'having': {
            'type': 'dimSelector',
            'dimension': args['dimension'],
            'value': args['value'],
        }}


class LoggingHelper:

    @staticmethod
    def getExceptionMsg(exception):
        try:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_dict = {"Exception": exc_type, "File": fname, "Line": exc_tb.tb_lineno, "Message": str(exception)}
            return str(err_dict)
        except Exception as e:
            return 'Exception with Logging: "%s", Other exception: "%s"' % (str(e), str(exception))


def get_user_id_from_token(header):
    parts = header.split()
    token = parts[1]
    db_session = get_session()
    user_session = db_session.query(UserSession).filter_by(access_token=token).first()
    if user_session is None:
        print("user session is NULL for user_id")
    else:
        # logged_in_users[token] = {"user_id": user_session.user_id, "ekryp_partner_id": user_session.ekryp_partner_id}
        return user_session.user_id


def get_ekryp_partner_id_from_token(header):
    parts = header.split()
    token = parts[1]
    db_session = get_session()
    user_session = db_session.query(UserSession).filter_by(access_token=token).first()
    if user_session is None:
        print("user session is NULL for ekryp_partner_id")
    else:
        # logged_in_users[token] = {"user_id": user_session.user_id, "ekryp_partner_id": user_session.ekryp_partner_id}
        return user_session.ekryp_partner_id


def get_user_email_from_token(header):
    parts = header.split()
    token = parts[1]
    db_session = get_session()
    user_session = db_session.query(UserSession).filter_by(access_token=token).first()
    if user_session is None:
        print("user session is NULL for ekryp_partner_id")
    else:
        user = db_session.query(User).filter_by(id=user_session.user_id).first()
        # logged_in_users[token] = {"user_id": user_session.user_id, "ekryp_partner_id": user_session.ekryp_partner_id}
        return user.email_id


def remove_token_from_dict(header):
    parts = header.split()
    token = parts[1]
    if token in logged_in_users:
        logged_in_users.pop(token, None)

    return token





