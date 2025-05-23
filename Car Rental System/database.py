users = {}
customer_records = {}

def add_user(name, email, password):
    users[email] = {
        "name": name,
        "password": password
    }

def get_user(email):
    return users.get(email)

def add_customer_record(email, record):
    if email in customer_records:
        customer_records[email].append(record)
    else:
        customer_records[email] = [record]

def get_customer_records(email):
     return customer_records.get(email)
