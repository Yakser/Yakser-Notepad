from datetime import datetime
from jinja2 import Markup


class momentjs(object):
    def __init__(self, timestamp):
        year, month, day = map(int, timestamp.split()[0].split('-'))
        hour, minute = map(int, timestamp.split()[1].split(':'))
        self.timestamp = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    def render(self, format):
        return Markup("""<script>moment.locale("ru");
                            document.write(moment(\"%s\").%s);
                        </script>"""
                      % (
                          self.timestamp.strftime("%Y-%m-%dT%H:%M:%S"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")

# momentjs
# # Created by Sergey Yaksanov at 28.02.2021
# Copyright © 2020 Yakser. All rights reserved.
