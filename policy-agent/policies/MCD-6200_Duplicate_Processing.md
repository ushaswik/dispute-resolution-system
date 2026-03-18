
# MCD-6200: Duplicate Transaction Processing

## Section 1: Overview
When cardholder is charged multiple times for a single transaction.

## Section 2: Identifying Duplicates

### Section 2.1: True Duplicates:
- Same merchant, same amount, same/similar time
- Multiple authorizations that posted (not just pending)
- System error caused duplicate charge
- Cardholder received only one item/service

### Section 2.2: Not Duplicates:
- Multiple intentional purchases
- Pre-authorization + final charge (hotel, gas)
- Subscription charges on same day (but different months)
- Similar amounts but different transactions

## Section 3: Evidence Review

### From Cardholder:
1. Bank statement showing duplicate charges
2. Confirmation that only one item/service received
3. Communication with merchant about duplicate

### From Merchant:
1. Transaction logs showing distinct transactions
2. Proof of multiple items shipped
3. System logs (if technical error claimed)

## Section 4: Resolution Guidelines

### Section 4.1: Automatic Approval (Fast-Track):
- Charges within 1 minute of each other, same amount → APPROVE
- Merchant already credited one → APPROVE (confirm credit processed)
- Merchant confirms system error → APPROVE

### Section 4.2: Requires Investigation:
- Charges hours/days apart but same amount
- Merchant claims both are valid separate transactions
- High-value items (>$500)

### Section 4.3: Deny If:
- Cardholder received multiple items (proof of delivery)
- Charges are for different dates (e.g., hotel multi-night stay)
- "Duplicate" is actually authorization hold + final charge

## Section 5: Special Cases

### Section 5.1: Hotel/Car Rental Holds
- Pre-authorization (hold) + final charge is NORMAL
- Hold may appear as separate charge but will drop off
- Only dispute if BOTH posted as final charges
- **Educate cardholder** - usually not a duplicate

### Section 5.2: Gas Station Transactions
- $1 authorization + actual amount is NORMAL
- Dispute only if $1 charge POSTED (rare)
- Usually DENY - educate about gas station holds

### Section 5.3: Restaurant Tips
- Original charge + tip adjustment = NOT duplicate
- Two separate final charges = duplicate → APPROVE
