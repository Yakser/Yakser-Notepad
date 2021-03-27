def send_login_and_password(receiver_email, login, password):
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    port = 465  # для SSL подключения
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
    <html>
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
      <style>
        {styles}
      </style>
    </html>
    """

    # Сделать их текстовыми\html объектами MIMEText
    # part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Внести HTML\текстовые части сообщения MIMEMultipart
    # Почтовый клиент сначала попытается отрендерить последнюю часть
    # message.attach(part1)
    message.attach(part2)

    # Создание безопасного контекста SSL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(app_email, app_password)
        server.sendmail(app_email, receiver_email, message.as_string())

# send_login_and_password('sergeyyaksanov@yandex.ru', 'login', 'password')
# # email_engine
# # # Created by Sergey Yaksanov at 27.03.2021
# # Copyright © 2020 Yakser. All rights reserved.
