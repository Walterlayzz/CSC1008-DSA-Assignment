
class Passenger:
    def __init__(self, passengerId, name, fromLongitude, fromLatitude, toLongitude, toLatitude):
        self.driverId = passengerId
        self.name = name
        self.fromLongitude = fromLongitude
        self.fromLatitude = fromLatitude
        self.toLongitude = toLongitude
        self.toLatitude = toLatitude
        self.next = None
        self.prev = None
#
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
