import datetime
class Entry:
    """has all the components for the question"""
    def __init__(self, dt, content):
        self.content = content
        self.dt = dt

    def get_comparison(self):
        return self.dt.timestamp()

    def get_date_time(self):
        return self.format_date + " " + self.format_time

    def format_date(self):
        return str(self.dt.month) + "." + str(self.dt.day) + "." + str(self.dt.year)

    def format_time(self):
        minute = dt.minute
        hour = dt.hour
        end = "am"

        if hour > 12:
            hour -= 12
            end = "pm"
        if hour == 0:
            hour = 12

        return str(hour) + str(minute) + " " + end

    def as_dict(self):
        return self.__dict__
