import json

# Define global variables for data files
BOOKS_FILE = "Books.dat"
BORROWS_FILE = "Borrows.dat"
RESERVATIONS_FILE = "Reservations.dat"
MEMBERS_FILE = "Members.dat"

# Initialize data files with empty lists if they don't exist
for file in [BOOKS_FILE, BORROWS_FILE, RESERVATIONS_FILE, MEMBERS_FILE]:
    try:
        with open(file, "r") as f:
            pass
    except FileNotFoundError:
        with open(file, "w") as f:
            json.dump([], f)


# Function to read data from a file
def read_data(file_name):
    with open(file_name, "r") as file:
        data = json.load(file)
    return data


# Function to write data to a file
def write_data(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file)


# Function to list all books
def list_all_books():
    books = read_data(BOOKS_FILE)
    if books:
        print("All Books:")
        print("{:<5} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Available"))
        for book in books:
            available_status = "Yes" if book["available"] else "No"
            print("{:<5} {:<30} {:<20} {:<10}".format(book["id"], book["title"], book["author"], available_status))
    else:
        print("No books found.")


# Function to search for books
def search_books(keyword):
    books = read_data(BOOKS_FILE)
    found_books = [book for book in books if keyword.lower() in book["title"].lower()]
    if found_books:
        print("Found Books:")
        for book in found_books:
            print_book_info(book)
    else:
        print("No books found.")


# Function to display list of available books
def display_available_books():
    books = read_data(BOOKS_FILE)
    available_books = [book for book in books if book["available"]]
    if available_books:
        print("Available Books:")
        for book in available_books:
            print_book_info(book)
    else:
        print("No books available.")


