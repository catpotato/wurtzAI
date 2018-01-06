class Entry:
    """has all the components for the question"""
    def __init__(self, date, time, content):
        self.content = contents
        self.date = date
        self.time = time

    def get_date_time(self):
        return self.format_date + " " + self.format_time

    def format_date(self):
        return str(self.date.month) + "." + str(self.date.day) + "." + str(self.date.year)

    def format_time(self):
        minute = time.minute
        hour = time.hour
        end = "am"

        if hour > 12:
            hour -= 12
            end = "pm"
        if hour == 0:
            hour = 12

        return str(hour) + str(minute) + " " + end
