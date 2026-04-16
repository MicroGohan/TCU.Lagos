from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.models.user import Usuario
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.get_by_id(user_id)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def rol_requerido(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or g.user.rol not in roles:
                flash('No tienes permiso para acceder a esta página.', 'error')
                return redirect(url_for('estudiantes.index'))
            return view(**kwargs)
        return wrapped_view
    return decorator

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.get_by_username(username)
        error = None

        if user is None:
            error = 'Usuario incorrecto.'
        elif not user.check_password(password):
            error = 'Contraseña incorrecta.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('estudiantes.index'))

        flash(error, 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/setup')
def setup_defaults():
    Usuario.ensure_default_admin()
    flash('Usuarios por defecto (admin, director, profesor) configurados.', 'success')
    return redirect(url_for('auth.login'))
