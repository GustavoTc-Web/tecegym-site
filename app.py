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
        session['user_id'] = user['id']
        session['user'] = user['nome']
        return redirect('/pagina-inicial')
    else:
        flash('E-mail ou senha incorretos. Tente novamente.')
        return redirect('/index02')



@app.route('/evolução', methods=['POST', 'GET'])
def evolucao():
    if 'user_id' not in session:
        return redirect('/index02')
    
    if request.method == 'POST':

        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        gordura = float(request.form['gordura'])
        data_registro = request.form['data_registro']
        id_user = session['user_id']

        con = mysql.connector.connect(**db_config)
        cursor = con.cursor()
        sql = """
            INSERT INTO evolucao (id_usuario, peso, altura, gordura_corporal, data_registro)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (id_user, peso, altura, gordura, data_registro))
        con.commit()
        cursor.close()
        con.close()

        return redirect('/evolução')

    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM evolucao WHERE id_usuario = %s", (session['user_id'],))
    evolucao_data = cursor.fetchall()
    cursor.close()
    con.close()

    return render_template('evolução.html', evolucao=evolucao_data)
    


@app.route('/perfil')
def perfil():
    if 'user_id' not in session:
        return redirect('/index02')
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cadastro WHERE id = %s", (session['user_id'],))
    user_data = cursor.fetchone()
    cursor.execute("""
        SELECT * FROM evolucao 
        WHERE id_usuario = %s 
        ORDER BY data_registro DESC 
        LIMIT 1
    """, (session['user_id'],))
    ultima_evolucao = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template('perfil.html', user=user_data, evolucao=ultima_evolucao)



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

@app.route('/personal')
def personal():
    return render_template('personal.html')

@app.route('/evolução')
def historico_evolução():
    return render_template('evolução.html')

@app.route('/planlimit')
def plano_limitado():
    return render_template('planlimit.html')

if __name__ == '__main__':
    app.run(debug=True)
