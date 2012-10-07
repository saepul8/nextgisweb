from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
)

from .component import Component, load_all

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    load_all()
    config = Configurator(settings=settings)

    secret = settings.get('auth.secret')
    assert secret, "auth.secret not set"

    authn_policy = AuthTktAuthenticationPolicy(secret=secret)
    config.set_authentication_policy(authn_policy)

    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_tm')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    for impl in Component.registry:
        if hasattr(impl, 'setup_routes'):
            impl.setup_routes(config)

    config.scan()
    return config.make_wsgi_app()

