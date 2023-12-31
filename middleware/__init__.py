from middleware.auth import protected

def register_middleware(app):
    app.register_middleware(protected, "request")