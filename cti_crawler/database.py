import re
import pymysql, datetime
from pymysql.converters import escape_string

class CTI_DB(object):
    def __init__(self, tableName):
        self.tableName = tableName

    def connection(self):
        try:
            db=pymysql.connect(host='cti.ckhlebdeaf8u.us-east-1.rds.amazonaws.com', user='seit', password='cti_seit666', database='ThreatIntelligence', charset='utf8mb4')
        except Exception as e:
            print("Connection to database failed!")
        return db

    def create_table(self, db):
        sql = "CREATE TABLE IF NOT EXISTS " + self.tableName + " (`id` INT NOT NULL AUTO_INCREMENT, `title` VARCHAR(100), `author` VARCHAR(40), `publishdate` VARCHAR(40), `content` LONGTEXT, `tags` VARCHAR(256), `url` VARCHAR(256) unique, PRIMARY KEY (id, url));"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def create_filteredtable(self, db):
        sql = "CREATE TABLE IF NOT EXISTS " + self.tableName + " (`id` INT NOT NULL AUTO_INCREMENT, `create_time` VARCHAR(80), `title` VARCHAR(100), `author` VARCHAR(40), `publishdate` VARCHAR(40), `content` LONGTEXT, `tags` VARCHAR(256), `url` VARCHAR(256) unique, PRIMARY KEY (id, url));"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def drop_table(self, db):
        sql = "DROP TABLE " + self.tableName
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def add_item(self, item, db):
        cursor = db.cursor()
        item_data = (item['title'], item['author'], item['publish_date'], item['contents'], item['tags'], item['url'])
        sql = "INSERT IGNORE INTO " + self.tableName + " VALUES (NULL,'%s','%s','%s','%s','%s','%s')" % item_data
        cursor.execute(sql)
        db.commit()
        cursor.close()

    def filter_CPS(self, db):
        cursor = db.cursor()
        cursor.execute('SHOW TABLES')
        table_list = cursor.fetchall()
        for table in table_list:
            if table[0] == self.tableName:
                continue
            sql = "select count(*) from information_schema.columns where table_name = '%s' and column_name = 'content'"%table[0]
            cursor.execute(sql)
            fit_tuple=cursor.fetchall()
            if fit_tuple[0][0] == 1:
                args = ["embed.*", "embedded.*", "IoT.*", "sensor.*", "physical.*", "automobile.*", "automotive.*", "car.*", "home.*", "vehicle.*"]
                for arg in args:
                    sql2 = '''select * from {} where `content` regexp "{}"'''.format(table[0], r''+arg+'')
                    cursor.execute(sql2)
                    filtered_content=cursor.fetchall()
                    if len(filtered_content) != 0:
                        title=escape_string(filtered_content[0][1])
                        author=escape_string(filtered_content[0][2])
                        publishdate=escape_string(filtered_content[0][3])
                        content=escape_string(filtered_content[0][4])
                        tags=escape_string(filtered_content[0][5])
                        url=escape_string(filtered_content[0][6])
                        dt=escape_string(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        
                        sql3 = "INSERT INTO {} (create_time, title, author, publishdate, content, tags, url) SELECT '{}', '{}', '{}', '{}', '{}', '{}', '{}' FROM DUAL WHERE NOT EXISTS (SELECT * FROM {} WHERE url='{}')".format(self.tableName, dt, title, author, publishdate, content, tags, url, self.tableName, url)
                        # sql = "INSERT INTO " + self.tableName+  " VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(dt, title, author, publishdate, content, tags, url)
                        cursor.execute(sql3)
                        db.commit()

if __name__ == '__main__':
    source = CTI_DB('cti_cps')
    db=source.connection()
    source.create_filteredtable(db)
    source.filter_CPS(db)