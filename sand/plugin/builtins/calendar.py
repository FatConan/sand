import calendar
from datetime import date

from sand.plugin import SandPlugin

from typing import List


class Plugin(SandPlugin):
    config_options = {}
    events = {}

    @staticmethod
    def calendar_month(year:int, month:int):
        return calendar.Calendar().monthdatescalendar(year, month)

    def get_day_events(self, date:date):
        day_events = (self.events.get("%d" % date.year, {})
                      .get("%d" % date.month, {})
                      .get("%d" % date.day, []))
        return day_events

    def get_week_events(self, week_dates:List[date]):
        events = []
        for d in week_dates:
            events += self.get_day_events(d)
        return events

    def configure(self, site_data, site):
        self.config_options = site_data.get("calendar", {})
        self.events = self.config_options.get("events", {})

    def add_render_context(self, page, environment, data):
        data["CALENDAR"] = self