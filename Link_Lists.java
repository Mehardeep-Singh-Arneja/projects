class Node
{
    Object data;
    Node next = null;
    public Node(Object data)
    {
        this.data = data;
    }
}

public class LinkedList
{
    Node head = null;

    public Node add(Object value)
    {
        if (this.head == null)
        {
            this.head = new Node(value);
            return head;
        }
        Node curr = this.head;
        while (curr.next != null)
        {
            curr = curr.next;
        }
        curr.next = new Node(value);
        return curr.next;
    }

    public void printll()
    {
        Node curr = this.head;
        while (curr != null)
        {
            System.out.printf(curr.data+" -→ ");
            curr = curr.next;
        }
        System.out.printf("None");
    }
}
