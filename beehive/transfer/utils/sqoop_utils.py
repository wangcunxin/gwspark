# -*- coding:utf8 -*-

__author__ = 'kevin'


class HiveUtil:
    def __init__(self):
        pass

    @staticmethod
    def templet_insert_sql(tb, columns):
        hive_cmd = "hive -e 'insert overwrite table %s.%s select %s from %s.%s;'" % (
            "beehive", tb, columns, "default", tb)
        return hive_cmd

    @staticmethod
    def templet_insert_sql_partition(tb, dat, columns):
        hive_cmd = "hive -e 'insert overwrite table %s.%s partition(dat='%s') " \
                   "select %s from %s.%s where dat='%s';'" % ("beehive", tb, dat, columns, "default", tb, dat)
        return hive_cmd

    @staticmethod
    def templet_sqoop_sql_oracle():
        cmd = '''
        sqoop import \
        --connect "jdbc:oracle:thin:@%(host)s:%(port)s:%(sid)s" \
        --username %(username)s \
        --password %(password)s \
        --table "%(db_name)s.%(tb_name)s" \
        --columns "%(columns)s" \
        --fields-terminated-by %(sep)s \
        --hive-drop-import-delims \
        --target-dir /user/sqoop/%(hive_tb_name)s  \
        --append \
        -m 1;
        '''
        return cmd

    @staticmethod
    def templet_sqoop_sql_oracle_partition():
        cmd = '''
        sqoop import \
        --connect "jdbc:oracle:thin:@%(host)s:%(port)s:%(sid)s" \
        --username %(username)s \
        --password %(password)s \
        --table "%(db_name)s.%(tb_name)s" \
        --columns "%(columns)s" \
        --where "to_char(ADDTIME,'yyyyMMdd')='%(dat)s'" \
        --fields-terminated-by %(sep)s \
        --hive-drop-import-delims \
        --target-dir /user/sqoop/%(hive_tb_name)s/dat='%(dat)s'  \
        --append \
        -m 1;
        '''
        return cmd

    @staticmethod
    def templet_sqoop_sql_postgresql_partition():
        cmd = '''
        sqoop import \
        --driver org.postgresql.Driver \
        --connect "jdbc:postgresql://%(host)s:%(port)s/%(db_name)s" \
        --username %(username)s \
        --password %(password)s \
        --table "%(db_name)s.%(tb_name)s" \
        --columns "%(columns)s" \
        --where "to_char(ADDTIME,'yyyyMMdd')='%(dat)s'" \
        --fields-terminated-by %(sep)s \
        --hive-drop-import-delims \
        --target-dir /user/sqoop/%(hive_tb_name)s/dat='%(dat)s'  \
        --append \
        -m 1;
        '''
        return cmd

    @staticmethod
    def templet_sqoop_sql_mysql():
        cmd = '''
        sqoop import \
        --connect "jdbc:mysql://%(host)s:%(port)s/%(db_name)s" \
        --username %(username)s \
        --password %(password)s \
        --table "%(tb_name)s" \
        --columns "%(columns)s" \
        --fields-terminated-by %(sep)s \
        --hive-drop-import-delims \
        --target-dir /user/sqoop/%(hive_tb_name)s  \
        --append \
        -m 1;
        '''
        return cmd

    pass
