                                                                                                                                                                                                                                                                                                                                                                                                                                                     clinic_management.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                        import sqlite3
import uuid
from datetime import datetime

# Function to create the database and table if it doesn't exist
def create_database():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # Create table with the necessary columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            appointment_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            pincode TEXT NOT NULL,
            payment_mode TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'Booked'
        )
    """)
    conn.commit()
    conn.close()

# Option 1: Book a new appointment
def book_new_appointment():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    print("\nEnter patient details:")
    name = input("Enter name: ")
    address = input("Enter address: ")
    pincode = input("Enter pincode: ")
    payment_mode = input("Enter payment mode (e.g., Cash, Card): ")
    time_slot = input("Enter time slot: ")
    amount = float(input("Enter amount for the appointment in ₹: "))

    # Generate unique appointment number
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    appointment_number = f"HOSP-{date_str}-{uuid.uuid4().hex[:4].upper()}"

    # Insert appointment details into the database
    try:
        cursor.execute("""
            INSERT INTO patients (appointment_number, name, address, pincode, payment_mode, time_slot, amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (appointment_number, name, address, pincode, payment_mode, time_slot, amount))
        conn.commit()
        print(f"\nAppointment booked successfully.\n")
        print(f"Receipt:\n")
        print(f"Pragyan Clinic\nName: {name}\nAmount: ₹{amount:.2f}\nTime: {time_slot}\nAppointment No: {appointment_number}")
        print("\nThanks for choosing Pragyan Clinic.\n")
    except sqlite3.Error as e:
        print(f"Error booking appointment: {e}")
    finally:
        conn.close()

# Option 2: View all appointments
def view_all_appointments():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    if patients:
        print("\nList of all appointments:")
        for patient in patients:
            status = patient[7]  # Status field
            print(f"Appointment #{patient[0]}: {patient[1]} at {patient[5]}, Amount: ₹{patient[6]:.2f}, Status: {status}")
    else:
        print("\nNo appointments found.")
    conn.close()

# Option 3: Cancel an appointment
def cancel_appointment():
    appointment_number = input("\nEnter appointment number to cancel: ")
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE appointment_number = ?", (appointment_number,))
    patient = cursor.fetchone()

    if patient:
        cursor.execute("UPDATE patients SET status = 'Cancelled' WHERE appointment_number = ?", (appointment_number,))
        conn.commit()
        print(f"\nAppointment #{appointment_number} has been cancelled.")
    else:
        print("\nNo patient found with that appointment number.")
    conn.close()

# Option 4: Reschedule an appointment
def reschedule_appointment():
    appointment_number = input("\nEnter appointment number to reschedule: ")
    new_time_slot = input("Enter new time slot: ")

    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE appointment_number = ?", (appointment_number,))
    patient = cursor.fetchone()

    if patient:
        cursor.execute("UPDATE patients SET time_slot = ?, status = 'Rescheduled' WHERE appointment_number = ?",
                       (new_time_slot, appointment_number))
        conn.commit()
        print(f"\nAppointment #{appointment_number} has been rescheduled to {new_time_slot}.")
    else:
        print("\nNo patient found with that appointment number.")
    conn.close()

# Option 5: View available seats
def view_available_seats():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM patients WHERE status = 'Booked' OR status = 'Rescheduled'")
    booked_count = cursor.fetchone()[0]
    total_seats = 50  # For example, assuming clinic has 50 seats
    available_seats = total_seats - booked_count

    print(f"\nAvailable seats: {available_seats}/{total_seats}")
    conn.close()

# Option 6: Search patient by appointment number
def search_patient_by_appointment_number():
    appointment_number = input("\nEnter appointment number to search: ")
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE appointment_number = ?", (appointment_number,))
    patient = cursor.fetchone()

    if patient:
        print(f"\nAppointment #{patient[0]}: {patient[1]} at {patient[5]}, Amount: ₹{patient[6]:.2f}, Status: {patient[7]}")
    else:
        print("\nNo patient found with that appointment number.")
    conn.close()

# Main menu function
def main():
    create_database()  # Ensure the database is created before starting the menu
    while True:
        print("\n1. Book New Appointment")
        print("2. View All Appointments")
        print("3. Cancel Appointment")
        print("4. Reschedule Appointment")
        print("5. View Available Seats")
        print("6. Search Patient by Appointment Number")
        print("7. Exit")

        choice = input("\nEnter choice: ")

        if choice == '1':
            book_new_appointment()
        elif choice == '2':
            view_all_appointments()
        elif choice == '3':
            cancel_appointment()
        elif choice == '4':
            reschedule_appointment()
        elif choice == '5':
            view_available_seats()
        elif choice == '6':
            search_patient_by_appointment_number()
        elif choice == '7':
            print("\nExiting the system.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()


