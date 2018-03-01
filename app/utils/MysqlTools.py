#  -*- coding: utf-8 -*-

'''
Created on 2017年5月4日

@author: tony
'''
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import create_engine
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from app.jobscheduler.log.MyLogger import MyLogger
logger = MyLogger.getLogger()
from harrypotte.jobscheduler.config import JobConfig

# from lib.log4me import MyLogger
# logger = MyLogger.getLogger()


class MysqlTools(object):
    '''
    classdocs
    '''
    engine = None
    datax_engine = None

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def initConnection():
        if MysqlTools.engine is None:
            try:
                MysqlTools.engine = create_engine(
                    JobConfig.mysql_conn_online, pool_size=30, max_overflow=-1, pool_recycle=500, echo=True)
            except Exception, e:
                logger.error("initConnection is Error:%s" % (e))
        if MysqlTools.datax_engine is None:
            try:
                MysqlTools.datax_engine = create_engine(
                    JobConfig.mysql_conn_online, pool_size=30, max_overflow=-1, pool_recycle=500, echo=True)
            except Exception, e:
                logger.error("initConnection is Error:%s" % (e))

    @staticmethod
    def getEngine():
        try:
            conn = create_engine(JobConfig.mysql_conn_online)

        except Exception, e:
            logger.error("Mysql is Error:%s" % (e))
        return conn

    @staticmethod
    def getSession():
        MysqlTools.initConnection()
#         DBSession = sessionmaker(bind=MysqlTools.engine)
#         # 创建session对象:
#         session = DBSession()
        session_factory = sessionmaker(autocommit=True,
                                       autoflush=True, bind=MysqlTools.engine)

        session = scoped_session(session_factory)
        return session

    @staticmethod
    def getManualSession():
        MysqlTools.initConnection()
#         DBSession = sessionmaker(bind=MysqlTools.engine)
#         # 创建session对象:
#         session = DBSession()
        session_factory = sessionmaker(autocommit=False,
                                       autoflush=False, bind=MysqlTools.engine)

        session = scoped_session(session_factory)
        return session

    @staticmethod
    def getManualDataXSession():
        MysqlTools.initConnection()
        session_factory = sessionmaker(autocommit=False,
                                       autoflush=False, bind=MysqlTools.datax_engine)

        session = scoped_session(session_factory)
        return session

    @staticmethod
    def getSessionByEngine(engine):
        DBSession = sessionmaker(bind=engine)
        # 创建session对象:
        session = DBSession()
        return session

    def transTypeValue(self, val):
        value = ''
#         if isinstance(val, (int, float)):
        if val is None:
            value = 'NULL'
        else:
            value = str(val)
        return value
        pass

    def getDbNameStr(self, conf_path):
        file = open(conf_path)
        name_str = ''
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                #                 name_str = name_str + str(line).strip() + ','
                #                 print '----------------------------------------------------'
                #                 print name_str
                #                 print '*************************'
                #                 print line
                #                 print '===================================================='
                #                 print line.index('#')
                if line.find('#') == 0:
                    continue
                name_str = name_str + line.strip('\n') + ','
        if name_str is not None:
            name_str = name_str[0:-1]
        return name_str

    def getDbUpdateStr(self, conf_path, value_list):
        file = open(conf_path)
        name_str = ''
        num = 0
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                if line.find('#') == 0:
                    continue
                num = num + 1
#                 print type(value_list[num])
#                 print value_list[num]
#                 print value_list[num].strftime('%Y-%m-%d %H:%M:%S')
                if value_list[num] is None:
                    name_str = name_str + \
                        line.strip(
                            '\n') + "=" + str(self.transTypeValue(value_list[num])) + "" + ','

                else:
                    name_str = name_str + \
                        line.strip(
                            '\n') + "='" + str(self.transTypeValue(value_list[num])) + "'" + ','
#                 name_str = name_str + ','
        if name_str is not None:
            name_str = name_str[0:-1]
        return name_str

    def getDbValueStr(self, value_list):
        value_str = ''
        for i, s in enumerate(value_list):

            if i == 0:
                continue
            if s is None:
                value_str = value_str + str(self.transTypeValue(s)) + ','
            else:
                value_str = value_str + "'" + \
                    str(self.transTypeValue(s)) + "'" + ','

#             s=self.transTypeValue(s)
#             value_str=value_str+"'"+str(s)+"'" + ','
#             value_str = value_str + ','
        if value_str is not None:
            value_str = value_str[0:-1]
        return value_str


    def save(self, obj):

        try:
            session = MysqlTools.getManualSession()
            session.add(obj)
            session.commit()
        except Exception, e:
            if session is not None:
                session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            #             if session is not None:
            #                 session.close()
            #             if MysqlTools.engine is not None:
            #                 MysqlTools.engine.close()
            pass

#     一、当天或当日插入的数据：
#     1、传统对比判断：SELECT * FROM `t` WHERE DATE_FORMAT(addTime,'%Y-%m-%d') = date_format(now(),'%Y-%m-%d')");
#     2、第一点的简写：SELECT * FROM `t` WHERE addTime >= date_format(NOW(),'%Y-%m-%d');
#     3、利用函数判断：SELECT * FROM `t` WHERE DATEDIFF(addTime,NOW()) =0;//推荐此方法
# 4、利用时间戳判断：SELECT * FROM `t` WHERE addTime BETWEEN
# (UNIX_TIMESTAMP(now()-86440)) AND now();

    def getModJobList(self):
        session = MysqlTools.getSession()
        sql = 'select * from job_info2 where TIMESTAMPDIFF(SECOND,create_time,NOW()) <= ' + str(
            1 * 60 * 60)
