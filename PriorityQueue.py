class Node:
    def __init__(self, nodeId, length):
        self.nodeId = nodeId
        self.length = length
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __len__(self):
        temp = self.head
        count = 0
        while temp is not None:
            count += 1
            temp = temp.next

        return count

    def insertAtHead(self, node):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = node

    def delete(self, node):
        temp = self.head
        while temp is not None:
            if temp.nodeId != node:
                temp = temp.next
            else:
                if temp == self.head:
                    self.head = self.head.next
                    if self.head is not None:
                        self.head.prev = None
                elif temp == self.tail:
                    self.tail = self.tail.prev
                    if self.tail is not None:
                        self.tail.next = None
                else:
                    prev = temp.prev
                    curr = temp.next
                    prev.next = curr
                    curr.prev = prev
                del temp
                return

    def insertAtTail(self, node):
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def insert(self, node):
        if self.__len__() == 0 or node.length <= self.head.length:
            self.insertAtHead(node)
        elif node.length >= self.tail.length:
            self.insertAtTail(node)
        else:
            temp = self.head.next
            prev = self.head
            while temp is not None:
                if temp.length >= node.length >= prev.length:
                    node.next = temp
                    temp.prev = node
                    node.prev = prev
                    prev.next = node
                    break
                else:
                    temp = temp.next
                    prev = prev.next


class PriorityQueue:
    def __init__(self):
        self.prioList = LinkedList()

    def enqueue(self, node, length):
        self.prioList.insert(Node(node, length))

    def dequeue(self):
        node = {
            "nodeId": self.prioList.head.nodeId,
            "length": self.prioList.head.length
        }

        self.prioList.delete(self.prioList.head.nodeId)
        return node

    def isEmpty(self):
        if len(self.prioList) == 0:
            return True
        return False
