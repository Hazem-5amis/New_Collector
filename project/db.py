import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv() 

def connect_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "mysql-1048f440-hazemkhamees09-54f8.l.aivencloud.com"),
            user=os.getenv("DB_USER", "avnadmin"),
            password=os.getenv("DB_PASSWORD", "AVNS_vaHAO19stzD5g28qGIp"),
            database=os.getenv("DB_NAME", "defaultdb"),
            port=os.getenv("DB_PORT", "15656"),
            ssl_disabled=False 
        )
    except mysql.connector.Error as err:
        print(f"❌ فشل الاتصال بقاعدة البيانات السحابية: {err}")
        return None

def save_articles(articles):
    db = connect_db()
    if db is None: return
        
    cursor = db.cursor()
    query = """
    INSERT IGNORE INTO articles (title, source_name, description, url, category, published_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    count = 0
    for article in articles:
        data = (
            article.get('title'),
            article.get('source', {}).get('name'),
            article.get('description'),
            article.get('url'),
            article.get('category_label'),
            article.get('publishedAt')
        )
        try:
            cursor.execute(query, data)
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"⚠️ خطأ أثناء حفظ المقال: {e}")
            
    db.commit()
    cursor.close()
    db.close()
    print(f"✅ تم حفظ {count} مقالاً جديداً في Aiven Cloud DB.")
