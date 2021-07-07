# Django basics and REST API

## Django basics

- Forms
    * Step (Abstract Inheritance): Text, Quiz
        Stepはテーブルを持たない
    * Question (Multi-Table Inheritance): TrueFalseQuestion, MultipleChoiceQuestion
        Questionはテーブルを持つ。内部的にはForeign keyで参照
- ORM
- Templates
    - basics
    - filters and tags
    - inheritance
    - templatetags
- Admin customize
- Unit test
- No Login and Sign up
    * login from admin interface
- Packages
    - Markdown
    - django-debug-toolbar
- JavaScript/CSS libraries
    - jquery.formset.js
    - marked.js


## Libraries

- Django REST Framework
- Markdown
- marked.js


## Django REST Framework

- TokenAuthentication
```
>>> from rest_framework.authtoken.models import Token
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='ganq')
>>> Token.objects.create(user=user)
<Token: 116828e883d542de79ce8c7d93ef7c3f0abf8b92>
```
or
```
python manage.py drf_create_token <user>
```


## User情報

Username: ganq
Password: hawkeye1

Username: hoge
Password: testhoge
