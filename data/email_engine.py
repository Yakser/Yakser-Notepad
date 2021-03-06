def send_login_and_password(receiver_email, login, password):
    """
    Отправляет письмо с логином и паролем при регистрации пользователя
    """
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port = 465
    app_password = "YakserNotepad1234"
    app_email = "yaksernotepad@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ваш логин и пароль от приложения Notepad"
    message["From"] = app_email
    message["To"] = receiver_email

    styles = """
        body{
            background: #f2f3f4;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 5px;
            color: #242e42;
            border-radius: 15px;
        }
        h1 {
            text-align: center;
        }
        p{
            font-size: 24px;
        }
        .content{
            text-align: center;
        }
        .footer{
            
            text-align: center;
        }
        a {
            font-size: 24px;
            color: #365fe5;
        }
        
    """
    html = f"""
    <html lang="ru">
    <head>
        <title>Добро пожаловать в приложение Notepad!</title>
        <style>
            {styles}
        </style>
    </head>
    <body>
        <h1>
            Добро пожаловать в приложение Notepad!
        </h1>
        <div class="content">
            <p>
                Ваш логин: <strong>{login}</strong>
            </p>
            <p>
                Ваш пароль: <strong>{password}</strong>
            </p>
        </div>
        <div class="footer">
            <a href="https://yakser-notepad.herokuapp.com/login">Войти</a>
        </div>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)  # прикрепление html страницы к письму

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(app_email, app_password)  # авторизация на smtp сервере
        server.sendmail(app_email, receiver_email, message.as_string())  # отправка письма


def send_account_deleted(receiver_email, login):
    """
        Отправляет письмо, уведомляющее об удалении аккаунта
    """
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port = 465
    app_password = "YakserNotepad1234"
    app_email = "yaksernotepad@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ваш аккаунт приложения Notepad удален"
    message["From"] = app_email
    message["To"] = receiver_email

    styles = """
        body{
            background: #f2f3f4;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 5px;
            color: #242e42;
            border-radius: 15px;
        }
        h1 {
            text-align: center;
        }
        p{
            font-size: 24px;
        }
        .content{
            text-align: center;
        }
        .footer{

            text-align: center;
        }
        a {
            font-size: 24px;
            color: #365fe5;
        }

    """
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
        <head>
            <title>Аккаунт {login} приложения Notepad удален!</title>
            <style>
                {styles}
            </style>
        </head>
      <body>
        <h1>
            Аккаунт {login} приложения Notepad удален!
        </h1>
        <div class="content">
            <p>
                Аккаунт <strong>{login}</strong> удален.
            </p>
           
        </div>
        <div class="footer">
            <a href="https://yakser-notepad.herokuapp.com/register">Создать новый аккаунт</a>
        </div>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)  # прикрепление html страницы к письму

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(app_email, app_password)  # авторизация на smtp сервере
        server.sendmail(app_email, receiver_email, message.as_string())  # отправка письма


def send_password_changed(receiver_email, login, new_password):
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port = 465
    app_password = "YakserNotepad1234"
    app_email = "yaksernotepad@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Пароль от Вашего аккаунта Notepad изменен!"
    message["From"] = app_email
    message["To"] = receiver_email

    styles = """
            body{
                background: #f2f3f4;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 5px;
                color: #242e42;
                border-radius: 15px;
            }
            h1 {
                text-align: center;
            }
            p{
                font-size: 24px;
            }
            .content{
                text-align: center;
            }
            .footer{

                text-align: center;
            }
            a {
                font-size: 24px;
                color: #365fe5;
            }

        """
    html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <title>Пароль от аккаунта {login} был изменен</title>
            <style>
                {styles}
            </style>
        </head>
          <body>
            <h1>
                Пароль от аккаунта {login} был изменен
            </h1>
            <div class="content">
                <p>
                    Новый пароль: <strong>{new_password}</strong>
                </p>

            </div>
            <div class="footer">
                <a href="https://yakser-notepad.herokuapp.com/">Notepad</a>
            </div>
          </body>
        </html>
        """

    part = MIMEText(html, "html")
    message.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(app_email, app_password)  # авторизация на smtp сервере
        server.sendmail(app_email, receiver_email, message.as_string())  # отправка письма
