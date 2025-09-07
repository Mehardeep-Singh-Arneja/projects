class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        """Add node at the end"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def prepend(self, data):
        """Add node at the beginning"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        """Delete first node with given value"""
        curr = self.head

        if curr and curr.data == key:
            self.head = curr.next
            return

        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next

        if curr is None:
            print(f"{key} not found.")
            return

        prev.next = curr.next

    def search(self, key):
        """Search for a value"""
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False

    def length(self):
        """Return number of nodes"""
        count = 0
        curr = self.head
        while curr:
            count += 1
            curr = curr.next
        return count

    def print_list(self):
        """Print linked list"""
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")


# 🔹 Example Usage 🔹

ll = LinkedList()

ll.append(10)
ll.append("20s")
ll.append(30)
ll.prepend(5)

print("Linked List:")
ll.print_list()

print("\nLength:", ll.length())

print("\nSearching for 20:", ll.search(20))
print("Searching for 30:", ll.search(30))

print("\nDeleting 20...")
ll.delete(20)
ll.print_list()
