from app import create_app, db
from app.models import Compound, SpectralData, Project

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug=True)