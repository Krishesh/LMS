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
        print("{:<5} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Available"))
        for book in available_books:
            print("{:<5} {:<30} {:<20} {:<10}".format(book["id"], book["title"], book["author"], "Yes"))
    else:
        print("No books available.")


# Function to print book information
def print_book_info(book):
    print(f"Title: {book['title']}, Author: {book['author']}, Available: {book['available']}")


# Function to borrow or make a reservation for a book
def borrow_or_reserve_book(book_id, member_id):
    books = read_data(BOOKS_FILE)

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


# Function to make a reservation
def make_reservation(book_id, member_id):
    reservations = read_data(RESERVATIONS_FILE)
    books = read_data(BOOKS_FILE)
    # Check if the book or member exists
    if not any(book["id"] == book_id for book in books):
        print("Book not found.")
        return False
    if not any(member["id"] == member_id for member in read_data(MEMBERS_FILE)):
        print("Member not found.")
        return False
    # Check if the reservation already exists
    if any(reservation["book_id"] == book_id and reservation["member_id"] == member_id for reservation in reservations):
        print("Reservation already made.")
        return False

    # Add the reservation
    reservations.append({"book_id": book_id, "member_id": member_id})
    write_data(reservations, RESERVATIONS_FILE)
    print("Reservation made successfully.")
    return True


def list_borrowed_books_by_member(member_id):
    borrows = read_data(BORROWS_FILE)
    books = read_data(BOOKS_FILE)

    borrowed_books = []
    for borrow in borrows:
        if borrow["member_id"] == member_id:
            for book in books:
                if book["id"] == borrow["book_id"]:
                    borrowed_books.append(book)
                    break

    if borrowed_books:
        print(f"Borrowed Books for Member ID {member_id}:")
        print("{:<5} {:<30} {:<20} {:<10}".format("ID", "Title", "Author", "Available"))
        for book in borrowed_books:
            print("{:<5} {:<30} {:<20} {:<10}".format(book["id"], book["title"], book["author"], "No"))
    else:
        print("No borrowed books found for this member.")


# Main function for customer application
def customer_main():
    print("Welcome to LMS Customer Application")

    while True:
        print("--------------------------------------------")
        print("\nSelect an option:")
        print("1. Search for books")
        print("2. Reserve a book")
        print("******------******")
        print("3. List all books")
        print("4. Display available books")
        print("5. List of borrowed a book")

        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            keyword = input("Enter keyword to search for books: ")
            search_books(keyword)

        elif choice == "2":
            book_id = int(input("Enter book ID to borrow: "))
            books = read_data(BOOKS_FILE)
            # Check if the book or member exists
            '''
            if not any(book["id"] == book_id for book in books):
                print("Book not found.")
                return True'''
            member_id = int(input("Enter your member ID: "))  # Assuming customer has a member ID
            ''' 
             if not any(member["id"] == member_id for member in read_data(MEMBERS_FILE)):
                print("Member not found.")
                return True'''
            make_reservation(book_id, member_id)

        elif choice == "3":
            list_all_books()

        elif choice == "4":
            display_available_books()

        elif choice == "5":
            member_id = int(input("Enter member ID to list borrowed books: "))
            list_borrowed_books_by_member(member_id)

        elif choice == "6":
            print("Exiting Customer Application...")
            break
        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    customer_main()
