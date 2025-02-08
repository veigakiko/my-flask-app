from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "chave_secreta_segura"  # Used for flash messages

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kiko:ff15dHpkRtuoNgeF8eWjpqymWLleEM00@dpg-ct76kgij1k6c73b3utk0-a.oregon-postgres.render.com/beachtennis"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Fetch client names from the database
def get_clients():
    with app.app_context():
        try:
            results = db.engine.execute("SELECT nome_completo FROM public.tb_clientes;")
            return [row[0] for row in results]
        except Exception as e:
            print(f"❌ Error fetching clients: {e}")
            return []

# Fetch product names from the database
def get_products():
    with app.app_context():
        try:
            results = db.engine.execute("SELECT product FROM public.tb_products;")
            return [row[0] for row in results]
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            return []

# Fetch last 10 orders from the database
def get_last_orders():
    query = """
    SELECT "Cliente", "Produto", "Quantidade", "Data", status, id
    FROM public.tb_pedido
    ORDER BY "Data" DESC
    LIMIT 10;
    """
    with app.app_context():
        try:
            results = db.engine.execute(query)
            return results.fetchall()
        except Exception as e:
            print(f"❌ Error fetching orders: {e}")
            return []

# Insert a new order into the database
def insert_order(client, product, quantity):
    query = """
    INSERT INTO public.tb_pedido ("Cliente", "Produto", "Quantidade", "Data", status, id) 
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, 'Open', nextval('tb_pedido_id_seq'::regclass))
    """
    with app.app_context():
        try:
            db.engine.execute(query, (client, product, quantity))
            flash("Pedido registrado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao registrar pedido: {e}", "danger")

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    """ Login Page (No authentication, just redirecting to /home) """
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """ Signup Page (After signup, redirects to /) """
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/cash', methods=['GET', 'POST'])
def cash():
    """ Cash Page with Clients, Products Dropdown and Order Table """
    clients = get_clients()
    products = get_products()
    last_orders = get_last_orders()

    if request.method == 'POST':
        client = request.form.get('client')
        product = request.form.get('product')
        quantity = request.form.get('quantity')

        if not client or not product or not quantity:
            flash("Por favor, preencha todos os campos!", "warning")
        else:
            insert_order(client, product, quantity)

    return render_template('cash.html', clients=clients, products=products, last_orders=last_orders)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/loyalty')
def loyalty():
    return render_template('loyalty.html')

@app.route('/power_bi')
def power_bi():
    return render_template('power_bi.html')

if __name__ == '__main__':
    app.run(debug=True)
