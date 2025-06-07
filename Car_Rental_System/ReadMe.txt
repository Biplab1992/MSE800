# Installation and Setup

** System Requirements **

- Operating system: Windows
- Python 3.6+ is installed on your system.
- A valid Firebase project with Firebase enabled.
- The Firebase Admin SDK service account JSON file. (Already included in the repository with name -"serviceAccount.Json")
- Required Python packages: firebase-admin



** Installation and Configuration **

1. Clone the Repository:
	- Open VScode and click on Clone Git Repository..
	- Paste the following code when prompted "git clone https://github.com/Biplab1992/Car_Rental_System"

2. Create a New Virtual Environment:
	- python -m venv Biplab
	- Biplab\Scripts\activate

3. Select the Biplab Interpreter:
	- Press Ctrl+Shift+P to open Command Palette
	- Select " Python(version name)('Biplab':venv)

4. Install the Firebase Admin SDK: pip install firebase-admin




** Running the System **

To start the Car Rental System, simply run: python main.py

This will display the main menu with option as follows:

1. Register User: New user can create an account by providing their name, email id, password and role.

2. Login: Admins and customers have different menus where Admins can access the features like Add, 	update, delete cars, approve rental requests, list cars while customers can see available cars 	and request for rentals, view their loyalty points.

3. Exit: Choose to close the application.




-------- File Structure and Purpose----------

- main.py
	This is the software gateway. It displays the initial menu and routes the users to appropriate sub menu based on their roles.

- database.py
	This file contains all functions for interacting with Google Firestore, including connections to collections for users, cars, rentals and payments.

- user_manager.py
	Implements the UserManager class, which handles user registration, login, viewing loyalty points, and retrieving payment and rental histories from the database.

- car_manager.py
	Implements the CarManager class responsible for adding, listing, updating, and deleting car records in the database.

- booking_manager.py
	Implements the BookingManager class, which manages the rental process—displaying available cars, handling rental requests (including date validation and loyalty point redemption), simulating payment via the payment_gateway, and saving rental records.

- payment_gateway.py
	Contains the simulated payment processing functionality which prompts the user for confirmation for payment via eSewa.




---------- Bugs and Issues -------------

- Simulated Payment Process:
The payment gateway simulation does not integrate with a real payment API. It relies on user input (yes/no) to simulate payment success.
	
- Multiple booking of cars in same dates:
This system doesn't check for the cars that are already booked for specified dates, but keeps on accepting new bookings.

Please report any issues or bugs via tha GitHub issues page on this repository.



----------- License ---------

MIT License

Copyright (c) 2025 Biplab1992

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



------ Credits ------------

Developer:
Biplab Neupane
(Auckland, New Zealand)
neubiplab@gmail.com

Feel free to contact me for any questions, support or further development inquiries.

