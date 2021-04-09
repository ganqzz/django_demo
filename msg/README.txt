# Authentication

- Built-in
    * django.contrib.auth.urls
    * override default Auth templates => registration/*.html
    * scratch LoginView, LogoutView (eventually not in use)
    * SignUpView
    * default LoginView, LogoutView
    * settings.
        LOGIN_REDIRECT_URL
        LOGOUT_REDIRECT_URL
        LOGIN_URL

- Custom User Model
    - using email field as identification instead of username field
    - UserManager(BaseUserManager)
    - PermissionsMixin
    - settings.AUTH_USER_MODEL
    - get_user_model()

- Authorization
    - PermissionRequiredMixin


# Packages
- Markdown


# minor tips
- Community名にascii以外を使用するとslugが""になる: ``slugify(text, allow_unicode=True)``
- Django3対応: ``{% load static %}``


# test account

ganq@hoge.com
hawkeye1