# Function to print book information
def print_book_info(book):
    print(f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, Available: {book['available']}")


# Function to borrow or make a reservation for a book
def borrow_or_reserve_book(book_id, member_id):
    books = read_data(BOOKS_FILE)
    # Check if the book or member exists
    if not any(book["id"] == book_id for book in books):
        print("Book not found.")
        return False
    if not any(member["id"] == member_id for member in read_data(MEMBERS_FILE)):
        print("Member not found.")
        return False

    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                write_data(books, BOOKS_FILE)

                borrows = read_data(BORROWS_FILE)
                borrows.append({"book_id": book_id, "member_id": member_id})
                write_data(borrows, BORROWS_FILE)

                print("Book borrowed successfully.")
            else:
                reservations = read_data(RESERVATIONS_FILE)
                existing_reservation = next(
                    (r for r in reservations if r["book_id"] == book_id and r["member_id"] == member_id), None)
                if existing_reservation:
                    print("Reservation already made.")
                else:
                    choice = input("Book is currently unavailable. Do you want to make a reservation? (yes/no): ")
                    if choice.lower() == "yes":
                        make_reservation(book_id, member_id)
                    else:
                        print("No reservation made.")
            return
    print("Book not found.")


# Function to list all borrowed books
def list_borrowed_books():
    borrows = read_data(BORROWS_FILE)
    books = read_data(BOOKS_FILE)
    members = read_data(MEMBERS_FILE)

    if borrows:
        print("Borrowed Books:")
        print("{:<5} {:<30} {:<20} {:<15} {:<10}".format("ID", "Title", "Author", "Member Name", "Member ID"))
        for borrow in borrows:
            for book in books:
                if book["id"] == borrow["book_id"]:
                    for member in members:
                        if member["id"] == borrow["member_id"]:
                            print("{:<5} {:<30} {:<20} {:<15} {:<10}".format(book["id"], book["title"], book["author"],
                                                                             member["name"], member["id"]))
                            break
                    break
    else:
        print("No books are currently borrowed.")


# Function to make a reservation
def make_reservation(book_id, member_id):
    reservations = read_data(RESERVATIONS_FILE)
    reservations.append({"book_id": book_id, "member_id": member_id})
    write_data(reservations, RESERVATIONS_FILE)
    print("Reservation made successfully.")


# Function to manage book records
def manage_books(action, book_info):
    books = read_data(BOOKS_FILE)
    if action == "create":
        book_info["id"] = len(books) + 1  # Assign a unique ID
        books.append(book_info)
        print("Book created successfully.")
    elif action == "read":
        book_id = book_info["id"]
        found_book = next((book for book in books if book["id"] == book_id), None)
        if found_book:
            print("Book Details:")
            print(
                f"ID: {found_book['id']}, Title: {found_book['title']}, Author: {found_book['author']}, Available: {found_book['available']}")
        else:
            print("Book not found.")
    elif action == "update":
        book_id = book_info["id"]
        for book in books:
            if book["id"] == book_id:
                book.update(book_info)
                print("Book updated successfully.")
                break
        else:
            print("Book not found.")
    elif action == "delete":
        book_id = book_info["id"]
        books = [book for book in books if book["id"] != book_id]
        print("Book deleted successfully.")
    else:
        print("Invalid action.")

    write_data(books, BOOKS_FILE)


# Function to manage member profiles
def manage_members(action, member_info):
    members = read_data(MEMBERS_FILE)
    if action == "create":
        member_info["id"] = len(members) + 1  # Assign a unique ID
        members.append(member_info)
        print("Member profile created successfully.")
    elif action == "read":
        member_id = member_info["id"]
        found_member = next((member for member in members if member["id"] == member_id), None)
        if found_member:
            print("Member Details:")
            print(f"ID: {found_member['id']} \nName: {found_member['name']} \nEmail: {found_member['email']}")
        else:
            print("Member not found.")
    elif action == "update":
        member_id = member_info["id"]
        for member in members:
            if member["id"] == member_id:
                member.update(member_info)
                print("Member profile updated successfully.")
                break
        else:
            print("Member not found.")
    elif action == "delete":
        member_id = member_info["id"]
        members = [member for member in members if member["id"] != member_id]
        print("Member profile deleted successfully.")
    else:
        print("Invalid action.")

    write_data(members, MEMBERS_FILE)


# Function to receive returned books
def receive_returned_book(book_id):
    books = read_data(BOOKS_FILE)
    borrows = read_data(BORROWS_FILE)

    for book in books:
        if book["id"] == book_id:
            book["available"] = True
            print("Book marked as returned successfully.")
            break
    else:
        print("Book not found.")

    # Remove borrow record for the returned book
    updated_borrows = [borrow for borrow in borrows if borrow["book_id"] != book_id]
    write_data(updated_borrows, BORROWS_FILE)

    write_data(books, BOOKS_FILE)


# Function to list all Members
def list_all_members():
    members = read_data(MEMBERS_FILE)
    if members:
        print("All Members:")
        print("{:<5} {:<20} {:<30}".format("ID", "Name", "Email"))
        for member in members:
            print("{:<5} {:<20} {:<30}".format(member["id"], member["name"], member["email"]))
    else:
        print("No members found.")


# Function to book summary
def book_summary():
    books = read_data(BOOKS_FILE)
    total_books = len(books)
    total_available_books = sum(book["available"] for book in books)
    total_unavailable_books = total_books - total_available_books

    print("Book Summary:")
    print(f"Total Books: {total_books}")
    print(f"Total Available Books: {total_available_books}")
    print(f"Total Unavailable Books: {total_unavailable_books}")
    # Display reservation queue for a specific book
    book_id = int(input("Enter book ID to view reservation queue (or enter 0 to skip): "))
    if book_id != 0:
        reservations = read_data(RESERVATIONS_FILE)
        reservation_queue = [reservation for reservation in reservations if reservation["book_id"] == book_id]
        if reservation_queue:
            print(f"Reservation Queue for Book ID {book_id}:")
            print("{:<10} {:<20} {:<30}".format("Member ID", "Name", "Email"))
            for reservation in reservation_queue:
                member_id = reservation["member_id"]
                member = next((member for member in read_data(MEMBERS_FILE) if member["id"] == member_id), None)
                if member:
                    print("{:<10} {:<20} {:<30}".format(member_id, member["name"], member["email"]))
                else:
                    print("{:<10} {:<20} {:<30}".format(member_id, "Not found", "Not found"))
        else:
            print("No reservations found for this book.")


# Function to list all reservation
def list_all_reservation_books():
    reservations = read_data(RESERVATIONS_FILE)
    books = read_data(BOOKS_FILE)

    if reservations:
        reserved_books = []
        for reservation in reservations:
            for book in books:
                if book["id"] == reservation["book_id"]:
                    reserved_books.append(book)
                    break

        if reserved_books:
            print("All Reservation Books:")
            print("{:<5} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Available"))
            for book in reserved_books:
                print("{:<5} {:<30} {:<20} {:<10}".format(book["id"], book["title"], book["author"], "No"))
        else:
            print("No reservation books found.")
    else:
        print("No reservations found.")


# Function to reservation to borrow
def convert_reservation_to_borrow(book_id, member_id):
    # Check if the book is available
    books = read_data(BOOKS_FILE)
    book = next((book for book in books if book["id"] == book_id), None)
    if book is None:
        print("Book not found.")
        return

    if not book["available"]:
        print("Book is not available for borrowing.")
        return

    # Check if the member has already borrowed the same book
    borrows = read_data(BORROWS_FILE)
    if any(borrow["book_id"] == book_id and borrow["member_id"] == member_id for borrow in borrows):
        print("You have already borrowed this book.")
        return

    # Remove the reservation record
    reservations = read_data(RESERVATIONS_FILE)
    reservations = [reservation for reservation in reservations if
                    reservation["book_id"] != book_id or reservation["member_id"] != member_id]
    write_data(reservations, RESERVATIONS_FILE)

    # Add a new borrow record
    borrow_record = {"book_id": book_id, "member_id": member_id}
    borrows.append(borrow_record)
    write_data(borrows, BORROWS_FILE)

    # Update the book availability
    book["available"] = False
    write_data(books, BOOKS_FILE)

    print("Book borrowed successfully.")


