# ------------------------------------------------------------
# Ankit Kumar Mishra
# Roll No. - 2501730079
# ------------------------------------------------------------

import sys
import json
import logging
from pathlib import Path
from typing import List, Optional

# =========================================================================
# 1. SETUP: Logging Configuration and Error Handling
# =========================================================================

# Task 5: Integrate Python's logging module with proper log levels (INFO, ERROR) [cite: 35]
LOG_FILE = 'library_manager.log'
# Configure logging to write to a file and output to the console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOG_FILE, mode='a'),
                        logging.StreamHandler(sys.stdout)
                    ])
logger = logging.getLogger('LibraryApp')

# =========================================================================
# 2. Book Class (Task 1: Book Class Design) [cite: 16]
# =========================================================================

class Book:
    """
    Represents a single book in the library inventory[cite: 17].
    Attributes: title, author, isbn, status ('available' or 'issued') [cite: 18]
    """
    def __init__(self, title: str, author: str, isbn: str, status: str = 'available'):
        """Initializes a new Book instance."""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status.lower() # Encapsulation

    # Task 1: __str__() method [cite: 19]
    def __str__(self):
        """Returns a human-readable string representation of the Book."""
        return f"Title: {self.title} | Author: {self.author} | ISBN: {self.isbn} | Status: {self.status.upper()}"

    # Task 1: to_dict() method for JSON serialization [cite: 19]
    def to_dict(self):
        """Returns a dictionary representation for JSON saving."""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': self.status
        }
        
    # Task 1: issue() method [cite: 20]
    def issue(self) -> bool:
        """Changes the book status to 'issued' if currently 'available'."""
        if self.is_available():
            self.status = 'issued'
            return True
        return False

    # Task 1: return_book() method [cite: 20]
    def return_book(self) -> bool:
        """Changes the book status to 'available' if currently 'issued'."""
        if self.status == 'issued':
            self.status = 'available'
            return True
        return False

    # Task 1: is_available() method [cite: 20]
    def is_available(self) -> bool:
        """Checks if the book is currently 'available'."""
        return self.status == 'available'

# =========================================================================
# 3. Inventory Manager Class (Task 2 & 3: Persistence) [cite: 21, 25]
# =========================================================================

class LibraryInventory:
    """
    Manages the collection of Book objects and handles file persistence with JSON[cite: 22, 26].
    """
    def __init__(self, data_file: str = 'book_catalog.json'):
        # Task 2: Maintain a list of Book objects [cite: 23]
        self.books: List[Book] = []
        # Task 3: Use pathlib.Path for file operations [cite: 27]
        self.data_file = Path(data_file) 
        self._load_catalog()

    def _load_catalog(self):
        """
        Loads the book catalog from the JSON file. Handles missing/corrupted files[cite: 26, 28].
        """
        # Task 3 & 5: Handle missing or corrupted files with try-except [cite: 28, 34]
        try: 
            if self.data_file.exists(): 
                with self.data_file.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Recreate Book objects from the dictionary list
                    self.books = [Book(**book_dict) for book_dict in data] 
                logger.info("Catalog loaded successfully from %s", self.data_file)
            else:
                # Handle missing file exceptions [cite: 28]
                logger.info("Catalog file not found (%s). Starting with an empty inventory.", self.data_file)
        except json.JSONDecodeError:
            logger.error("Catalog file is corrupted (JSONDecodeError). Starting with an empty inventory.", exc_info=True)
            self.books = []
        except Exception as e:
            logger.error("An unexpected error occurred while loading the catalog: %s", e, exc_info=True)
            self.books = []

    def save_catalog(self):
        """Saves the current book catalog to the JSON file."""
        try: # Task 5: Use try–except blocks for file operations [cite: 34]
            # Convert Book objects to dictionaries for JSON serialization
            data = [book.to_dict() for book in self.books]
            with self.data_file.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logger.info("Catalog saved successfully to %s", self.data_file)
        except Exception as e:
            logger.error("Failed to save catalog: %s", e, exc_info=True)
            raise # Re-raise to inform the calling function (CLI)

    # Task 2: add_book() method [cite: 24]
    def add_book(self, book: Book) -> bool:
        """Adds a Book object to the inventory. Checks for existing ISBN."""
        if any(b.isbn == book.isbn for b in self.books):
            logger.warning("Attempted to add a book with duplicate ISBN: %s", book.isbn)
            return False
        self.books.append(book)
        self.save_catalog()
        return True

    # Task 2: search_by_title() method [cite: 24]
    def search_by_title(self, title: str) -> List[Book]:
        """Searches for books whose title contains the search string (case-insensitive)."""
        search_term = title.lower()
        return [book for book in self.books if search_term in book.title.lower()]

    # Task 2: search_by_isbn() method [cite: 24]
    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        """Searches for a single book matching the exact ISBN."""
        return next((book for book in self.books if book.isbn == isbn), None)

    # Task 2: display_all() method [cite: 24]
    def display_all(self):
        """Returns the entire list of books."""
        return self.books

