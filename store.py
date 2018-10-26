import mysql.connector as mysql

db = mysql.connect(host='127.0.0.1', user='root', passwd='', database='dlm')
cursor = db.cursor()
query = "select id,category from categories"
cursor.execute(query)
rows = cursor.fetchall()
db.commit()
db.close()
categories = {}
for row in rows:
    categories[row[1]] = row[0]


def insert(values, category):
    db = mysql.connect(host='127.0.0.1', user='root',
                       passwd='', database='dlm')
    cursor = db.cursor()
    try:
        query = 'insert into articles(source,author,title,description,url,urlToImage,publishedAt) values("%s","%s",%s,%s,"%s","%s","%s")' % tuple(
            values)
        cursor.execute(query)
    except:
        pass
    try:
        query = "select id from articles where title=%s and publishedAt='%s'" % (
            values[2], values[-1])
        cursor.execute(query)
        result = cursor.fetchall()
        article_id = result[0][0]
        query = 'select id from a_to_c_predictions where article_id=%d' % (
            article_id)
        cursor.execute(query)
        result = cursor.fetchall()
        if(len(result) == 0):
            query = "insert into a_to_c_predictions(article_id,category_id) values(%d,%d) on duplicate KEY UPDATE category_id=%d" % (
                article_id, categories[category], categories[category])
        else:
            query = 'update a_to_c_predictions set category_id=%d where article_id=%d' % (
                categories[category], article_id)
        cursor.execute(query)
    except Exception as e:
        print e
        pass
    db.commit()
    db.close()
