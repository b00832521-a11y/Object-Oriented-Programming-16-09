# UML exo 2 - ABCD Records - Level 2 - Task 2.1

Statement: complete use case diagram with the additional actors (Collection Department Clerk, Non-Member) and use cases (Verify Item Availability, Apply Discount, Print Invoice, Print Shipping List, Order Unavailable Items, Send Membership Application), with include, extend and the system boundary.

![Exo 2 Task 2.1](exo2_level2_usecase.jpg)

## Actors (outside the system boundary)
Member, Non-Member, Order Processing Clerk, Collection Department Clerk.

## Use cases (inside "ABCD Records system")
Place Order, Make Payment, Apply Discount, Order Unavailable Items, Send Membership Application, Verify Membership, Verify Item Availability, Process Order, Print Invoice, Print Shipping List.

## Relations
- include (always): Place Order -> Verify Membership; Process Order -> Verify Item Availability, Print Invoice, Print Shipping List.
- extend (sometimes): Apply Discount and Order Unavailable Items extend Place Order (Royal members); Send Membership Application extends Verify Membership (non-members).
