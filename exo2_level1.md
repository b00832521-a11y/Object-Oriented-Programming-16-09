# UML exo 2 - ABCD Records - Level 1

Statement: ABCD Records is a mail-order company selling CDs and tapes to record club members.
Level 1: Task 1.1 use case diagram, Task 1.2 class diagram.

![Exo 2 Level 1](exo2_level1.jpg)

## Task 1.1 - Use case diagram
- Actors (outside the system boundary): Member, Order Processing Clerk.
- Use cases (inside "ABCD system"): Place Order, Verify Membership, Process Order, Make Payment.
- Member: Place Order, Make Payment. Order Processing Clerk: Verify Membership, Process Order.
- Place Order <<include>> Verify Membership (only members can place orders: always checked).

## Task 1.2 - Class diagram
- Member: id, name, class; placeOrder(), pay().
- Order: id, item, date; saveRecord(), updateStatus().
- OrderProcessingClerk: id, name; handleVerification(), handleProcessing().
- Associations: Member 1 -- 1..* Order; Order * -- 0..1 OrderProcessingClerk; Member and OrderProcessingClerk linked by a verification relation.
