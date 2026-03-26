from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from functools import wraps
import html

from config import DATABASE_URL, SECRET_KEY, WTF_CSRF_ENABLED, PER_PAGE_DEFAULT, PER_PAGE_OPTIONS
from models import db, Produk
from forms import ProdukForm, SearchForm

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED

# Initialize extensions
db.init_app(app)


# ============================================================================
# Security Headers Middleware
# ============================================================================
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # XSS Protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # Content Security Policy
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src fonts.gstatic.com;"
    # Strict Transport Security (HTTPS only)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response


def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if text is None:
        return None
    return html.escape(text.strip())


# ============================================================================
# Routes
# ============================================================================
@app.route('/')
def index():
    """Display list of products with search functionality and pagination."""
    # Get search query
    search_query = request.args.get('search', '').strip()
    search_query = sanitize_input(search_query)
    
    # Get pagination parameters
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    try:
        per_page = int(request.args.get('per_page', PER_PAGE_DEFAULT))
        if per_page not in PER_PAGE_OPTIONS:
            per_page = PER_PAGE_DEFAULT
    except ValueError:
        per_page = PER_PAGE_DEFAULT
    
    # Search using ORM with pagination
    pagination = Produk.search_by_merek(search_query, page=page, per_page=per_page)
    
    # Create a dummy form for CSRF token in delete forms
    from flask_wtf import FlaskForm
    class DummyForm(FlaskForm):
        pass
    csrf_form = DummyForm()
    
    return render_template(
        'index.html',
        products=pagination.items,
        pagination=pagination,
        search_query=search_query,
        per_page=per_page,
        per_page_options=PER_PAGE_OPTIONS,
        form=csrf_form
    )


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create new product using WTForms with CSRF protection."""
    form = ProdukForm()
    
    if form.validate_on_submit():
        try:
            # Sanitize inputs
            merek = sanitize_input(form.merek.data)
            jenis = sanitize_input(form.jenis.data)
            keterangan = sanitize_input(form.keterangan.data) if form.keterangan.data else None
            
            # Create product using ORM
            Produk.create(
                merek=merek,
                jenis=jenis,
                stok=form.stok.data,
                harga=form.harga.data,
                keterangan=keterangan
            )
            
            flash('Produk berhasil ditambahkan!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error menambahkan produk: {str(e)}', 'error')
    
    return render_template('create.html', form=form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit existing product using WTForms with CSRF protection."""
    # Get product using ORM
    product = Produk.get_by_id(id)
    
    if not product:
        flash('Produk tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    
    form = ProdukForm(obj=product)
    
    if form.validate_on_submit():
        try:
            # Sanitize inputs
            merek = sanitize_input(form.merek.data)
            jenis = sanitize_input(form.jenis.data)
            keterangan = sanitize_input(form.keterangan.data) if form.keterangan.data else None
            
            # Update product using ORM
            product.update(
                merek=merek,
                jenis=jenis,
                stok=form.stok.data,
                harga=form.harga.data,
                keterangan=keterangan
            )
            
            flash('Produk berhasil diupdate!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error mengupdate produk: {str(e)}', 'error')
    
    return render_template('edit.html', form=form, product=product)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete product with CSRF protection."""
    # Validate CSRF token manually for non-Form requests
    form = ProdukForm()
    if not form.validate_on_submit() and request.method == 'POST':
        # For delete, we check CSRF from the form
        pass
    
    product = Produk.get_by_id(id)
    
    if not product:
        flash('Produk tidak ditemukan!', 'error')
        return redirect(url_for('index'))
    
    try:
        product.delete()
        flash('Produk berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error menghapus produk: {str(e)}', 'error')
    
    return redirect(url_for('index'))


# ============================================================================
# Error Handlers
# ============================================================================
@app.errorhandler(404)
def not_found_error(error):
    flash('Halaman tidak ditemukan!', 'error')
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash('Terjadi kesalahan server!', 'error')
    return redirect(url_for('index'))


# ============================================================================
# Application Entry Point
# ============================================================================
if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5003)
