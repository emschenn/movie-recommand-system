
import pymysql

def user_search(target):
   
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"

   user_name = None
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         user_name = row[0]
         # 打印结果
         print ("user_name=%s " % \
               (user_name ))
   except:
      print ("Error: unable to fetch data")

   if user_name is None:
      print('No user')
      return True
   else:
      print('search result ', user_name)
      return False
   
   # 关闭数据库连接
   db.close()

def movie_list_search(target):
    # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"

   movie = None
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         # 打印结果
         print ("movie=%s " % \
               (movie))
   except:
      print ("Error: unable to fetch data")
   
   # 关闭数据库连接
   db.close()

def movie_update(target):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   movie = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         # 打印结果
         print ("movie=%s " % \
               (movie))
   except:
      print ("Error: unable to fetch data")

   movie_list = movie.split(',')
   movie_list.append('7')
   print(movie_list)
   str1 = ','.join(str(e) for e in movie_list)
   print(str1)
  
   sql_update = "UPDATE movie SET watched_movie_id='" + str1 + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(sql_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()

# 修bug用 只增加一個評分
def rating_update_test(target):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   rating = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         rating = row[2]
         # 打印结果
         print ("rating=%s " % \
               (rating))
   except:
      print ("Error: unable to fetch data")

   rating_list = rating.split(',')
   rating_list.append('4.0')
   print(rating_list)
   str1 = ','.join(str(e) for e in rating_list)
   print(str1)
  
   sql_update = "UPDATE movie SET watched_movie_id='" + str1 + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(sql_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()

def update(target, like_topic, movieId):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   name_update = "UPDATE movie SET user_name='" + target + "' WHERE user_name='" + 'tmp_name' + "'"
   try:
      # 执行SQL语句
      cursor.execute(name_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()

   
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   movie = list()
   rating = list()
   topic = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         rating = row[2]
         topic = row[4]
         # 打印结果
         print ("movie=%s " % \
               (movie))
         print ("rating=%s " % \
               (rating))
         print ("topic=%s " % \
               (topic))
   except:
      print ("Error: unable to fetch data")

   #movie
   print(movie)
   movie_list = list()
   if len(movie) != 0:
      movie_list = movie.split(',')
   for tmp in movieId:
      movie_list.append(tmp)
   print('movie ', movie_list)
   str1 = ','.join(str(e) for e in movie_list)
   print(str1)
  
   movie_update = "UPDATE movie SET watched_movie_id='" + str1 + "' WHERE user_name='" + target + "'"

   #rating
   rating_list = list()
   if len(rating) != 0:
      rating_list = rating.split(',')
   for tmp in movieId:
      rating_list.append('5')
   print('rating', rating_list)
   str1 = ','.join(str(e) for e in rating_list)
   print(str1)

   rating_update = "UPDATE movie SET rating='" + str1 + "' WHERE user_name='" + target + "'"

   #movie
   topic_list = list()
   if len(topic) != 0:
      topic_list = topic.split(',')
   for tmp in like_topic:
      topic_list.append(tmp)
   str1 = ','.join(str(e) for e in topic_list)
   print(str1)

   topic_update = "UPDATE movie SET like_topic='" + str1 + "' WHERE user_name='" + target + "'"

  
   try:
      # 执行SQL语句
      cursor.execute(movie_update)
      cursor.execute(rating_update)
      cursor.execute(topic_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()
   


def rating_update(target, tmdbId, rating):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   movie = list()
   ratings = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         ratings = row[2]
         # 打印结果
         print ("movie=%s " % \
               (movie))
         print ("ratings=%s " % \
               (ratings))
   except:
      print ("Error: unable to fetch data")

   #movie
   print(tmdbId)
   movie_list = list()
   if len(movie) != 0:
      movie_list = movie.split(',')
   # for tmp in tmdbId:
   movie_list.append(tmdbId)
   print('movie ', movie_list)
   str1 = ','.join(str(e) for e in movie_list)
   print(str1)

   #rating
   rating_list = list()
   if len(ratings) != 0:
      rating_list = ratings.split(',')
   # for tmp in rating:
   rating_list.append(rating)
   print('rating', rating_list)
   str2 = ','.join(str(e) for e in rating_list)
   print(str2)

  
   movie_update = "UPDATE movie SET watched_movie_id='" + str1 + "' WHERE user_name='" + target + "'"
   rating_update = "UPDATE movie SET rating='" + str2 + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(movie_update)
      cursor.execute(rating_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()

def favorite_update(target, tmdbId):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         # 打印结果
         print ("movie=%s " % \
               (favorite))
   except:
      print ("Error: unable to fetch data")

   #movie
   print(tmdbId)
   favorite_list = list()
   if len(favorite) != 0:
      favorite_list = favorite.split(',')
   # for tmp in tmdbId:
   favorite_list.append(tmdbId)
   print('movie ', favorite_list)
   str1 = ','.join(str(e) for e in favorite_list)
   print(str1)


  
   favorite_update = "UPDATE movie SET favorite='" + str1 + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(favorite_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()

def get_favorite(target):
      # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         # 打印结果
         print ("movie=%s " % \
               (favorite))
   except:
      print ("Error: unable to fetch data")

   favorite_list = list()
   if len(favorite) != 0:
      favorite_list = favorite.split(',')

   return favorite_list

def favorite_remove(target, tmdbId):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         # 打印结果
         print ("movie=%s " % \
               (favorite))
   except:
      print ("Error: unable to fetch data")

   #movie
   print(tmdbId)
   favorite_list = list()
   if len(favorite) != 0:
      favorite_list = favorite.split(',')
   # for tmp in tmdbId:
   favorite_list.remove(tmdbId)
   print('movie ', favorite_list)
   str1 = ','.join(str(e) for e in favorite_list)
   print(str1)


  
   favorite_update = "UPDATE movie SET favorite='" + str1 + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(favorite_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   # 关闭数据库连接
   db.close()

def get_bpr(target):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   bpr = None
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         bpr = row[5]
         # 打印结果
         print ("bpr=%s " % \
               (bpr))
   except:
      print ("Error: unable to fetch data")

   
   # 关闭数据库连接
   db.close()
   return bpr

def update_bpr(target, value):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   bpr = None
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         bpr = row[5]
         # 打印结果
         print ("bpr=%s " % \
               (bpr))
   except:
      print ("Error: unable to fetch data")


   bpr_update = "UPDATE movie SET BPR='" + str(value) + "' WHERE user_name='" + target + "'"
  
   try:
      # 执行SQL语句
      cursor.execute(bpr_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()

   
   # 关闭数据库连接
   db.close()

def get_movie_rating(target):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # SQL 查询语句
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   movie = list()
   ratings = list()
   try:
      # 执行SQL语句
      cursor.execute(sql, target)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         ratings = row[2]
         # 打印结果
         print ("movie=%s " % \
               (movie))
         print ("ratings=%s " % \
               (ratings))
   except:
      print ("Error: unable to fetch data")

   movie_list = list()
   if len(movie) != 0:
      movie_list = movie.split(',')
   ratings_list = list()
   if len(ratings) != 0:
      ratings_list = ratings.split(',')

   
   # 关闭数据库连接
   db.close()
   return movie_list, ratings_list

def clear_column(target, col):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('name ', target)
   
   # # SQL 查询语句
   # sql = "SELECT * FROM movie WHERE user_name = %s"

   clear_update = "UPDATE movie SET " + col +"='" + "" + "' WHERE user_name='" + target + "'"
   print(clear_update)
  
   try:
      # 执行SQL语句
      cursor.execute(clear_update)
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


'''

def happiness_movie(num):
    # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()
   
   # SQL 查询语句
   sql = "SELECT happiness FROM movie"

   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      results = cursor.fetchall()
      print (num)
      
      for row in results[num]:
         happiness = row
        
         # 打印结果
         print ("happiness=%s " % \
               (happiness ))
      
   except:
      print ("Error: unable to fetch data")

def anger_movie(num):
    # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()
   
   # SQL 查询语句
   sql = "SELECT anger FROM movie"

   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      results = cursor.fetchall()
      print (num)
      
      for row in results[num]:
         anger = row
        
         # 打印结果
         print ("anger=%s " % \
               (anger ))
      
   except:
      print ("Error: unable to fetch data")

def neutral_movie(num):
    # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()
   
   # SQL 查询语句
   sql = "SELECT neutral FROM movie"

   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      results = cursor.fetchall()
      print (num)
      
      for row in results[num]:
         neutral = row
        
         # 打印结果
         print ("neutral=%s " % \
               (neutral ))
      
   except:
      print ("Error: unable to fetch data")

def fear_movie(num):
    # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()
   
   # SQL 查询语句
   sql = "SELECT fear FROM movie"

   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      results = cursor.fetchall()
      print (num)
      
      for row in results[num]:
         fear = row
        
         # 打印结果
         print ("fear=%s " % \
               (fear ))
      
   except:
      print ("Error: unable to fetch data")

def new_insert(name, topic, id):
   # 打开数据库连接
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   
   rating = list()
   for tmp in id:
      rating.append(5)

   str1 = ','.join(str(e) for e in rating)
   str2 = ','.join(str(e) for e in id)
   str3 = ','.join(str(e) for e in topic)
   
   
   # 使用cursor()方法获取操作游标 
   cursor = db.cursor()

   print('insert name   ' + name)
   
   # SQL 插入语句
   #movie_info
   
   sql = """INSERT INTO movie(user_name, watched_movie_id, rating)
            VALUES (name, '1,50,97', '2,3,5', 'sth.')"""
   
   sql = "INSERT INTO movie(`user_name`, `watched_movie_id`, `rating`, `favorite`, `like_topic`) VALUES (%s, %s, %s, %s, %s)"

   try:
      # 执行sql语句
      cursor.execute(sql, (name, str2, str1, 'NULL', str3))
      # 提交到数据库执行
      db.commit()
   except Exception as e:
      # 如果发生错误则回滚
      print(e)
      db.rollback()
   
   # 关闭数据库连接
   db.close()

'''

if __name__=='__main__':
   # movie_update('jh1g')
   update_bpr('1234', 0)
   # get_bpr('1234')
   # clear_column('1234', 'watched_movie_id')
   # clear_column('1234', 'rating')
   # rating_update('1234', '287947,329996,429617', '4, 5, 3')
   # rating_update_test('1234')
   # movie, rating = get_movie_rating('1234')
   # md = dict()
   # print(len(movie))
   # print(len(rating))
   # for index in range(len(movie)):
   #    md[movie[index]] = rating[index]
   # print(md)