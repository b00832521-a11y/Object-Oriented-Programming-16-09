# UML exo 2 - ABCD Records - Level 2 - Task 2.2

Statement: complete the class diagram of Task 1.2 with the additional classes Item (CD, Tape), Invoice, ShippingList, Payment (Cash, Check, BankDraft), MembershipApplication, OrderLine. Model inheritance for Member, Payment and Item types, show all multiplicities. Scenario: a Royal member orders 2 CDs (one unavailable) and pays by check.

![Exo 2 Task 2.2 - complete class diagram](exo2_task22_class.jpg)

## Classes from Task 1.2 (kept)
- Member: id, name; placeOrder(), pay().
- Order: id, date; saveRecord(), updateStatus().
- OrderProcessingClerk: id, name; handleVerification(), handleProcessing().
- Associations: Member 1 -- 1..* Order; Order * -- 0..1 OrderProcessingClerk; Member * -- * OrderProcessingClerk (verification).

## Added classes
- Inheritance Member: RoyalMember (discount, priority, orderUnavailableItem()) and RegularMember.
- Inheritance Item: CD and Tape (Item: id, title, price; availability is an attribute, not a subclass).
- OrderLine: quantity. Order 1 composition 1..* OrderLine; OrderLine * -- 1 Item (no direct Order-Item link).
- Inheritance Payment: Cash, Check, BankDraft (each with processPay()). Member linked to Payment.
- Invoice (id, date) and ShippingList (id, date) linked to OrderProcessingClerk (1 -- *).
- MembershipApplication (id, date, status) linked to Member.

## Scenario
A RoyalMember places an Order with 2 OrderLines (2 CDs); one CD is unavailable, which only a Royal member may still order. The clerk processes the order (Invoice + ShippingList) and the member pays with a Check.

## Notes for review
- Invoice and ShippingList can be linked to Order (the order they concern) and/or to the clerk who prints them.
- Availability (available / unavailable) is better as an attribute of Item than as subclasses, because an item changes state over time.
