Sandbox
===

## Authentication

- Password
Username: ganq
Password: hawkeye1

- Built-in
    * Form and Template customization
    * default LoginView, LogoutView
    * settings.
        LOGIN_REDIRECT_URL
        LOGOUT_REDIRECT_URL
        LOGIN_URL

- Register

- Profile model pattern
    - Profile model as User model's add-on (One-to-One)


## Django Class Based Views (CBVs)

- カスタマイズし過ぎに注意する
- CreateView/UpdateView (ModelFormMixin)
   自動で作成されたFormクラスが使われる（カスタマイズが不要の場合）
