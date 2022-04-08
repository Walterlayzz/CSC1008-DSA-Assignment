
class Driver:
    def __init__(self, name, node, longitude, latitude):
        self.name = name
        self.node = node
        self.longitude = longitude
        self.latitude = latitude
        self.distToPass = 0






# class DriverLinkedList:
#     def __init__(self):
#         self.head = None
#         self.tail = None
#
#     def getHead(self):
#         if self.head is not None:
#             return self.head
#         return None
#
#     def insertAtHead(self, node):
#         if self.head is None:
#             self.head = self.tail = node
#         else:
#             self.head.prev = node
#             node.next = self.head
#             self.head = node
#
#     def deleteAtHead(self):
#         if self.head is None:
#             return
#         if self.head.next is None:
#             self.head = None
#             return
#         self.head = self.head.next
#         self.tail = None

