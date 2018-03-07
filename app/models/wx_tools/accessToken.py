#  -*- coding: utf-8 -*-
# IngressController.py
import json, datetime, time
from app.utils.MysqlTools import MysqlTools


from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

class accessToken(object):


    def save(self, obj):
        pass

    def getAccessToken(self):
        status = 0
        msg = 'success'
        sql = '''
        SELECT 
          access_token,
          expires_time
        FROM access_token_list
        WHERE status = 1
        '''
        results = []
        session = MysqlTools.getSession()
        try:
            results = session.execute(sql).fetchall()
        except Exception, e:
            status = 1
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close()
        return results, status, msg

    def updateAccessToken(self, urlResp):
        session = MysqlTools.getSession()
        access_token = urlResp['access_token']
        expires_in = urlResp['expires_in']
        air_time = datetime.datetime.now()
        d2 = air_time + datetime.timedelta(seconds=7200)
        expires_time_stamp = time.mktime(d2.timetuple())

        try:
            sql = '''
                update 
                    access_token_list 
                set access_token='{}' ,expires_in = {},air_time = '{}', expires_time = {} where status=1
            '''.format(access_token, expires_in, air_time, expires_time_stamp)
            session.execute(sql)

        except Exception, e:
            session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close()

    def insertAccessToken(self, urlResp):
        session = MysqlTools.getSession()

        access_token = urlResp['access_token']
        expires_in = urlResp['expires_in']
        air_time = datetime.datetime.now()
        d2 = air_time + datetime.timedelta(seconds=expires_in)
        expires_time_stamp = time.mktime(d2.timetuple())
        access_token_columns = 'access_token,air_time,expires_in,expires_time,status'
        value_str = str("'{0}','{1}',{2},{3},{4}").format(access_token, air_time, expires_in, expires_time_stamp, 1)
        sql = str('insert into access_token_list ' +
                  '({0}) values ({1})').format(access_token_columns, value_str)
        try:
            session.execute(sql)
        # session.commit()
        except Exception, e:
            session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close