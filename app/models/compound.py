from app import db
from datetime import datetime

class Compound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    molecular_formula = db.Column(db.String(100), nullable=True)
    molecular_weight = db.Column(db.Float, nullable=True)
    structure_image = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    spectral_data = db.relationship('SpectralData', backref='compound', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Compound {self.name}>'

class SpectralData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compound_id = db.Column(db.Integer, db.ForeignKey('compound.id'), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # '1H NMR', '13C NMR', 'IR', 'MS', 'HPLC', etc.
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    notes = db.Column(db.Text)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SpectralData {self.data_type} for {self.compound.name}>'