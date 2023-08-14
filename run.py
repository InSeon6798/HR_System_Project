from flask import Flask, render_template, request, redirect, url_for, session, abort
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
def main():
    return render_template('login.html')

#로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 이 예시에서는 간단하게 사번과 비밀번호가 일치하면 로그인 성공으로 가정합니다.
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user_data = cursor.fetchone()

        if user_data:
            session['username'] = username
            print('로그인성공')
            return render_template('main.html')

    return render_template('login.html')

#로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)
    print("로그아웃 성공")
    return redirect(url_for('login'))

#메인페이지 테스트
@app.route('/main')
def page2():
    return render_template('main.html')

#인적사항 데베
@app.route('/1')
def index():
    page = request.args.get('page', default=1, type=int)
    per_page = 10

    current_data, columns, total_pages = get_page_data("em_json", page, per_page)

    return render_template('dlswjr.html', data=current_data, columns=columns, page=page, total_pages=total_pages)


#채용사항 데베
@app.route('/2')
def test():
    page = request.args.get('page', default=1, type=int)
    per_page = 10

    current_data, columns, total_pages = get_page_data("today", page, per_page)

    return render_template('codyd.html', data=current_data, columns=columns, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)





