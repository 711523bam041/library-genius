from datetime import datetime, timedelta
from modules.database import DatabaseConnection
from modules.student_manager import StudentManager
from modules.book_manager import BookManager
from modules.fine_calculator import FineCalculator


class TransactionManager:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
        self.student_mgr = StudentManager()
        self.book_mgr = BookManager()
        self.fine_calc = FineCalculator()

    def borrow_book(self, student_id: str, book_id: int):
        # 1) validate student
        student = self.student_mgr.get_student(student_id)
        if not student:
            return False, "Student not found"

        # 2) validate book by ID
        book = self.book_mgr.get_book_by_id(book_id)
        if not book:
            return False, "Book not found"

        # 3) student eligibility (borrow_limit vs current_outstanding)
        ok, msg = self.student_mgr.check_eligibility(student_id)
        if not ok:
            return False, msg

        # 4) book availability (available_copies > 0)
        ok, msg = self.book_mgr.check_availability(book_id)
        if not ok:
            return False, msg

        # 5) create transaction row
        borrow_date = datetime.now()
        due_date = (borrow_date + timedelta(days=21)).date()

        q = (
            "INSERT INTO transactions "
            "(student_id, book_id, borrow_date, due_date, status) "
            "VALUES (%s, %s, %s, %s, 'Active')"
        )
        if (
            self.db.execute_update(
                q, (student_id, book_id, borrow_date, due_date)
            )
            == 0
        ):
            return False, "Failed to create transaction"

        # 6) update book copies
        if not self.book_mgr.update_available_copies(book_id, borrow=True):
            return False, "Failed to update book copies"

        # 7) update student's outstanding count
        if not self.student_mgr.update_outstanding(student_id, increment=True):
            return False, "Failed to update student outstanding"

        return True, f"Borrowed successfully, due date {due_date}"

    def return_book(self, student_id: str, book_id: int, condition: str = "Good"):
        # 1) find active transaction
        rows = self.db.execute_query(
            "SELECT * FROM transactions "
            "WHERE student_id = %s AND book_id = %s AND status = 'Active'",
            (student_id, book_id),
        )
        if not rows:
            return False, "No active borrow transaction found"

        tx = rows[0]

        # 2) calculate fine
        return_dt = datetime.now()
        fine = self.fine_calc.calculate_fine(tx["due_date"], return_dt)

        # 3) close transaction
        q = (
            "UPDATE transactions "
            "SET return_date = %s, fine_amount = %s, "
            "book_condition_on_return = %s, status = 'Returned' "
            "WHERE transaction_id = %s"
        )
        if (
            self.db.execute_update(
                q, (return_dt, fine, condition, tx["transaction_id"])
            )
            == 0
        ):
            return False, "Failed to update transaction"

        # 4) update book copies
        if not self.book_mgr.update_available_copies(book_id, borrow=False):
            return False, "Failed to update book copies"

        # 5) update student's outstanding count
        if not self.student_mgr.update_outstanding(student_id, increment=False):
            return False, "Failed to update student outstanding"

        return True, f"Returned successfully, fine = {fine}"

    def get_student_borrowed_books(self, student_id: str):
        q = (
            "SELECT t.transaction_id, t.book_id, b.title, b.author, "
            "t.borrow_date, t.due_date, t.status, t.fine_amount "
            "FROM transactions t "
            "JOIN books b ON t.book_id = b.book_id "
            "WHERE t.student_id = %s AND t.status = 'Active'"
        )
        return self.db.execute_query(q, (student_id,))
