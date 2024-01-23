from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'c928ba4f26979fe137232ae1a30cff74a2602ddeaf28ca226969724afacc5686'
csrf =CSRFProtect(app)
bootstrap = Bootstrap5(app)


@app.cli.command('init-db')
def init_db():
     db.create_all()
     print('ok')


@app.route('/')
def index():
    context = {'title':'Welcom to MySite'}
    return render_template('base.html', **context)


@app.route('/reg/', methods=['GET','POST'])
def reg_user():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        user = db.session.query(User).filter(User.user_email == form.email.data).first()
        if user:
                if user.user_login == form.username.data and user.check_password(form.password.data):
                    flash('Вы успешно прошли авторизацию', 'success')
                    return redirect(url_for('index'))
                flash('Неверное имя пользователя или пароль', 'danger')
                return render_template('register.html', form=form)

        else:    
            newuser = User(user_login = form.username.data, user_email = form.email.data)
            newuser.set_password(form.password.data)
            db.session.add(newuser)
            db.session.commit()
            flash('Регистрация прошла успешно', 'success')
    
    return render_template('register.html', form=form)




if __name__ == '__main__':
    with app.app_context():     
        db.create_all()
    app.run(debug=True)
