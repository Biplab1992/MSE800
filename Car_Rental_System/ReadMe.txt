Car Rental System

The Car Rental System is a python based software for fast and easy car rental operations. This software allows users to register as a admin or as a customer, login to view available cars, request rentals, gain and redeem loyalty points, process payments via a simulated eSewa module and record each records in Google Firestore. Admins can add, update, delete cars ad approve rentals, while customers can request available cars for rentals and track their loyalty points.

------- Table of Contents -------

- Features
- Prerequisites
- Installation and Configuration
- Running the System
- File Structure and Purpose
- Known Bugs and Issues
- License
- Credits


-------- Features ------------

- User Management:
	Register new users, login user, view loyalty points, view payment history and check customer records.

- Car Management:
	Admins can add, list, update and delete car records.

- Booking Management:
	Customers can request rentals and get car rates based on car selected, select renting start and end dates, choose to redeem their loyalty points 	for discount. Similarly Admins can review pending rentals requested by the customers which can be approved or rejected. The system simulates 	payment processing and updates customer loyalty points accordingly.


-------- Prerequisites --------

Before setting up the system, ensure you have the following:

- Python 3.6+ installed on your system.
- A valid Firebase project with Firebase enabled.
- The Firebase Admin SDK service account JSON file.
- Required Python packages:
	- firebase-admin


-------- Installation and Configuration ------------




