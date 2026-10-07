import sqlite3

#接続
def connect_db():
  conn = sqlite3.connect("sales.db")
  conn.execute("PRAGMA foreign_keys = ON")
  #外部キー制約を有効化している

  return conn

#テーブル作成
def create_table():
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price INTEGER CHECK(price >= 0),
    status TEXT
  )
  """)

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS payment(
    id INTEGER PRIMARY KEY,
    datetime TEXT
  )
  """)

  cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_detail(
      id INTEGER PRIMARY KEY,
      payment_id INTEGER,
      product_id INTEGER,
      count INTEGER CHECK(count > 0),
      price INTEGER,
      FOREIGN KEY (payment_id) REFERENCES payment(id),
      FOREIGN KEY (product_id) REFERENCES product(id)
    )
    """)
  #FOREIGN KEY (payment_id) REFERENCES payment(id)    参照
  #存在しない会計IDを売り上げ明細に登録できない仕組み
  

  conn.commit()

  conn.close()

#商品登録
def add_product(name, category, price, status):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    INSERT INTO product(name, category, price, status)
    VALUES(?, ?, ?, ?)
  """,(
    name,
    category,
    price,
    status
  ))

  conn.commit()

  conn.close()

#商品データ取得
def get_product_data():
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    SELECT *
    FROM product
  """)

  data = cursor.fetchall()
  conn.close()

  return data

#商品編集
def edit_product(id, name, category, price, status):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    UPDATE product
    SET name = ?, category = ?, price = ?, status = ?
    WHERE id = ?
  """,(
    name,
    category,
    price,
    status,
    id
  ))

  conn.commit()

  conn.close()

#売り上げ登録
def add_payment(now):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    INSERT INTO payment(datetime)
    VALUES(?)
    """,(
      now,
    ))

  payment_id = cursor.lastrowid

  conn.commit()

  conn.close()

  return payment_id

#売り上げ明細登録
def add_sales_detail(payment_id, product_id, count, price):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    INSERT INTO sales_detail(payment_id, product_id, count, price)
    VALUES(?, ?, ?, ?)
  """,(
    payment_id,
    product_id,
    count,
    price
  ))

  conn.commit()

  conn.close()

def get_payment_data(selected_date):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    SELECT id
    FROM payment
    WHERE DATE(datetime) = ?
  """,(
    selected_date,
  ))

  payment_id = cursor.fetchall()

  conn.close()

  return payment_id

def get_sales_data(payment_id):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    SELECT payment.id, TIME(payment.datetime), product.name, sales_detail.count, sales_detail.price, sales_detail.id
    FROM sales_detail
    JOIN product
    ON sales_detail.product_id = product.id
    JOIN payment
    ON sales_detail.payment_id = payment.id
    WHERE payment_id = ?
  """,(
    payment_id,
  ))

  data = cursor.fetchall()

  conn.close()

  return data

def sales_data_update(sales_id, count):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    UPDATE sales_detail
    SET count = ?
    WHERE id = ?
  """,(
    count,
    sales_id
  ))

  conn.commit()

  conn.close()

def get_monthly_sales_data(select_date):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    SELECT product.name, 
          SUM(
            CASE
              WHEN strftime('%Y-%m', payment.datetime) = ?
              THEN sales_detail.count
              ELSE 0
            END
          ),
          SUM(
            CASE
              WHEN strftime('%Y-%m', payment.datetime) = ?
              THEN sales_detail.count * sales_detail.price
              ELSE 0
            END
          )
    FROM product
    LEFT JOIN sales_detail
    ON product.id = sales_detail.product_id
    LEFT JOIN payment
    ON sales_detail.payment_id = payment.id
    AND strftime('%Y-%m', payment.datetime) = ?
    GROUP BY product.id, product.name
  """,(
    select_date,
    select_date,
    select_date
  ))

  data = cursor.fetchall()

  conn.close()

  return data

def get_days_sales_data(select_date):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    SELECT DATE(payment.datetime), SUM(sales_detail.count * sales_detail.price)
    FROM payment
    JOIN sales_detail
    ON payment.id = sales_detail.payment_id
    WHERE strftime('%Y-%m', payment.datetime) = ?
    GROUP BY DATE(payment.datetime)
  """,(
    select_date,
  ))

  data = cursor.fetchall()

  conn.close()

  return data

def delete_payment(payment_id):
  conn = connect_db()

  cursor = conn.cursor()

  cursor.execute("""
    DELETE FROM sales_detail
    WHERE payment_id = ?
  """,(
    payment_id,
  ))

  cursor.execute("""
    DELETE FROM payment
    WHERE id = ?
  """,(
    payment_id,
  ))

  conn.commit()

  conn.close()
    
create_table()