# =========================================================================
# 4. Command Line Interface (Task 4 & 5: CLI and Exception Handling) [cite: 29]
# =========================================================================

class LibraryCLI:
    """
    Menu-Driven Command Line Interface for the Library Inventory Manager[cite: 30].
    """
    def __init__(self, data_file: str = 'book_catalog.json'):
        self.inventory = LibraryInventory(data_file)

    def _get_input(self, prompt: str, input_type=str, allow_empty: bool = False) -> Optional[str]:
        """
        Helper function for consistent input and validation[cite: 32].
        """
        while True:
            try: # Task 5: Use try–except blocks for input operations [cite: 34]
                user_input = input(prompt).strip()
                if not user_input and not allow_empty:
                    print("Input cannot be empty. Please try again.")
                    logger.warning("Empty input received.")
                    continue
                
                # Simple type validation 
                if input_type is int:
                    return int(user_input)
                
                return user_input
            except (EOFError, KeyboardInterrupt):
                print("\nOperation cancelled by user.")
                logger.info("Input cancelled.")
                return None
            except ValueError:
                print(f"Invalid input type. Expected {input_type.__name__}.")
                logger.error("ValueError on input.")

    # --- Core Menu Operations ---

    def add_book(self):
        """Adds a book to the inventory."""
        print("\n--- Add New Book ---")
        try: # Task 5: Use try–except blocks for input operations [cite: 34]
            title = self._get_input("Enter Title: ")
            author = self._get_input("Enter Author: ")
            isbn = self._get_input("Enter ISBN (unique identifier): ")
            
            if not all([title, author, isbn]):
                print("Book details cannot be empty. Operation cancelled.")
                return

            new_book = Book(title=title, author=author, isbn=isbn)
            if self.inventory.add_book(new_book):
                print(f"\n✅ Book added successfully: {new_book}")
            else:
                print(f"\n❌ ERROR: Book with ISBN '{isbn}' already exists. Not added.")
                logger.error("Failed to add book due to duplicate ISBN: %s", isbn)

        except Exception as e:
            print(f"\n❌ An unexpected error occurred while adding the book: {e}")
            logger.error("Error during Add Book operation.", exc_info=True)


    def issue_return_book(self, operation: str):
        """Handles issuing or returning a book by ISBN."""
        action = "issue" if operation == "issue" else "return"
        print(f"\n--- {action.title()} Book ---")
        try: # Task 5: Use try–except blocks for input operations [cite: 34]
            isbn = self._get_input(f"Enter the ISBN of the book to {action}: ")
            if not isbn:
                return

            book = self.inventory.search_by_isbn(isbn)

            if book:
                if operation == "issue" and book.issue():
                    self.inventory.save_catalog()
                    print(f"\n✅ Book issued successfully: {book.title} (Status: {book.status.upper()})")
                elif operation == "return" and book.return_book():
                    self.inventory.save_catalog()
                    print(f"\n✅ Book returned successfully: {book.title} (Status: {book.status.upper()})")
                else:
                    print(f"\n⚠️ Action failed. Book is already {book.status}.")
                    logger.info("Action failed: Book already in desired state (%s)", book.status)
            else:
                print(f"\n❌ Book with ISBN '{isbn}' not found.")
                logger.info("ISBN not found for %s operation: %s", operation, isbn)

        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            logger.error(f"Error during {operation} book operation.", exc_info=True)


    def search_books(self):
        """Allows searching by title or ISBN."""
        print("\n--- Search Book ---")
        print("1. Search by Title")
        print("2. Search by ISBN")
        
        choice = self._get_input("Enter choice (1 or 2): ")
        if not choice:
            return

        try:
            if choice == '1':
                search_term = self._get_input("Enter search term (part of title): ")
                if not search_term: return
                results = self.inventory.search_by_title(search_term)
                
            elif choice == '2':
                isbn = self._get_input("Enter exact ISBN: ")
                if not isbn: return
                book = self.inventory.search_by_isbn(isbn)
                results = [book] if book else []
                
            else:
                print("\n⚠️ Invalid search choice. Returning to main menu.")
                return

            if results:
                print("\n--- Search Results ---")
                for book in results:
                    print(book)
            else:
                print("\n❌ No books found matching your search criteria.")
                logger.info("No search results found.")

        except Exception as e:
            print(f"\n❌ An unexpected error occurred during search: {e}")
            logger.error("Error during search operation.", exc_info=True)


    def view_all_books(self):
        """Displays all books in the catalog."""
        print("\n--- Current Library Catalog ---")
        books = self.inventory.display_all()
        if books:
            # Sort for better display organization
            sorted_books = sorted(books, key=lambda b: b.title.lower())
            for book in sorted_books:
                print(book)
        else:
            print("The library inventory is currently empty.")


    def display_menu(self):
        """Displays the interactive CLI menu."""
        print("\n" + "="*40)
        print("📚 Library Inventory Manager CLI")
        print("="*40)
        print("1. Add New Book")  # [cite: 31]
        print("2. Issue Book")    # [cite: 31]
        print("3. Return Book")   # [cite: 31]
        print("4. View All Books")# [cite: 31]
        print("5. Search Book")   # [cite: 31]
        print("6. Exit")          # [cite: 31]
        print("-"*40)


    def run(self):
        """Main loop for the CLI."""
        while True:
            self.display_menu()
            
            choice = self._get_input("Enter your choice (1-6): ", allow_empty=True)
            if not choice:
                continue

            try: # Task 5: Use try–except blocks for all file and input operations [cite: 34]
                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.issue_return_book("issue")
                elif choice == '3':
                    self.issue_return_book("return")
                elif choice == '4':
                    self.view_all_books()
                elif choice == '5':
                    self.search_books()
                elif choice == '6':
                    break # Exit loop
                else:
                    print("\n⚠️ Invalid choice. Please enter a number between 1 and 6.")
                    logger.warning("Invalid menu choice: %s", choice)
            
            except Exception as e:
                print(f"\n❌ CRITICAL ERROR in application loop: {e}")
                logger.critical("Unhandled exception in main loop.", exc_info=True)
                break
            
            finally: # Task 5: Use finally block to ensure saving before exit [cite: 34]
                # Ensure the latest state is saved before the program terminates
                    try:
                         self.inventory.save_catalog()
                    except Exception:
                # Log the error but continue exiting
                        logger.error("Failed to save catalog during final shutdown.", exc_info=True)
            
            print("\n👋 Thank you for using the Library Inventory Manager. Exiting.")
            logger.info("Application successfully exited.")

# =========================================================================
# 5. Execution
# =========================================================================

if __name__ == "__main__":
    # The default data file name will be 'book_catalog.json' in the same directory
    cli = LibraryCLI() 
    cli.run()