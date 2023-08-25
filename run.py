from flask import Flask, render_template, request, redirect, url_for, session
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
def get_all_data(table_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")  # Fetch columns
    columns = [column[0] for column in cursor.fetchall()]

    cursor.execute(f"SELECT * FROM {table_name}")
    all_data = cursor.fetchall()

    return all_data, columns


#로그인 화면
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
            print("로그인성공")
            return redirect(url_for('page2')) #데이터 검증 성공하면 main으로 들어가진다

    return render_template('login.html')

#로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)
    print("로그아웃 성공")  
    return redirect(url_for('login'))


#메인 화면
@app.route('/main.html')
def page2():
    return render_template('main.html')

#인적사항 데베
@app.route('/human')
def index():
    current_data, columns = get_all_data("em_json")
    return render_template('human.html', data=current_data, columns=columns)

#채용사항 데베
@app.route('/employment')
def test():
    current_data, columns = get_all_data("today")
    return render_template('employment.html', data=current_data, columns=columns)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)

