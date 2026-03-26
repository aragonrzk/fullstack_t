"""
Database Models for PT XYZ Vehicle Inventory System
Using SQLAlchemy ORM for security and ease of use
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Produk(db.Model):
    """Model for fs_produk table - Vehicle Products"""
    __tablename__ = 'fs_produk'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merek = db.Column(db.String(100), nullable=False, index=True)
    jenis = db.Column(db.String(100), nullable=False)
    stok = db.Column(db.Integer, nullable=False, default=0)
    harga = db.Column(db.Numeric(15, 2), nullable=False)
    keterangan = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Produk {self.id}: {self.merek} {self.jenis}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'merek': self.merek,
            'jenis': self.jenis,
            'stok': self.stok,
            'harga': float(self.harga),
            'keterangan': self.keterangan,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def search_by_merek(cls, keyword, page=1, per_page=10):
        """Search products by merek with pagination (case-insensitive)"""
        if keyword:
            pagination = cls.query.filter(
                cls.merek.ilike(f'%{keyword}%')
            ).order_by(cls.id.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
        else:
            pagination = cls.query.order_by(cls.id.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
        return pagination
    
    @classmethod
    def get_by_id(cls, product_id):
        """Get product by ID"""
        return cls.query.get(product_id)
    
    @classmethod
    def create(cls, merek, jenis, stok, harga, keterangan=None):
        """Create new product"""
        produk = cls(
            merek=merek,
            jenis=jenis,
            stok=stok,
            harga=harga,
            keterangan=keterangan
        )
        db.session.add(produk)
        db.session.commit()
        return produk
    
    def update(self, merek=None, jenis=None, stok=None, harga=None, keterangan=None):
        """Update product details"""
        if merek is not None:
            self.merek = merek
        if jenis is not None:
            self.jenis = jenis
        if stok is not None:
            self.stok = stok
        if harga is not None:
            self.harga = harga
        if keterangan is not None:
            self.keterangan = keterangan
        db.session.commit()
        return self
    
    def delete(self):
        """Delete product"""
        db.session.delete(self)
        db.session.commit()
