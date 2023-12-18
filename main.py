import sqlite3

from flask import Flask, render_template, g, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

REGIONS = {
    1: "Шевченківський",
    2: "Залізничний",
    3: "Сихівський",
    4: "Галицький",
    5: "Франківський",
    6: 'Личаківський',
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database0.db')
    return db

def create_db():
    cr = sqlite3.connect('database0.db')
    cr.execute("""
        CREATE TABLE IF NOT EXISTS users
            (your_name VARCHAR(128), region INT, order_name VARCHAR(128), phone VARCHAR(32)) 
    """)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

workers_list = [
    {"name": "John", "work": 'сhief'},
    {"name": "George", "work": 'cook'},
    {"name": "Mark", "work": 'cook'},
    {"name": "Leo", "work": 'waiter'},
]

menu_list = [
    {'name': 'Margherita', 'ingredients': 'tomato sauce, mozzarella, basil.', 'price': '3.5$'},
    {'name': '4 cheeses', 'ingredients': 'parmesan, emmental, ricotta, gorgonzola.', 'price': '4$'},
    {'name': '4 seasons', 'ingredients': 'tomato sauce, salami, ham, arugula, tomato, feta, cherry, mozzarella, oregano.', 'price': '6$'},
    {'name': '4 meats', 'ingredients': 'tomato sauce, bacon, marinated chicken, ham, fresh tomatoes, mozzarella ', 'price': '4$'},
    {'name': 'Vegetarian with tofu', 'ingredients': 'tomato sauce, tofu cheese, mushrooms, tomatoes, corn, onions, olives, herbs', 'price': '5$'},
]


@app.route('/')
@app.route('/home')
def first_page():
    return render_template("index.html", title='Home page')

@app.route('/menu')
def menu():
    menu_info = {
        "title": "Меню",
        "block_title": "Menu",
        "menu": menu_list
    }
    return render_template("menu.html", **menu_info)

@app.route('/images')
def photos():
    images_info = {
        'block_title': "Images"
    }
    return render_template("images.html", **images_info)

@app.route('/about')
def info():
    worker_info = {
        "title": "Інформація",
        "block_title": "Workers",
        "workers": workers_list
    }
    return render_template("info.html", **worker_info)

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == "POST":
        name = request.form.get("name")
        region = request.form.get("region")
        phone = request.form.get("phone")
        order = request.form.get("order")
        cr = get_db()
        cr.execute("""
            INSERT INTO users (your_name, region, order_name, phone) VALUES (?,?,?,?)
        """, (name, region, order, phone))
        cr.commit()
        return render_template("index.html")

    else:
        return render_template("register.html", cities=REGIONS)

@app.route('/users')
def participants():
    cr = get_db().cursor()
    cr.execute("SELECT * FROM users")
    data = cr.fetchall()
    return render_template("users.html", users=data, cities=REGIONS)



if __name__ == "__main__":
    create_db()
    app.run(debug=True)