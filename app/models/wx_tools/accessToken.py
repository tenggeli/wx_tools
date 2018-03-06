#  -*- coding: utf-8 -*-

import json
from app.utils.MysqlTools import MysqlTools


from app.utils.MyLogger import MyLogger

logger = MyLogger.getLogger()

class accessToken(object):
    def save(self, obj):
        session = MysqlTools.getManualSession()
        new_id = None
        try:
            session.add(obj)
            session.commit()
            new_id = obj.id
            return new_id
        except Exception, e:
            session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close()
        return new_id

    def getAccessToken(self):
        status = 0
        msg = 'success'
        sql = '''
        SELECT access_token,expires_time
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
