import database

def process_payment(customer_email, amount):
    """
    Simulates payment via eSewa by prompting the user for confirmation.
    If the user replies 'yes', the payment is marked successful.
    If 'no', the rental request is canceled.
    """
    response = input(f"\nThe total rental cost is ${amount}. Do you want to proceed with payment via eSewa? (yes/no): ").strip().lower()
    
    if response == "yes":
        print(f"Payment Successful! ${amount} charged to {customer_email}.")
        record_payment(customer_email, amount)
        return True
    else:
        print("Payment Unsuccessful. Rental request cannot proceed.")
        return False

def record_payment(customer_email, amount):
    """
    Stores payment confirmation in Firestore.
    """
    payment_data = {
        "customer_email": customer_email,
        "amount": amount,
        "status": "Completed"
    }
    
    db_ref = database.get_payments_collection()
    db_ref.document(customer_email).set(payment_data)
    print(f"Payment record saved for {customer_email}.")