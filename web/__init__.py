from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from subprocess import run
import os
import sqlite3
# from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()

def CreateApp():
    DB_USER = os.getenv("DB_USER", "rpcovington")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Heather21!")
    DB_SERVER = os.getenv("DB_SERVER", "192.168.68.156")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "Personaldb")

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "TasfafahhkhistemporaasdayUntilsetupinConfigFile12345678901"
    # === Database Config ===
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite | mysql | mssql

    if DB_TYPE == "sqlite":
        CreateTable()
        # Local SQLite file
        DB_NAME = os.getenv("DB_NAME", "X:\\Scripts\\NFCServer\\web\\warehouse.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

    elif DB_TYPE == "mysql":
        # MySQL / MariaDB
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
        )

    elif DB_TYPE == "mssql":
        # Microsoft SQL Server (requires `pyodbc`)
        DB_USER = os.getenv("DB_USER", "sa")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_SERVER = os.getenv("DB_SERVER", "localhost")
        DB_PORT = os.getenv("DB_PORT", "1433")
        DB_NAME = os.getenv("DB_NAME", "flaskdb")
        DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER},{DB_PORT}/{DB_NAME}"
            f"?driver={DRIVER.replace(' ', '+')}"
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    @app.after_request
    def add_header(response):
        response.headers.pop('X-Frame-Options', None)
        response.headers['Content-Security-Policy'] = "frame-ancestors *"
        return response

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    db.init_app(app)

    from web.views import views
    from web.auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from web.models import User

    # csrf = CSRFProtect(app)

    return app


def Install():
    """TODO: Build Out a """
    run(f"pip3 install -r C:\\Users\\rpcov\\PycharmProjects\\InventoryManagment\\requirements.txt")


def CreateTable(db_name="X:\\Scripts\\NFCServer\\web\\warehouse.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Table: General assets (machines, tools, etc.)
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS user (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             Username TEXT NOT NULL,
             FirstName TEXT,
             LastName TEXT,
             Email TEXT,
             password TEXT,
             Role TEXT DEFAULT 'Guest'
         )
         """)

    # Table: General assets (machines, tools, etc.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            asset_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            location_id INTEGER,
            status TEXT DEFAULT 'available',
            notes TEXT,
            FOREIGN KEY(location_id) REFERENCES locations(location_id)
        )
        """)

    # Table: Locations (storage shelves, bins, racks)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """)

    # Table: Wire spools
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wire_spools (
            spool_id INTEGER PRIMARY KEY AUTOINCREMENT,
            gauge TEXT NOT NULL,
            color TEXT NOT NULL,
            length REAL NOT NULL, -- in meters or feet
            material TEXT,
            location_id INTEGER,
            status TEXT DEFAULT 'in_stock',
            FOREIGN KEY(location_id) REFERENCES locations(location_id)
        )
        """)

    # Table: Harness builds
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harnesses (
            harness_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            project_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'in_progress',
            notes TEXT
        )
        """)

    # Table: Wires used in a harness (links harnesses and spools)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harness_wires (
            hw_id INTEGER PRIMARY KEY AUTOINCREMENT,
            harness_id INTEGER NOT NULL,
            spool_id INTEGER,
            length_used REAL NOT NULL,
            position_label TEXT, -- label or connector ID
            FOREIGN KEY(harness_id) REFERENCES harnesses(harness_id),
            FOREIGN KEY(spool_id) REFERENCES wire_spools(spool_id)
        )
        """)

    # Table: Transaction log (asset/wire check-in/out)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT NOT NULL, -- 'asset' or 'wire'
            item_id INTEGER NOT NULL,
            action TEXT NOT NULL, -- 'checkout', 'return', 'consume'
            quantity REAL DEFAULT 1,
            user TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created with tables.")