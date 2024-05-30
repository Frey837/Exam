from flask import Flask, render_template, request, redirect, url_for
import requests
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'

table=[
    ['Pudgik',1.25,5,'',''],
    ['Venik',1.69,9,'',''],
    ['Bik',1.72,12,'',''],
    ['Bebul',1.86,17,'',''],
    ['Kunka',2.20,1,'','']
]


Games=[
    ['Nil','Debil',randint(6, 10),randint(6, 10),0],
    ['Pisa','Popa',randint(6, 10),randint(6, 10),0],
    ['Cica','Kaka',randint(6, 10),randint(6, 10),0],
    ['Artem','Sigma',randint(6, 10),randint(6, 10),0],
    ['Yana','Cist',randint(6, 10),randint(6, 10),0]
]



def bez_PVN(tabula):
    for row in tabula:
        row[-2] = round((row[-3]*row[-4]), 2)
    return tabula

def ar_PVN(tabula):
    for row in tabula:
        row[-1] = round((row[-3]*row[-4]) * 1.21, 2)
    return tabula

def average(tabula):
    for row in tabula:
        if len(row) == 4:
            row.append((row[-1]+row[-2])/2)
        else:
            row[-1] = (row[-2]+row[-3])/2
    return tabula


@app.route('/', methods=['GET', 'POST'])
def index():
    url_users = 'https://jsonplaceholder.typicode.com/users'
    response_users = requests.get(url_users)
    users = response_users.json() if response_users.status_code == 200 else []
    return render_template('index.html', users=users)

@app.route('/user/<int:user_id>')
def user_posts(user_id):
    # Iegūstam konkrēta lietotāja publikācijas
    url_posts = f'https://jsonplaceholder.typicode.com/posts?userId={user_id}'
    response_posts = requests.get(url_posts)
    posts = response_posts.json() if response_posts.status_code == 200 else []
    return render_template('user_posts.html', posts=posts, user_id=user_id)

@app.route('/view1/<variable>')
def view1(variable):
    return render_template('view1.html', variable=variable)

@app.route('/view2/<variable>')
def view2(variable):
    return render_template('view2.html', variable=variable)

@app.route('/view3')
def view3():
    bez_PVN(table)
    ar_PVN(table)
    return render_template('view3.html', tabula=table)

@app.route('/view4')
def view4():
    average(Games)
    MAX=max(Games, key=lambda x: x[4])
    MIN=min(Games, key=lambda x: x[4])
    return render_template('view4.html', tabula=Games,max = MAX,min = MIN)

@app.route('/view5')
def view5():
    return render_template('view5.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        OK = False
        while OK != True:
            if ('@' in email) and ('.com' in email) or ('.lv' in email):
                if (len(password)>=8):
                    return render_template('congratulations.html')
                return render_template('error_password.html')
            return render_template('error_email.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
