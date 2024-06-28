# GatorLibrary System

This repository contains the implementation of the GatorLibrary system, developed as part of the COP5536 – Advanced Data Structures course at the University of Florida, Fall 2023.

## Project Overview

The GatorLibrary system is designed to manage a library's book inventory and handle patron reservations using efficient data structures. The system utilizes a Red-Black Tree (RBT) for book management and a Min-Heap for priority-based reservation handling.

## Features

- **Book Management:** Insertion, deletion, and search operations are performed using a Red-Black Tree.
- **Reservation System:** Priority-based reservations are managed using a Min-Heap.
- **Persistent System:** The system remains active until the `Quit()` command is issued.
- **Command-Line Interface:** The system processes commands from an input file provided as a command-line argument.

## Classes and Methods

### 1. Book Class

Encapsulates book-related operations.
- `make_reservation(patron_id, priority)`: Adds a reservation for a patron with a given priority.
- `cancel_reservation(patron_id)`: Cancels a reservation made by a patron.
- `get_next_reservation()`: Retrieves the highest-priority patron from the reservation queue.
- `return_book()`: Marks the book as returned.

### 2. RBTNode Class

Defines nodes within the Red-Black Tree.

### 3. RedBlackTree Class

Manages the Red-Black Tree structure.
- `leftRotation(RBTNode)`: Performs a left rotation.
- `rightRotation(RBTNode)`: Performs a right rotation.
- `insertionFix(RBTNode)`: Fixes violations during insertion.
- `delete(book_id)`: Removes a book node.
- `insert(Book)`: Adds a book node.
- `search(book_id)`: Retrieves a book node by ID.
- `switch(RBTNode)`: Swaps nodes during deletion.

### 4. MinHeap Class

Manages priority queues for reservations.
- `insert(element)`: Adds a new reservation to the priority queue.
- `pop()`: Removes and returns the highest-priority reservation.
- `peek()`: Returns the highest-priority reservation without removal.
- `_heapify_up(index)`: Maintains heap properties during insertion.
- `_heapify_down(index)`: Maintains heap properties during deletion.
- `_swap(i, j)`: Swaps two elements in the heap.

### 5. Patron Class

Represents patrons in the library system.
- `__init__(patronID, priority, timestamp)`: Initializes a patron object.

### 6. LibrarySystem Class

Orchestrates various operations within the library system.
- `print_book(book_id)`: Prints details of a specific book.
- `print_books(book_id1, book_id2)`: Prints details of books within a specified range.
- `insert_book(book_id, book_name, author_name, availability_status)`: Inserts a new book into the library system.
- `borrow_book(patron_id, book_id, patron_priority)`: Facilitates borrowing a book by a patron.
- `return_book(patron_id, book_id)`: Handles the return of a book.
- `delete_book(book_id)`: Deletes a book from the library system.
- `color_flip_count()`: Counts the number of color flips during RBT operations.
- `find_closest_book(target_id)`: Finds the book with an ID closest to the specified target ID.
- `execute_command(command)`: Parses and executes commands provided in the input file.

## Project Structure

- `gatorLibrary.py`: Contains all relevant classes and functions for the GatorLibrary system.
- `input.txt`: Example input file with commands to be processed by the system.

## Running the Project

To run the GatorLibrary system, provide the input file as a command-line argument:

```sh
python gatorLibrary.py input.txt
```

## Conclusion

The GatorLibrary system efficiently manages library operations using advanced data structures, ensuring fast and reliable performance. The combination of a Red-Black Tree for book management and a Min-Heap for reservations provides an optimal solution for library systems.
