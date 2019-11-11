# 主要SQL function
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
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   cursor = db.cursor()

   print('name ', target)
   
  
   sql = "SELECT * FROM movie WHERE user_name = %s"

   movie = None
   try:
      cursor.execute(sql, target)
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         
         print ("movie=%s " % \
               (movie))
   except:
      print ("Error: unable to fetch data")
   
   
   db.close()

def movie_update(target):
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   cursor = db.cursor()

   print('name ', target)
   
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   movie = list()
   try:
      cursor.execute(sql, target)
      
      results = cursor.fetchall()
      for row in results:
         movie = row[1]
         
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
      cursor.execute(sql_update)
      db.commit()
   except Exception as e:
      print(e)
      db.rollback()


   
   
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

   # string to list
   movie_list = list()
   rating_list = list()
   tmdbId_list = list()
   tmdbId_rating_list = list()
   if len(movie) != 0:
      movie_list = movie.split(',')
   if len(ratings) != 0:
      rating_list = ratings.split(',')
   tmdbId_list = str(tmdbId).split(',')
   tmdbId_rating_list = str(rating).split(',')

   
   print(len(movie_list))
   print(len(rating_list))

   print(movie_list)
   print(rating_list)
   
   for tmp in tmdbId_list:
      if tmp in movie_list:
         print(movie_list.index(tmp))
         pair = movie_list.index(tmp)
         del movie_list[pair]
         del rating_list[pair]
         print(movie_list)
         print(rating_list)
  


   
   # for tmp in tmdbId:
   movie_list.append(tmdbId)
   print('movie ', movie_list)
   str1 = ','.join(str(e) for e in movie_list)
   print(str1)

   #rating
  
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
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   cursor = db.cursor()

   print('name ', target)

   repeat_insert = movie_exists(target, tmdbId)
   if repeat_insert == 1:
      db.close()
      return
   
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      cursor.execute(sql, target)
      
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         
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
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   cursor = db.cursor()

   print('name ', target)
   
   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      cursor.execute(sql, target)
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         
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


def movie_exists(target, tmdbId):
   db  =  pymysql.connect ( host = '127.0.0.1' ,  user = 'root' ,  passwd = "" ,  db = 'test' )
   cursor = db.cursor()

   # 1:exist 0:not exists 
   result = 0

   sql = "SELECT * FROM movie WHERE user_name = %s"
   
   favorite = list()
   try:
      cursor.execute(sql, target)
      results = cursor.fetchall()
      for row in results:
         favorite = row[3]
         
         print ("movie=%s " % \
               (favorite))
   except:
      print ("Error: unable to fetch data")

   favorite_list = list()
   if len(favorite) != 0:
      favorite_list = favorite.split(',')
   
   if str(tmdbId) in favorite_list:
      result = 1
   else:
      result = 0


   db.close()
   return result



if __name__=='__main__':
   # movie_exists('Elmo', 777)
   # favorite_update('Elmo', 862)
   # movie_update('jh1g')
   # update_bpr('emschen', 1)
   get_bpr('1234')
   # clear_column('', 'watched_movie_id')
   # clear_column('', 'rating')
   # rating_update('emschen', '862,949,710,687,9598', '3,4,5,4,5')
   # rating_update_test('1234')
   # movie, rating = get_movie_rating('1234')
   # md = dict()
   # print(len(movie))
   # print(len(rating))
   # for index in range(len(movie)):
   #    md[movie[index]] = rating[index]
   # print(md)