# Part B - Contact Book

def add_contact(contact, phone, name):
    """Add a new contact to the contact book."""
    contact[phone] = name
    return contact


def find_contact(contact, phone):
    """Find a contact by phone number."""
    return contact.get(phone)


def delete_contact(contact, phone):
    """Delete a contact by phone number."""
    return contact.pop(phone, None)


def list_contacts(contact):
    """List all contacts."""
    return contact


# Avoid mutable default arguments because the same object can be shared between function calls.


if __name__ == "__main__":

    contacts = {
        "9876543210": "Rahul",
        "9123456780": "Anu"
    }

    print(list_contacts(contacts))
    print(find_contact(contacts, "9876543210"))
    print(delete_contact(contacts, "9123456780"))
    print(list_contacts(contacts))


  