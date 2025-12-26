Technologies Used
Python: The core programming language.

Streamlit: Used to create the web interface and handle user inputs.

SQLAlchemy & SQLite: Manages the local database to store reported issues permanently.

SMTPlib: A built-in Python library used to send emails via Gmail.


How the Email Trigger Works
The email notification system is automated to confirm successful submissions. Here is the flow:

User Submission: When a user clicks the "Submit Issue" button, the system first validates that all required fields are filled.

Database Entry: The system generates a unique Reference ID (e.g., ISS-2025-48291) and saves the issue details and photo path to the database.

Immediate Trigger: Once the data is successfully saved, the code triggers the send_email function.

Authentication & Sending: This function connects securely to the Gmail SMTP server using a dedicated App Password and sends a confirmation email containing the Reference ID to the user.
