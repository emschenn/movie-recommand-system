#!/usr/bin/python3
#  SQL練習用檔案
import pymysql

def insert(name, id, rating, favorite, topic):
    # 打开数据库连接
    db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
    
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    print('name   ' + name)
    
    # SQL 插入语句
    #movie_info
    '''
    sql = """INSERT INTO movie(user_name, watched_movie_id, rating)
            VALUES (name, '1,50,97', '2,3,5', 'sth.')"""
    '''
    sql = "INSERT INTO movie(`user_name`, `watched_movie_id`, `rating`, `favorite`, `like_topic`) VALUES (%s, %s, %s, %s, %s)"

    try:
        # 执行sql语句
        cursor.execute(sql, (name, id, rating, favorite, topic))
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误则回滚
        print(e)
        db.rollback()
    
    # 关闭数据库连接
    db.close()
    
if __name__=='__main__':
    insert('tmp_name', '', '', '', '')
    
