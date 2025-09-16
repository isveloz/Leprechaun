import datetime


class Scheduler:
    def __init__(self, schedule_config):
        self.schedule_config = schedule_config

    def is_scheduled_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")
        current_date = now.day

        for schedule in self.schedule_config.get("schedule", []):
            if not schedule.get("enabled", False):
                continue

            if current_time == schedule.get("time") and (
                current_day in schedule.get("days", []) or str(current_date) in schedule.get("days", [])
            ):
                return True

        return False

