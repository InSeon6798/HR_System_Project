from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'study_db'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="study_db"
)



cursor = db.cursor()

# 페이지네이션 함수
def get_data_page(page, per_page):
    start_idx = (page - 1) * per_page
    cursor.execute(f"SELECT * FROM em_json LIMIT {start_idx},{per_page}")#채용
    return cursor.fetchall()

def get_test_page(page, per_page):
    start_idx = (page - 1) * per_page
    cursor.execute(f"SELECT * FROM today LIMIT {start_idx},{per_page}")#인력
    return cursor.fetchall()

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

    cursor.execute("SELECT COUNT(*) FROM em_json")
    total_rows = cursor.fetchone()[0]
    total_pages = (total_rows + per_page - 1) // per_page

    current_data = get_data_page(page, per_page)

    return render_template('index.html', data=current_data, page=page, total_pages=total_pages)
                                                                                        

@app.route('/test.html')
def test():
    page = request.args.get('page', default=1, type=int)
    per_page = 10

    cursor.execute("SELECT COUNT(*) FROM today")  # today 테이블 조회
    total_rows = cursor.fetchone()[0]
    total_pages = (total_rows + per_page - 1) // per_page

    current_data = get_test_page(page, per_page)  # 'today' 테이블 조회

    return render_template('test.html', data=current_data, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)