# Function to delete reservation
def delete_reservation(book_id, member_id):
    # Remove the reservation record
    reservations = read_data(RESERVATIONS_FILE)
    updated_reservations = [reservation for reservation in reservations if
                            reservation["book_id"] != book_id or reservation["member_id"] != member_id]
    if len(reservations) == len(updated_reservations):
        print("Reservation not found.")
    else:
        write_data(updated_reservations, RESERVATIONS_FILE)
        print("Reservation deleted successfully.")


# Main function for customer application
def customer_main():
    print("Welcome to LMS STAFF Application")

    while True:
        print("******------******")
        print("Select an option:")
        print("******------******")
        print("{:<5} {:<25}".format("Option", "Description"))
        print("******------******")
        options = [
            ("1.", "Search for books"),
            ("2.", "Customer Borrow / Reservation book"),
            ("3.", "Receive returned book"),
            ("4.", "Manage books"),
            ("5.", "Manage members"),
            ("6.", "List all books"),
            ("7.", "List all members"),
            ("8.", "List available books"),
            ("9.", "List reservation books"),
            ("10.", "List Borrowed books"),
            ("11.", "Reservation to Borrowed books"),
            ("12.", "Delete Reservation"),
            ("13.", "View book summary"),
            ("14.", "Exit")
        ]
        for option in options:
            print("{:<5} {:<25}".format(option[0], option[1]))
        print("******------******")

        choice = input("Enter your choice: ")

        if choice == "1":
            keyword = input("Enter keyword to search for books: ")
            print("******------******")
            search_books(keyword)

        elif choice == "2":
            book_id = int(input("Enter book ID to borrow: "))
            member_id = int(input("Enter your member ID: "))  # Assuming customer has a member ID
            print("******------******")
            borrow_or_reserve_book(book_id, member_id)

        elif choice == "3":
            book_id = int(input("Enter book ID to mark as returned: "))
            print("******------******")
            receive_returned_book(book_id)

        elif choice == "4":
            action = input("Enter action (create/read/update/delete): ")
            book_info = {}
            if action in "create":
                book_info["title"] = input("Enter book title: ")
                book_info["author"] = input("Enter book author: ")
                book_info["available"] = input("Is book available? (True/False): ").lower() == "true"
            elif action == "update":
                book_info["id"] = int(input("Enter book ID: "))
                book_info["title"] = input("Enter book title: ")
                book_info["author"] = input("Enter book author: ")
                book_info["available"] = input("Is book available? (True/False): ").lower() == "true"
            elif action == "read" or action == "delete":
                book_info["id"] = int(input("Enter book ID: "))
            else:
                print("Invalid action.")
                continue
            print("******------******")
            manage_books(action, book_info)

        elif choice == "5":
            action = input("Enter action (create/read/update/delete): ")
            member_info = {}
            if action in "create":
                member_info["name"] = input("Enter member name: ")
                member_info["email"] = input("Enter member email: ")
            elif action == "update":
                member_info["id"] = int(input("Enter member ID: "))
                member_info["name"] = input("Enter member name: ")
                member_info["email"] = input("Enter member email: ")
            elif action == "read" or action == "delete":
                member_info["id"] = int(input("Enter member ID: "))
            else:
                print("Invalid action.")
                continue
            print("******------******")
            manage_members(action, member_info)

        elif choice == "6":
            list_all_books()

        elif choice == "7":
            list_all_members()

        elif choice == "8":
            display_available_books()

        elif choice == "9":
            list_all_reservation_books()

        elif choice == "10":
            list_borrowed_books()

        elif choice == "11":
            book_id = int(input("Enter book ID to borrow: "))
            member_id = int(input("Enter your member ID: "))  # Assuming customer has a member ID
            print("******------******")
            convert_reservation_to_borrow(book_id, member_id)

        elif choice == "12":
            book_id = int(input("Enter book ID to borrow: "))
            member_id = int(input("Enter your member ID: "))  # Assuming customer has a member ID
            print("******------******")
            delete_reservation(book_id, member_id)

        elif choice == "13":
            book_summary()

        elif choice == "14":
            print("Exiting Customer Application...")
            break

        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    customer_main()
