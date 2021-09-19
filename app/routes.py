from app.produtos import produto as produtos_blueprint
from app.auth import auth as auth_blueprint
from app.sabores import sabores as sabores_blueprint

# from app.api.api import api_bp
# from app.auth.auth import auth_bp
# from app.cart.cart import cart_bp
# from app.general.general import general_bp
# from app.products.products import products_bp
# from app.produtos.produtos import products_bp

# app.register_blueprint(api_bp, url_prefix='/api')
# app.register_blueprint(auth_bp)
# app.register_blueprint(cart_bp, url_prefix='/cart')
# app.register_blueprint(general_bp)
# app.register_blueprint(products_bp, url_prefix='/sorvetes')

    # login_manager.init_app(app)

    # from app import routes
    # routes.init_app(app)

def init_app(app):
    app.register_blueprint(produtos_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='')
    app.register_blueprint(sabores_blueprint)


