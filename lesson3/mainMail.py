import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
server.login(login, password)

email_from = "k3yari@yandex.kz"
email_to = "k3yari@yandex.kz"
website_url = "https://dvmn.org/profession-ref-program/k.potato4ever/1DvOx/"
friend_name = "друг"
my_name = "Arai"
email_text = """\
{}

Привет, %friend_name%! %my_name% приглашает тебя на сайт %website%!

%website% — это новая версия онлайн-курса по программированию. 
Изучаем Python и не только. Решаем задачи. Получаем ревью от преподавателя. 

Как будет проходить ваше обучение на %website%? 

→ Попрактикуешься на реальных кейсах. 
Задачи от тимлидов со стажем от 10 лет в программировании.
→ Будешь учиться без стресса и бессонных ночей. 
Задачи не «сгорят» и не уйдут к другому. Занимайся в удобное время и ровно столько, сколько можешь.
→ Подготовишь крепкое резюме.
Все проекты — они же решение наших задачек — можно разместить на твоём GitHub. Работодатели такое оценят. 

Регистрируйся → %website%  
На курсы, которые еще не вышли, можно подписаться и получить уведомление о релизе сразу на имейл."""
letter = """\
From: {0}
To: {1}
Subject: Приглашение!
Content-Type: text/plain; charset="UTF-8";""".format(email_from, email_to)
message = email_text.replace("%website%", website_url) \
                    .replace("%friend_name%", friend_name) \
                    .replace("%my_name%", my_name) \
                    .format(letter) \
                    .encode("UTF-8")

server.sendmail(email_from, email_to, message)
server.quit()