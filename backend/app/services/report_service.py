from app.models import Trek, Booking, User
from app.constants.roles import UserRole
from datetime import datetime

import os

class ReportService:

    @staticmethod
    def generate_monthly_report():

        total_treks = Trek.query.count()

        total_bookings = Booking.query.count()

        total_users = User.query.filter_by(
            role=UserRole.TREKKER.value
        ).count()

        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
        <html>
        <body>

        <h2>Monthly Trekking Report</h2>
        <p><small>Generated on: {generated_time}</small></p>

        <table border="1" cellpadding="8">

            <tr>
                <th>Total Treks</th>
                <td>{total_treks}</td>
            </tr>

            <tr>
                <th>Total Users</th>
                <td>{total_users}</td>
            </tr>

            <tr>
                <th>Total Bookings</th>
                <td>{total_bookings}</td>
            </tr>

        </table>

        </body>
        </html>
        """

        os.makedirs("reports", exist_ok=True)

        filename = "reports/monthly_report.html"

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(html)

        return filename