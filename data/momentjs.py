from datetime import datetime
from jinja2 import Markup


class momentjs(object):
    """ Осуществляет работу с библиотекой MomentJs"""

    def __init__(self, timestamp):
        """
        Приведение даты к объекту datetime
        """
        year, month, day = map(int, timestamp.split()[0].split('-'))
        hour, minute = map(int, timestamp.split()[1].split(':'))
        self.timestamp = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    def render(self, format):
        """Добавляет в html код страницы отформатированную дату и время"""
        return Markup("""<script>moment.locale("ru");
                            document.write(moment(\"%s\").%s);
                        </script>"""
                      % (
                          self.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), format))

    def format(self, fmt):
        """Форматирует дату с помощью js-функции библиотеки MomentJs  - format(fmt)"""
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        """Форматирует дату с помощью js-функции библиотеки MomentJs  - calendar()"""
        return self.render("calendar()")

    def fromNow(self):
        """Форматирует дату с помощью js-функции библиотеки MomentJs  - fromNow()"""
        return self.render("fromNow()")
