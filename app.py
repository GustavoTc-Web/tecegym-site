from flask import Flask, request, redirect, session, render_template, flash, get_flashed_messages
import mysql.connector

app = Flask(__name__)

app.secret_key = 'uma-chave-secreta-qualquer'

db_config = {
    'user': 'root',
    'password': 'mysql',
    'host': 'localhost',
    'database': 'tecegym'
}

@app.route('/')
@app.route('/index02')
def login_page():
    return render_template('index02.html')

@app.route('/cadastro')
def cadastro_form():
    return render_template('cadastro.html')

@app.route('/pagina-inicial')
def home():
    nome = session.get('user')
    return render_template('pagina-inicial.html', nome=nome)

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    print("[DEBUG] Recebi POST em /api/cadastro", request.form)

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(prepared=True)
    sql = "INSERT INTO cadastro (nome, email, senha) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nome, email, senha))
    con.commit()
    cursor.close()
    con.close()

    return redirect('/index02')

@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    print(f"Email: {email}, Senha: {senha}")

    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)
    sql = "SELECT * FROM cadastro WHERE email=%s AND senha=%s"
    cursor.execute(sql, (email, senha))
    user = cursor.fetchone()
    cursor.close()
    con.close()

    if user:
        session['user'] = user['nome']
        return redirect('/pagina-inicial')
    else:
        flash('E-mail ou senha incorretos. Tente novamente.')
        return redirect('/index02')

@app.route('/pagina-inicial')
def homepag_inicial():
    return render_template('pagina-inicial.html')

@app.route('/pagina-visitante')
def visitante():
    return render_template('pagina-visitante.html')

@app.route('/plano')
def plano_treino():
    return render_template('planos.html')

@app.route('/horarios')
def consultar_hora():
    return render_template('horario.html')

@app.route('/aulas')
def marcar_aulas():
    return render_template('aula.html')

@app.route('/dieta')
def dieta():
    return render_template('objetivo.html')

@app.route('/dieta_ganhar_massa')
def ganhar_massa():
    return render_template('dieta-ganhar.html')

@app.route('/dieta_manter_peso')
def manter():
    return render_template('dieta-manter.html')

@app.route('/dieta_emagrecer')
def pag_emagrecer():
    return render_template('dieta-emagrecer.html')

@app.route('/objetivos')
def escolher_objetivo():
    return render_template('objetivo.html')

if __name__ == '__main__':
    app.run(debug=True)
