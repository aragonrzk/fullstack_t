"""
WTForms for PT XYZ Vehicle Inventory System
Includes CSRF protection and input validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class ProdukForm(FlaskForm):
    """Form for creating and editing products"""
    merek = StringField('Merek Produk', validators=[
        DataRequired(message='Merek produk wajib diisi'),
        Length(min=1, max=100, message='Merek harus antara 1-100 karakter')
    ])
    
    jenis = StringField('Jenis Produk', validators=[
        DataRequired(message='Jenis produk wajib diisi'),
        Length(min=1, max=100, message='Jenis harus antara 1-100 karakter')
    ])
    
    stok = IntegerField('Jumlah Stok', validators=[
        DataRequired(message='Jumlah stok wajib diisi'),
        NumberRange(min=0, message='Stok tidak boleh negatif')
    ])
    
    harga = DecimalField('Harga (Rp)', validators=[
        DataRequired(message='Harga wajib diisi'),
        NumberRange(min=0, message='Harga tidak boleh negatif')
    ])
    
    keterangan = TextAreaField('Keterangan', validators=[
        Optional(),
        Length(max=1000, message='Keterangan maksimal 1000 karakter')
    ])
    
    submit = SubmitField('Simpan')


class SearchForm(FlaskForm):
    """Form for searching products"""
    search = StringField('Cari', validators=[
        Optional(),
        Length(max=100, message='Pencarian maksimal 100 karakter')
    ])
    submit = SubmitField('Cari')
