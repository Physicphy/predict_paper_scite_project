from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL_PAPER')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///paper_test.sqlite3'

    db.init_app(app)
    migrate.init_app(app, db)

    from paper_app.routes import (main_route, paper_route, predict_route)
    app.register_blueprint(main_route.bp)
    app.register_blueprint(predict_route.bp, url_prefix='/api')
    app.register_blueprint(paper_route.bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)