#         sql='select * from job_info where TIMESTAMPDIFF(SECOND,mod_time,NOW()) <= '+str(2*60*60)
#         print sql
        results = None
        try:
            results = session.execute(sql).fetchall()
        except Exception, e:
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close
        return results

    def getJobInfoList(self):
        session = MysqlTools.getSession()
        sql = 'select * from job_info '
        results = None
        try:
            results = session.execute(sql).fetchall()
        except Exception, e:
            logger.error("Mysql is Error:%s" % (e))
        finally:
            #             if session:
            #                 session.close
            pass
        return results

    def insertOrUpdateJobInfo(self, tablename, name_str, value_str, update_str):
        #         insert_sql="insert into datax_app ({0}) values ({1})".format(fields_str,value_str)
        session = MysqlTools.getSession()
        sql = str('insert into ' + tablename +
                  '({0}) values ({1}) ON DUPLICATE KEY UPDATE {2}').format(name_str, value_str, update_str)
#         print sql
        try:
            session.execute(sql)
            session.commit()
        except Exception, e:
            #             self.conn.rollback()
            # logger.error("Mysql Error insert single record %d: %s" % (e.args[0], e.args[1]))
            print "Mysql Error insert single record %d: %s" % (e.args[0], e.args[1])
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session:
                session.close

    def getTimeSux(self):
        millis = int(round(time.time() * 1000))  # round()方法返回 x 的小数点四舍五入到n个数字
        return millis

    def insertJobRunLog(self, jobRunInfo, status):
        jobRunInfo.starttime = self.getTimeSux()
#         jobRunInfo.job_status=status

        session = MysqlTools.getSession()
        try:
            session.add(jobRunInfo)
            session.commit
        except Exception, e:
            session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session is not None:
                session.close()
#             if MysqlTools.engine is not None:
#                 MysqlTools.engine.close()

    def updateJobRunLog(self, jobRunInfo, status):
        session = MysqlTools.getSession()
        sql = '''
                update job_run_info set status='{status}' where id='{id}'
            '''.format(status=jobRunInfo.status, id=jobRunInfo.id)
        try:
            session.execute(sql)
            session.commit
        except Exception, e:
            session.rollback()
            logger.error("Mysql is Error:%s" % (e))
        finally:
            if session is not None:
                session.close()

        pass

    def test(self):
            #     ms=MysqlConnection()
        #     ms.getConnection()
        #     MysqlConnection.getConnection()
        #         engine = create_engine("mysql+mysqldb://root:root@127.0.0.1:3306/my_job_db?charset=utf8")
        #         # 创建DBSession类型:
        #         DBSession = sessionmaker(bind=engine)
        #         # 创建session对象:
        #         session = self.getSession()
        # 创建新User对象:
        #     new_user = Users(id='5', name='Bob')
        #         new_user = Users(name='王力宏2')

        #         job = JobInfo(job_name='job3', job_file_path='/fs/path1', job_params='p1 p2', job_dept='bigdata',
        #                     job_desc='hive job', creater='张学友2', create_time='2017-05-06 17:10:00.000', priority=5, tag_depend='/tag1', is_check=1, tag_store='/tag2,/tag3', cron='Day(03:30)', editor='', mod_time='2017-05-05 18:45:00.000',
        #                     retry_num='2')
        #         job=JobInfo()
        #     #
        #         # 添加到session:
        # #         session.add(job)
        #         self.save(job)
        #     #     session.add(new_user)
        #         # 提交即保存到数据库:
        #         session.commit()
        #         ms = MysqlTools()
        #     rs = ms.getModJobList()
        #     print rs

        #         table_name = 'job_info'
        #         name_str = ''
        #         value = str = ''
        #         path = 'H:\\Project\bi.jobscheduler\config\job_info_column.config'
        #         print path
        # print
        # ms.getDbNameStr('H:\\Project\\bi.jobscheduler\\config\\job_info_column.config')

        # 关闭session:
        #         session.close()
        print 'success.....'


if __name__ == '__main__':
    print 'hello'
    ms = MysqlTools()
    ms.test()
#     conf_path = 'H:\\Project\\bi.jobscheduler\\config\\job_info_column.config'
# #     ms=MysqlConnection()
# #     ms.getConnection()
# #     MysqlConnection.getConnection()
#     engine = create_engine("mysql+mysqldb://root:root@127.0.0.1:3306/my_job_db?charset=utf8")
#     # 创建DBSession类型:
#     DBSession = sessionmaker(bind=engine)
#     # 创建session对象:
#     session = DBSession()
#     ms = MysqlTools()
#     rs = ms.getModJobList()
#     tablename='job_info'
#     for row in rs:
#         print type(row)
# #         print row.values()
# #         print row.values()[6]
# #         print row.values()[7]
# #         print type(row.values()[7])
#
# #         sqlalchemy.engine.result.RowProxy
#         print ms.getDbUpdateStr(conf_path, row.values())
#         name_str=ms.getDbNameStr(conf_path)
#         value_str=ms.getDbValueStr(row.values())
#         update_str=ms.getDbUpdateStr(conf_path, row.values())
#         ms.insertOrUpdateJobInfo(tablename, name_str, value_str, update_str)

    # 关闭session:
#     session.close()
    print 'success.....'
