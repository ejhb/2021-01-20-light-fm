"""Initialize Flask app."""
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        from application import routes

        from application.plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)
        from application.plotlydash.dashboard2 import create_dashboard
        app = create_dashboard(app)
        
        if app.config['FLASK_ENV'] == 'development':
            from application.assets import compile_assets
            compile_assets(app)

        return app

