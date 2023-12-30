from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def main():
    context = {'title': 'Главная',
    'enter': 'Вход'}
    return render_template('main_.html', **context)


@app.route('/clothes/')
def sample_cl():
    context = {'title': 'Одежда'}
    return render_template('clothes.html', **context)


@app.route('/shoes/')
def sample_sh():
    context = {'title': 'Обувь'}
    return render_template('shoes.html', **context)


@app.route('/jacket/')
def sample_jacket():
    context = {'title': 'Футболка'}
    return render_template('jacket.html', **context)



if __name__ == '__main__':
    app.run(debug=True)

