import time
import re
import sys

class Book:
    def __init__(self, book_id, book_name, author_name, availability_status):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = None
        self.reservation_heap = MinHeap()

    def make_reservation(self, patron_id, priority):
        patron = Patron(patron_id, priority)
        reservation = (patron_id, priority, patron.timestamp)
        self.reservation_heap.insert(reservation)

    def cancel_reservation(self, patron_id):
        new_heap = MinHeap()
        while self.reservation_heap.size() > 0:
            reservation = self.reservation_heap.pop()
            if reservation[0] != patron_id:
                new_heap.insert(reservation)
        self.reservation_heap = new_heap

    def get_next_reservation(self):
        if self.reservation_heap.size() > 0:
            return self.reservation_heap.peek()
        return None

    def return_book(self):
        if self.reservation_heap.size() > 0:
            patron_id, _, _ = self.reservation_heap.pop()
            return patron_id
        return None

BLACK = 'black'
RED = 'red'
#RBTNode initiates only the node which is then used by other classes like RedBlackTree
class RBTNode:
    def __init__(self, element):
        self.element = element
        self.parent = None
        self.color = RED
        self.leftChild = None
        self.rightChild = None


class RedBlackTree:
    def __init__(self):
        self.NIL = RBTNode(None)
        self.NIL.color = BLACK
        self.NIL.leftChild = None
        self.NIL.rightChild = None
        self.root = self.NIL
        self.color_flip_count=0

    def leftRotation(self, node: RBTNode) -> None:
        nodeRightChild = node.rightChild
        node.rightChild = nodeRightChild.leftChild

        if nodeRightChild.leftChild != self.NIL:
            nodeRightChild.leftChild.parent = node

        nodeRightChild.parent = node.parent

        if node.parent is None:
            self.root = nodeRightChild
        elif node == node.parent.leftChild:
            node.parent.leftChild = nodeRightChild
        else:
            node.parent.rightChild = nodeRightChild

        nodeRightChild.leftChild = node
        node.parent = nodeRightChild

    def rightRotation(self, node: RBTNode) -> None:
        nodeLeftChild = node.leftChild
        node.leftChild = nodeLeftChild.rightChild

        if nodeLeftChild.rightChild != self.NIL:
            nodeLeftChild.rightChild.parent = node

        nodeLeftChild.parent = node.parent

        if node.parent is None:
            self.root = nodeLeftChild
        elif node == node.parent.rightChild:
            node.parent.rightChild = nodeLeftChild
        else:
            node.parent.leftChild = nodeLeftChild

        nodeLeftChild.rightChild = node
        node.parent = nodeLeftChild
    #called from the function insert()
    def insertionFix(self, node: RBTNode) -> None:
        while node.parent and node.parent.color == RED:
            if node.parent == node.parent.parent.leftChild:
                otherNode = node.parent.parent.rightChild
                if otherNode.color == RED:
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(otherNode and otherNode.color == RED):
                      self.color_flip_count += 1
                    otherNode.color = BLACK
                    if(node.parent.parent and node.parent.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.rightChild:
                        node = node.parent
                        self.leftRotation(node)
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(node.parent.parent and node.parent.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.parent.color = RED
                    self.rightRotation(node.parent.parent)
            else:
                otherNode = node.parent.parent.leftChild
                if otherNode.color == RED:
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(otherNode and otherNode.color == RED):
                      self.color_flip_count += 1
                    otherNode.color = BLACK
                    if(node.parent.parent and node.parent.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.leftChild:
                        node = node.parent
                        self.rightRotation(node)
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(node.parent.parent and node.parent.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.parent.color = RED
                    self.leftRotation(node.parent.parent)
            if node == self.root:
                break
        self.root.color = BLACK

    def insert(self, element: Book) -> None:
        node = RBTNode(element)
        node.leftChild = self.NIL
        node.rightChild = self.NIL

        nodeParent = None
        tempNodeParent = self.root

        while tempNodeParent != self.NIL:
            nodeParent = tempNodeParent
            if node.element.book_id < tempNodeParent.element.book_id:
                tempNodeParent = tempNodeParent.leftChild
            else:
                tempNodeParent = tempNodeParent.rightChild

        node.parent = nodeParent
        if nodeParent is None:
            self.root = node
        elif node.element.book_id < nodeParent.element.book_id:
            nodeParent.leftChild = node
        else:
            nodeParent.rightChild = node

        self.insertionFix(node)
    #called from the function delete()
    def deletionFix(self, node: RBTNode) -> None:
        while node != self.root and node.color == BLACK:
            if node == node.parent.leftChild:
                otherNode = node.parent.rightChild
                # type 1
                if otherNode.color == RED:
                    #print("invoke 11")
                    otherNode.color = BLACK
                    self.color_flip_count += 1
                    if(node.parent and node.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.color = RED
                    self.leftRotation(node.parent)
                    otherNode = node.parent.rightChild
                # type 2
                if otherNode.leftChild.color == BLACK and otherNode.rightChild.color == BLACK:
                    #print("invoke 12")
                    if(otherNode and otherNode.color == BLACK):
                      self.color_flip_count += 1
                    otherNode.color = RED
                    node = node.parent
                else:
                    # type 3
                    if otherNode.rightChild.color == BLACK:
                        #print("invoke 13")
                        if(otherNode.leftChild and otherNode.leftChild.color == RED):
                          self.color_flip_count += 1
                        otherNode.leftChild.color = BLACK
                        if(otherNode and otherNode.color == BLACK):
                          self.color_flip_count += 1
                        otherNode.color = RED
                        self.rightRotation(otherNode)
                        otherNode = node.parent.rightChild
                    # type 4
                    if(otherNode and node.parent and (otherNode.color != node.parent.color)):
                      self.color_flip_count += 0
                    otherNode.color = node.parent.color
                    #print("invoke 14")
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(otherNode.rightChild and otherNode.rightChild.color == RED):
                      self.color_flip_count += 1
                    otherNode.rightChild.color = BLACK
                    self.leftRotation(node.parent)
                    node = self.root
            else:
                otherNode = node.parent.leftChild
                # type 1
                if otherNode.color == RED:
                    #print("invoke 21")
                    if(otherNode and otherNode.color == RED):
                      self.color_flip_count += 1
                    otherNode.color = BLACK
                    if(node.parent and node.parent.color == BLACK):
                      self.color_flip_count += 1
                    node.parent.color = RED

                    self.rightRotation(node.parent)
                    otherNode = node.parent.leftChild
                # type 2
                if otherNode.rightChild.color == BLACK and otherNode.leftChild.color == BLACK:
                    #print("invoke 22")
                    if(otherNode and otherNode.color == BLACK):
                      self.color_flip_count += 1
                    otherNode.color = RED
                    node = node.parent
                else:
                    # type 3
                    if otherNode.leftChild.color == BLACK:
                        #print("invoke 23")
                        if(otherNode.rightChild and otherNode.rightChild.color == RED):
                          self.color_flip_count += 1
                        otherNode.rightChild.color = BLACK
                        if(otherNode and otherNode.color == BLACK):
                          self.color_flip_count += 1
                        otherNode.color = RED
                        self.leftRotation(otherNode)
                        otherNode = node.parent.leftChild
                    # type 4
                    if(otherNode and node.parent and (otherNode.color != node.parent.color)):
                      self.color_flip_count += 0
                    #print("invoke 24")
                    otherNode.color = node.parent.color
                    if(node.parent and node.parent.color == RED):
                      self.color_flip_count += 1
                    node.parent.color = BLACK
                    if(otherNode.leftChild and otherNode.leftChild.color == RED):
                      self.color_flip_count += 1
                    otherNode.leftChild.color = BLACK
                    self.rightRotation(node.parent)
                    node = self.root
        node.color = BLACK

    def switch(self, firstNode: RBTNode, secondNode: RBTNode) -> None:
        if firstNode.parent is None:
            self.root = secondNode
        elif firstNode == firstNode.parent.leftChild:
            firstNode.parent.leftChild = secondNode
        else:
            firstNode.parent.rightChild = secondNode
        secondNode.parent = firstNode.parent

    def minimum(self, node: RBTNode) -> RBTNode:
        while node.leftChild != self.NIL:
            node = node.leftChild
        return node

    def delete(self, key: int) -> Book:
        node = self.search(key)

        if node == self.NIL:
            return None

        deletionNode = node
        deletionNodeColor = deletionNode.color

        # case 1
        if node.leftChild == self.NIL:
            replaceNode = node.rightChild
            self.switch(node, node.rightChild)
        # case 2
        elif node.rightChild == self.NIL:
            replaceNode = node.leftChild
            self.switch(node, node.leftChild)
        # case 3
        else:
            deletionNode = self.minimum(node.rightChild)
            deletionNodeColor = deletionNode.color
            replaceNode = deletionNode.rightChild

            if deletionNode.parent == node:
                replaceNode.parent = deletionNode
            else:
                self.switch(deletionNode, deletionNode.rightChild)
                deletionNode.rightChild = node.rightChild
                deletionNode.rightChild.parent = deletionNode

            self.switch(node, deletionNode)
            deletionNode.leftChild = node.leftChild
            deletionNode.leftChild.parent = deletionNode
            deletionNode.color = node.color

        if deletionNodeColor == BLACK:
            self.deletionFix(replaceNode)

        return node.element

    def search(self, key: int) -> RBTNode:
        node = self.root
        while node != self.NIL and key != node.element.book_id:
            if key < node.element.book_id:
                node = node.leftChild
            else:
                node = node.rightChild
        return node
    #recursive implementation of search
    def searchRange(self, node: RBTNode, startKey: int, endKey: int) -> list[Book]:
        if node == self.NIL:
            return []

        if endKey < node.element.bookID:
            return self.searchRange(node.leftChild, startKey, endKey)
        if startKey > node.element.bookID:
            return self.searchRange(node.rightChild, startKey, endKey)

        return self.searchRange(node.leftChild, startKey, endKey) + [node.element] + self.searchRange(node.rightChild, startKey, endKey)
#defines the MinHeap that is invoked during creation of each book
#every book has its own min heap
class MinHeap:
    def __init__(self, max_size=20):
        self.heap = []
        self.max_size = max_size

    def insert(self, element):
        if len(self.heap) < self.max_size:
            self.heap.append(element)
            self._heapify_up(len(self.heap) - 1)
        else:
            print("Reservation limit reached. Cannot add more reservations.")

    def pop(self):
        if self.heap:
            if len(self.heap) > 1:
                self._swap(0, len(self.heap) - 1)
            popped = self.heap.pop()
            self._heapify_down(0)
            return popped
        return None

    def peek(self):
        if self.heap:
            return self.heap[0]
        return None

    def size(self):
        return len(self.heap)

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self._compare(self.heap[parent_index], self.heap[index]):
                self._swap(parent_index, index)
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < len(self.heap) and self._compare(self.heap[left_child_index], self.heap[smallest]):
                smallest = left_child_index

            if right_child_index < len(self.heap) and self._compare(self.heap[right_child_index], self.heap[smallest]):
                smallest = right_child_index

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _compare(self, a, b):
        patron_a, priority_a, timestamp_a = a
        patron_b, priority_b, timestamp_b = b

        # Compare based on priority first
        if priority_a < priority_b:
            return False
        elif priority_a > priority_b:
            return True

        # If priorities are equal, compare based on timestamp
        return timestamp_a < timestamp_b

#defines a patron object, captures time during object creation maintaining timestamp accuracy
class Patron:
    def __init__(self, patron_id, priority):
        self.patron_id = patron_id
        self.priority = priority
        self.timestamp = time.time()

    def __lt__(self, other):
        return (self.priority, self.timestamp) < (other.priority, other.timestamp)

    def __eq__(self, other):
        return self.priority == other.priority and self.timestamp == other.timestamp

    def __repr__(self):
        return str(self.patron_id)



#main driver class that invokes all the other classes to run the implementation
#receives each command from main and parses it to interpret the command name and its arguments
class LibrarySystem:
    def __init__(self):
        self.red_black_tree = RedBlackTree()

    def print_book(self, book_id,output_file):
        book_node = self.red_black_tree.search(book_id)
        if book_node and book_node.element:
            book = book_node.element
            if(book.availability_status == 1):
              temp = "Yes"
            else:
              temp = "No"
            patron_ids = [reservation[0] for reservation in book.reservation_heap.heap]
            print(f"BookID = {book.book_id}\nTitle = {book.book_name}\n"
                  f"Author = {book.author_name}\n"
                  f"Availability = {temp}\nBorrowedBy = {book.borrowed_by}"
                  f"\nReservations = [{', '.join(map(str, patron_ids))}]\n", file=output_file)
        else:
            print(f"Book {book_id} not found in the Library\n", file=output_file)

    def print_books(self, book_id1, book_id2,output_file):
        for book_id in range(book_id1, book_id2 + 1):
            book_node = self.red_black_tree.search(book_id)
            if book_node and book_node.element:
                book = book_node.element
                if(book.availability_status==1):
                  temp = "Yes"
                else:
                  temp = "No"
                patron_ids = [reservation[0] for reservation in book.reservation_heap.heap]
                print(f"BookID = {book.book_id}\nTitle = {book.book_name}\n"
                      f"Author = {book.author_name}\n"
                      f"Availability = {temp}\nBorrowedBy = {book.borrowed_by}"
                      f"\nReservations = [{', '.join(map(str, patron_ids))}]\n", file=output_file)

    def insert_book(self, book_id, book_name, author_name, availability_status,output_file):
        book = Book(book_id, book_name, author_name, availability_status)
        self.red_black_tree.insert(book)

    def borrow_book(self, patron_id, book_id, patron_priority,output_file):
        book_node = self.red_black_tree.search(book_id)
        
        if book_node:
            book = book_node.element
            #print(f"Availability status : {book.availability_status}")
            #print(f"Borrowed by : {book.borrowed_by}")
            #print(f"Reservations before borrowing: {book.reservation_heap.heap}")
            if(book.availability_status == 1):
                book.availability_status = 0
                book.borrowed_by = patron_id
                print(f"Book {book_id} Borrowed by Patron {patron_id}\n", file=output_file)
            else:
                book.make_reservation(patron_id, patron_priority)
                print(f"Book {book_id} Reserved by Patron {patron_id}\n", file=output_file)
            #print(f"Reservations before borrowing: {book.reservation_heap.heap}")
        else:
            print(f"Book {book_id} not found in the Library\n", file=output_file)
        #print("---------------")

    def return_book(self, patron_id, book_id,output_file):
        #print(f"Returning book {book_id} by patron {patron_id}", file=output_file)
        print(f"Book {book_id} Returned by Patron {patron_id}\n", file=output_file)
        book_node = self.red_black_tree.search(book_id)
        if book_node:
            book = book_node.element
            if book.borrowed_by == patron_id:
                book.availability_status = 1
                book.borrowed_by = None
                next_reservation = book.get_next_reservation()
                #print(f"Next Reservation: {next_reservation}", file=output_file)
                if next_reservation:
                    next_patron_id = next_reservation[0]
                    print(f"Book {book_id} Allotted to Patron {next_patron_id}\n", file=output_file)
                    book.cancel_reservation(next_patron_id)
                    book.availability_status = 0
                    book.borrowed_by = next_patron_id
            else:
                print(f"Patron {patron_id} did not borrow Book {book_id}\n", file=output_file)
        else:
            print(f"Book {book_id} not found in the Library\n", file=output_file)

    def delete_book(self, book_id,output_file):
        book_node = self.red_black_tree.search(book_id)
        if book_node:
            book = book_node.element
            self.red_black_tree.delete(book_id)
            if not book.reservation_heap.heap:
                print(f"Book {book_id} is no longer available\n", file=output_file)
            else:
                canceled_patron_ids = [reservation[0] for reservation in book.reservation_heap.heap]
                print(f"Book {book_id} is no longer available. "
                      f"Reservations made by Patrons {', '.join(map(str, canceled_patron_ids))} have been cancelled!\n", file=output_file)
        else:
            print(f"Book {book_id} not found in the Library\n", file=output_file)


    def color_flip_count(self,output_file):

        flips = self.red_black_tree.color_flip_count
        print(f"Color Flip Count: {flips}\n", file=output_file)


    def find_closest_book(self, target_id,output_file):
        current = self.red_black_tree.root
        closest_smaller = None
        closest_bigger = None

        while current != self.red_black_tree.NIL:
            if target_id < current.element.book_id:
                closest_bigger = current
                current = current.leftChild
            else:
                closest_smaller = current
                current = current.rightChild

        if closest_smaller and closest_bigger:
            smaller_difference = abs(target_id - closest_smaller.element.book_id)
            bigger_difference = abs(target_id - closest_bigger.element.book_id)

            # Determine which book(s) to print
            if smaller_difference <= bigger_difference:
                closest_books = [closest_smaller.element]
                if smaller_difference == bigger_difference:
                    closest_books.append(closest_bigger.element)
            else:
                closest_books = [closest_bigger.element]

            # Sort the closest books by book ID
            closest_books.sort(key=lambda book: book.book_id)

            # Print details of closest books
            for book in closest_books:
                if(book.availability_status==1):
                  temp = "Yes"
                else:
                  temp = "No"
                patron_ids = [reservation[0] for reservation in book.reservation_heap.heap]
                print(f"BookID = {book.book_id}\nTitle = {book.book_name}\n"
                      f"Author = {book.author_name}\n"
                      f"Availability = {temp}\nBorrowedBy = {book.borrowed_by}"
                      f"\nReservations = [{', '.join(map(str, patron_ids))}]\n", file=output_file)
        else:
            print(f"No book found with BookID {target_id}", file=output_file)

    def execute_command(self, command, output_file):
        #print(f"Command : {command}", file=output_file)
        match = re.match(r'(\w+)\(([^)]*)\)', command)
        if match:
            action, args = match.groups()
            args = [arg.strip(' \'"') for arg in args.split(',')]

            if action == "InsertBook":
                match = re.match(r'InsertBook\((.*?)\)', command)

                if match:
                    # Extract values by ignoring commas within the first set of quotes
                    values = [val.strip() for val in re.split(r',(?=(?:(?:[^"]*"){2})*[^"]*$)', match.group(1))]

                    # Ensure the correct number of values
                    if len(values) == 4:
                        book_id, title, author_name, availability_status = values
                        self.insert_book(int(book_id), title, author_name, 1, output_file)
                    else:
                        print("Invalid number of arguments in InsertBook command")
                else:
                    print("Invalid command format")
            elif action == "PrintBook":
                book_id = int(args[0])
                self.print_book(book_id,output_file)
            elif action == "PrintBooks":
                book_id1, book_id2 = map(int, args)
                self.print_books(book_id1, book_id2,output_file)
            elif action == "BorrowBook":
                patron_id, book_id, patron_priority = map(int, args)
                self.borrow_book(patron_id, book_id, patron_priority,output_file)
            elif action == "ReturnBook":
                patron_id, book_id = map(int, args)
                self.return_book(patron_id, book_id,output_file)
            elif action == "DeleteBook":
                book_id = int(args[0])
                self.delete_book(book_id,output_file)
            elif action == "FindClosestBook":
                target_id = int(args[0])
                self.find_closest_book(target_id,output_file)
            elif action == "ColorFlipCount":
                self.color_flip_count(output_file)
            elif action == "Quit":
                print("Program Terminated!!", file=output_file)
                return True
            else:
                print(f"Unknown command: {command}")
        else:
            print(f"Invalid command: {command}")

        return False


def main():
    #accept command line argument, print correct usage if incorrect command line argument is passed.
    if len(sys.argv) != 2:
          print("Usage: python3 gatorLibrary.py <filename>")
          sys.exit(1)
    input_filename = sys.argv[1]
    
    output_filename = input_filename.replace(".txt", "_output_file.txt")

    library_system = LibrarySystem()

    #sequentially read each line from the input file
    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        for line in input_file:
            command = line.strip()
            if command == "Quit()":
                print("Program Terminated!!", file=output_file)
                break

            library_system.execute_command(command,output_file)


if __name__ == "__main__":
    main()