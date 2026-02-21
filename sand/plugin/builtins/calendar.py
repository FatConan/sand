import calendar
from sand.plugin import SandPlugin

class Plugin(SandPlugin):
    config_options = {}
    events = {}

    def calendar_month(self, year, month):
        return calendar.Calendar().monthdatescalendar(year, month)

    def get_day_events(self, date):
        day_events = (self.events.get("%d" % date.year, {})
                      .get("%d" % date.month, {})
                      .get("%d" % date.day, []))
        return day_events

    def get_week_events(self, week_dates):
        events = []
        for date in week_dates:
            events += self.get_day_events(date)
        return events

    def configure(self, site_data, site):
        self.config_options = site_data.get("calendar", {})
        self.events = self.config_options.get("events", {})

    def add_render_context(self, page, environment, data):
        data["CALENDAR"] = self