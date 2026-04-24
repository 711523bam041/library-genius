from modules.database import DatabaseConnection

class StudentManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()

    def get_student(self, student_id: str):
        rows = self.db.execute_query(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )
        return rows[0] if rows else None

    def search_student_by_name(self, name: str):
        return self.db.execute_query(
            "SELECT * FROM students WHERE student_name LIKE %s",
            (f"%{name}%",)
        )

    def check_eligibility(self, student_id: str):
        student = self.get_student(student_id)
        if not student:
            return False, "Student not found"

        if student["current_outstanding"] >= student["borrow_limit"]:
            return False, "Borrow limit reached"

        if student["total_fines_paid"] > 200:
            return False, "Pending fines too high"

        return True, "Eligible"

    def update_outstanding(self, student_id: str, increment: bool = True):
        delta = 1 if increment else -1
        return self.db.execute_update(
            "UPDATE students SET current_outstanding = current_outstanding + %s "
            "WHERE student_id = %s",
            (delta, student_id)
        ) > 0
