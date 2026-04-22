from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# 2. Модель User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Создаём базу данных
with app.app_context():
    db.create_all()


# 4. endpoint для перехода на страницу входа GET /login. 
# 5. endpoint для осуществления авторизации POST /login. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Пользователь с таким email не найден', 'error')
        elif not check_password_hash(user.password, password):
            flash('Неверный пароль', 'error')
        else:
            login_user(user)
            return redirect(url_for('index'))

    # Если GET или были ошибки — показываем форму снова
    return render_template('login.html')


# 3. Корневая страница endpoint для перехода на корневую страницу GET /. 
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return redirect('/login')


# 6. endpoint для перехода на страницу регистрации GET /signup.
# 7. endpoint для осуществления авторизации POST /signup.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
        else:
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация прошла успешно! Теперь войдите в систему.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')


# 8. Создать endpoint для осуществления авторизации GET /logout. 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


app.run(debug=True)