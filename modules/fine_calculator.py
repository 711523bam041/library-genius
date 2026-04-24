from datetime import datetime, date
from config import FINE_RATE_PER_DAY, MAX_FINE_AMOUNT

class FineCalculator:
    @staticmethod
    def calculate_fine(due_date, return_datetime):
        # due_date may be date or string; return_datetime is datetime
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        elif isinstance(due_date, datetime):
            due_date = due_date.date()
        elif isinstance(due_date, date):
            pass
        else:
            raise ValueError("Invalid due_date type")

        if isinstance(return_datetime, str):
            return_datetime = datetime.strptime(return_datetime, "%Y-%m-%d %H:%M:%S")

        days_late = (return_datetime.date() - due_date).days
        if days_late <= 0:
            return 0.0

        fine = days_late * FINE_RATE_PER_DAY
        if fine > MAX_FINE_AMOUNT:
            fine = MAX_FINE_AMOUNT
        return float(fine)
