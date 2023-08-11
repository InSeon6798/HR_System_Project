from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="study_db"
)

cursor = db.cursor()

# 공유하는 함수로 데이터를 가져오는 로직을 구현
def get_page_data(table_name, page, per_page):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    total_rows = cursor.fetchone()[0]
    total_pages = (total_rows + per_page - 1) // per_page

    cursor.execute(f"SHOW COLUMNS FROM {table_name}")  # 테이블의 컬럼 정보 조회
    columns = [column[0] for column in cursor.fetchall()]

    start_idx = (page - 1) * per_page
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {start_idx},{per_page}")
    current_data = cursor.fetchall()

    return current_data, columns, total_pages

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/page2.html')
def page2():
    return render_template('page2.html')

@app.route('/index.html')
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 10

    current_data, columns, total_pages = get_page_data("em_json", page, per_page)

    return render_template('index.html', data=current_data, columns=columns, page=page, total_pages=total_pages)

@app.route('/test.html')
def test():
    page = request.args.get('page', default=1, type=int)
    per_page = 10


    current_data, columns, total_pages = get_page_data("today", page, per_page)

    return render_template('test.html', data=current_data, columns=columns, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)

