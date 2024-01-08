from flask import Flask, redirect, render_template, url_for, request, make_response, abort


app = Flask(__name__)


user = {'user':'Natalya',
'mail': 'natalya@mail.ru'}

@app.route('/welcome/<username>/')
def salute(username):
    return render_template('hello.html',username=username)



@app.route('/', methods=['GET', 'POST'])
def authorization():
    if request.method=='POST':
        username = request.form.get('name')
        mail_user = request.form.get('mail')
        if username == user['user'] and mail_user == user['mail']:
            response = make_response(redirect(url_for('salute', username=username)))
            response.set_cookie('username', user['user'])
            return response
        else:
            return f'Ошибка! Попробуйте снова'
    else:
        response = make_response(render_template('index.html'))
        response.set_cookie('username', user['user'], max_age=0)
        return response
  


if __name__=='__main__':
    app.run(debug=True)