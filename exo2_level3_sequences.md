# UML exo 2 - ABCD Records - Level 3 - Sequence diagrams

Statement: create sequence diagrams for (1) Complete Order Processing Flow, (2) Membership Verification (success and failure), (3) Payment Processing (all types), (4) Item Reordering for Royal Members.

![Exo 2 Level 3 - sequence diagrams 1 to 3](exo2_level3_sequences.jpg)

## Scenario 1 - Complete order processing flow (top of the page)
- Participants: Member, Order, OrderProcessingClerk, Item, Invoice, ShippingList.
- Flow: Member places the order -> clerk verifies membership (handleVerification) -> clerk checks item availability -> clerk creates Invoice and ShippingList -> updateStatus / saveRecord -> confirmation to the member.

## Scenario 2 - Membership verification (middle)
- Participants: Member, OrderProcessingClerk, MembershipApplication.
- Success: membership verified, order accepted.
- Failure: clerk creates the membership form (MembershipApplication) and the order is refused.

## Scenario 3 - Payment processing, all types (bottom)
- Participants: Member, Cash, Check, BankDraft, Invoice.
- Member calls pay(), then processPay() on Cash, Check or BankDraft (polymorphism on Payment), each answering "received".
- Invoice is then marked paid (markPaid -> invoice paid).

## Scenario 4 - Item reordering for Royal members
Not on this photo yet (to be added). Logic: the clerk checks availability and the item is unavailable. [Royal] reorder() on the item, order set to pending, order saved, member informed. [Regular] order refused.
