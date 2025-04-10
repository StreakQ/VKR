from functools import wraps
from flask import session, redirect, url_for


def role_required(role):
    """
    Декоратор для проверки роли пользователя.
    :param role: Требуемая роль.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session or session.get("role") != role:
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator