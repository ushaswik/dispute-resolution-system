"""
Create realistic sample Mastercard dispute resolution policies
"""

import os
import json

# Create policies directory
os.makedirs("policies", exist_ok=True)

# Policy database
POLICIES = [
    {
        "policy_id": "MCD-4840",
        "policy_name": "Lost/Stolen Card Liability",
        "category": "Fraud Protection",
        "content": """
# MCD-4840: Lost/Stolen Card Liability

## Section 1: Overview
When a cardholder reports their card as lost or stolen, special liability protections apply to prevent the cardholder from being held responsible for unauthorized transactions.

## Section 2: Cardholder Liability Limits

### Section 2.1: Pre-Report Transactions
If a card is reported as lost or stolen BEFORE unauthorized transactions occur:
- Cardholder has ZERO liability
- All unauthorized charges must be reversed immediately
- No investigation required if reported promptly

### Section 2.2: Post-Report Transactions
If unauthorized transactions occur AFTER the card is reported lost/stolen:
- Cardholder has ZERO liability
- Merchant liable for accepting reported stolen card
- Approve refund automatically

### Section 2.3: Pre-Report Transactions (Before Notification)
If unauthorized transactions occur BEFORE card is reported:
- Cardholder liable for maximum $50 (US regulation)
- In practice, Mastercard Zero Liability typically applies
- Liability waived if cardholder reports within 2 business days

## Section 3: Required Documentation
To process a lost/stolen card claim:
1. Police report (recommended but not required)
2. Affidavit of unauthorized use (required)
3. Timeline of when card was lost
4. List of recognized vs unrecognized transactions

## Section 4: Processing Timeline
- Temporary credit: Within 1-2 business days
- Investigation period: Up to 90 days
- Final resolution: Credit becomes permanent if investigation confirms fraud

## Section 5: Common Scenarios

### Scenario A: Card stolen March 1, transaction March 3, reported March 3
**Resolution:** APPROVE refund. Card reported same day as dispute, zero liability applies.

### Scenario B: Card stolen March 1, transaction March 2, reported March 5
**Resolution:** APPROVE refund. Even though reported after transaction, within 2-day window, zero liability applies.

### Scenario C: Card stolen March 1, transaction March 2, reported March 15
**Resolution:** REVIEW. Outside 2-day window, evaluate circumstances. Usually approve under Zero Liability policy.
"""
    },
    
    {
        "policy_id": "MCD-2100",
        "policy_name": "Fraudulent Transaction Processing",
        "category": "Fraud Protection",
        "content": """
# MCD-2100: Fraudulent Transaction Processing

## Section 1: Definition of Fraud
A transaction is considered fraudulent when:
- Cardholder did not authorize the transaction
- Card was used without cardholder's knowledge
- Transaction was made with counterfeit or altered card
- Card details were used in card-not-present fraud

## Section 2: Zero Liability Protection

### Section 2.1: Eligibility
Cardholders are eligible for Zero Liability if:
- Cardholder has not been negligent (e.g., didn't share PIN)
- Cardholder reported fraud promptly (within 60 days)
- Account is in good standing
- Not a commercial/business card (different rules apply)

### Section 2.2: Automatic Approval Criteria
Automatically approve fraud claims when:
- Transaction amount < $500
- First fraud claim for this cardholder
- Transaction location doesn't match cardholder's normal pattern
- Transaction occurred outside cardholder's country

## Section 3: Investigation Requirements

### Section 3.1: Expedited Investigation (1-2 days)
For transactions:
- Under $100
- Clearly fraudulent pattern (e.g., multiple rapid transactions)
- Outside cardholder's geographic area

### Section 3.2: Standard Investigation (10-30 days)
For transactions:
- $100 - $1,000
- Requires merchant evidence review
- Pattern analysis needed

### Section 3.3: Extended Investigation (up to 90 days)
For transactions:
- Over $1,000
- Cardholder has history of disputes
- Suspicious circumstances

## Section 4: Evidence Requirements
Collect from cardholder:
1. Written statement of unauthorized use
2. Last authorized transaction date/time
3. List of unauthorized transactions
4. Whether card is still in possession (if yes, likely CNP fraud)

Collect from merchant:
1. Transaction receipt/authorization
2. IP address (for online transactions)
3. Shipping address (for goods)
4. AVS/CVV match results

## Section 5: Common Fraud Patterns

### Pattern A: Card-Not-Present (CNP) Fraud
- Online transactions without physical card
- Often international merchants
- Usually approve cardholder claim if AVS/CVV didn't match

### Pattern B: Counterfeit Card
- Physical transactions with cloned card
- Often in different geographic area
- Check if chip card (harder to counterfeit)

### Pattern C: Account Takeover
- Cardholder's account credentials stolen
- Legitimate card used fraudulently
- Verify if cardholder's email/phone also compromised
"""
    },
    
    {
        "policy_id": "MCD-5250",
        "policy_name": "Item Not Received",
        "category": "Transaction Disputes",
        "content": """
# MCD-5250: Item Not Received Disputes

## Section 1: Overview
When a cardholder pays for goods or services but does not receive them, they may file an "Item Not Received" dispute.

## Section 2: Eligibility Criteria

### Section 2.1: Valid Claims
Cardholder can dispute if:
- Paid for physical goods that were not delivered
- Delivery date has passed
- No delivery tracking shows receipt
- Merchant has not responded to inquiries

### Section 2.2: Invalid Claims
Cannot dispute if:
- Service was provided (use different dispute reason)
- Digital goods delivered to email (not applicable)
- Cardholder refused delivery
- Shipping address was incorrect (cardholder error)

## Section 3: Required Evidence

### From Cardholder:
1. Order confirmation email
2. Expected delivery date
3. Proof of merchant communication (emails/chat logs)
4. Confirmation that item not received

### From Merchant:
1. Shipping/tracking information
2. Delivery confirmation (signature if required)
3. Proof item sent to correct address
4. Communication history with cardholder

## Section 4: Evaluation Criteria

### Section 4.1: Approve Refund If:
- No valid tracking number provided by merchant
- Tracking shows "not delivered" or "returned to sender"
- Delivery to wrong address (merchant error)
- Merchant cannot provide proof of delivery
- Item marked "delivered" but cardholder has proof of absence (e.g., vacation)

### Section 4.2: Deny Refund If:
- Tracking shows delivered with signature
- Photo proof of delivery at correct address
- Cardholder signed for package
- Cardholder's household member received

### Section 4.3: Escalate If:
- Tracking shows "delivered" but no signature
- Delivery photo is unclear
- Conflicting evidence from both parties
- High-value item (>$1,000) with disputed delivery

## Section 5: Special Circumstances

### Section 5.1: Package Theft (Porch Pirates)
- If item delivered to correct address but stolen, generally NOT merchant's fault
- Liability falls on shipping carrier or homeowner's insurance
- Merchant may offer goodwill replacement but not required
- **Deny dispute** but suggest filing claim with carrier

### Section 5.2: COVID-19 Delivery Delays
- Extended delivery times due to pandemic
- If item still in transit but delayed, **DEFER** dispute
- Give merchant additional 30 days
- Approve if no delivery after extended period

### Section 5.3: International Shipments
- Customs delays common
- Check customs tracking
- Allow 60-90 days for international delivery
- Approve if no delivery after reasonable time + customs clearance
"""
    },
    
    {
        "policy_id": "MCD-5260",
        "policy_name": "Item Not As Described",
        "category": "Transaction Disputes",
        "content": """
# MCD-5260: Item Not As Described Disputes

## Section 1: Overview
When received goods differ materially from merchant's description, cardholder may dispute.

## Section 2: Valid vs Invalid Claims

### Section 2.1: Valid "Not As Described" Claims:
- Item is different model/version than advertised
- Material defect not disclosed (e.g., broken, damaged)
- Counterfeit goods when authentic promised
- Significantly different quality than shown
- Missing major features advertised

### Section 2.2: Invalid Claims (Buyer's Remorse):
- Cardholder changed mind
- Didn't like color/style (subjective preference)
- Found cheaper elsewhere
- Ordered wrong size (cardholder error)
- Item matches description but expectations differed

## Section 3: Evidence Requirements

### From Cardholder:
1. Original product listing/description screenshots
2. Photos of actual received item
3. Proof of return attempt (if merchant has return policy)
4. Communication with merchant about issue

### From Merchant:
1. Original product listing
2. Photos of item as shipped
3. Return policy
4. Proof cardholder didn't attempt return

## Section 4: Resolution Guidelines

### Section 4.1: Approve If:
- Clear material difference (photos show obvious discrepancy)
- Counterfeit item confirmed
- Merchant description was misleading
- Merchant refuses reasonable return

### Section 4.2: Deny If:
- Item matches description
- Subjective opinion (color slightly different, etc.)
- Merchant has accepted return but cardholder refuses
- Cardholder didn't contact merchant first

### Section 4.3: Partial Refund Scenarios:
- Minor defect but item usable → Offer 20-50% partial refund
- Missing accessory → Refund value of missing item
- Lower quality than described → 30-40% partial refund

## Section 5: Special Product Categories

### Section 5.1: Electronics
- Must match advertised specifications
- If refurbished sold as new → APPROVE full refund
- If lower specs than advertised → APPROVE
- If cosmetic damage only → Offer partial (10-20%)

### Section 5.2: Clothing/Apparel
- Size discrepancy from size chart → APPROVE
- Color variation from website → Usually DENY (lighting differences common)
- Material different than stated → APPROVE
- "Fits weird" → DENY (subjective)

### Section 5.3: Collectibles/Vintage
- Condition must match description
- If listed "excellent" but arrives damaged → APPROVE
- Age-appropriate wear → Usually DENY
- Authentication issues → APPROVE + report merchant
"""
    },
    
    {
        "policy_id": "MCD-6100",
        "policy_name": "Canceled Recurring Transaction",
        "category": "Subscription Disputes",
        "content": """
# MCD-6100: Canceled Recurring Transaction Disputes

## Section 1: Overview
When cardholder cancels a subscription but continues to be charged.

## Section 2: Cancellation Requirements

### Section 2.1: Valid Cancellation Methods:
- Written cancellation confirmation from merchant
- Email confirmation of cancellation
- Screenshot of account showing "canceled" status
- Certified mail receipt (for traditional services)

### Section 2.2: Invalid Cancellation Claims:
- Cardholder "intended to cancel" but never did
- Assumed cancellation (e.g., stopped using service)
- Forgot to cancel before renewal
- Missed cancellation deadline stated in terms

## Section 3: Processing Guidelines

### Section 3.1: Approve Refund If:
- Cardholder has cancellation confirmation dated BEFORE charge
- Merchant terms violated (e.g., charged after free trial despite cancellation)
- Cancellation process was unavailable/broken
- Multiple charges after valid cancellation

### Section 3.2: Deny Refund If:
- No proof of cancellation
- Cancellation after charge already processed
- Terms clearly state charge would occur (e.g., annual renewal auto-charge)
- Cardholder had access to service during charged period

### Section 3.3: Partial Refund Scenarios:
- Canceled mid-billing cycle → Prorated refund for unused time
- Charged for annual when monthly was expected → Refund difference

## Section 4: Common Subscription Scenarios

### Scenario A: Streaming Services (Netflix, Spotify, etc.)
- Usually easy to cancel in app/website
- If cardholder shows canceled status but charged → APPROVE
- If "forgot to cancel" before renewal → DENY
- Free trial converted to paid despite cancellation → APPROVE

### Scenario B: Gym Memberships
- Often require in-person or certified mail cancellation
- Check merchant's stated cancellation policy
- If cardholder followed policy but still charged → APPROVE
- If cardholder tried to cancel by stopping payment → DENY

### Scenario C: Software/SaaS
- Check if cardholder had access during disputed period
- If access was active → DENY (services were available)
- If access terminated but charged → APPROVE
- Annual renewals: Check if renewal notice sent

## Section 5: Special Considerations

### Section 5.1: "Difficult to Cancel" Patterns
If merchant makes cancellation unreasonably difficult:
- No clear cancellation method → APPROVE dispute
- Requires phone call during limited hours → Review case by case
- Charges cancellation fee not disclosed → APPROVE + warn merchant

### Section 5.2: Auto-Renewal Notices
Merchants must provide advance notice of auto-renewal:
- 30 days notice standard
- If no notice sent → APPROVE refund
- If notice sent but to old email → Usually DENY (cardholder's responsibility to update)
"""
    },
    
    {
        "policy_id": "MCD-6200",
        "policy_name": "Duplicate Processing",
        "category": "Transaction Errors",
        "content": """
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
"""
    },
    
    {
        "policy_id": "MCD-6300",
        "policy_name": "Incorrect Transaction Amount",
        "category": "Transaction Errors",
        "content": """
# MCD-6300: Incorrect Amount Disputes

## Section 1: Overview
When cardholder is charged a different amount than agreed upon or expected.

## Section 2: Valid Amount Dispute Scenarios

### Section 2.1: Pricing Errors:
- Advertised price different from charged amount
- Promotional discount not applied
- Item rang up at wrong price
- Currency conversion error (international)

### Section 2.2: Unauthorized Amount Changes:
- Tip added without authorization (delivery/restaurant)
- Additional fees not disclosed at purchase
- Amount increased after transaction
- Automatic gratuity added without notice

## Section 3: Evidence Requirements

### From Cardholder:
1. Receipt or screenshot showing expected price
2. Advertisement/listing with stated price
3. Photo of price tag (in-store purchases)
4. Email confirmation with different amount

### From Merchant:
1. Itemized receipt
2. Terms of sale (fee disclosures)
3. Proof cardholder authorized amount
4. System pricing records

## Section 4: Resolution Guidelines

### Section 4.1: Approve Partial Refund If:
- Clear pricing error (proof of advertised lower price)
- Unauthorized fees added
- Mathematical error on receipt
- Quantity charged incorrect (charged for 3, bought 1)

**Refund amount:** Difference between charged and correct amount

### Section 4.2: Approve Full Refund If:
- Egregious overcharge (2x or more than expected)
- Merchant refuses to correct clear error
- Fraudulent amount change after transaction

### Section 4.3: Deny If:
- Amount matches receipt cardholder signed
- Fees clearly disclosed in merchant terms
- Cardholder misremembered price
- Exchange rate fluctuation (international, rates vary)

## Section 5: Specific Scenarios

### Section 5.1: Restaurant Tips
- If cardholder didn't authorize tip amount → APPROVE adjustment
- If tip line was blank and merchant added 20% → APPROVE (merchant fraud)
- If cardholder wrote tip but disputes amount → Check receipt signature
- Automatic gratuity (large parties) → Only approve if not disclosed

### Section 5.2: Online Shopping
- If cart showed $100 but charged $120:
  * Check if taxes/shipping added (disclosed?) → Usually DENY
  * If final checkout page showed $100 → APPROVE difference
- Promotional codes not applied → APPROVE if valid code

### Section 5.3: Hotel/Travel
- Resort fees not disclosed → APPROVE removal
- Minibar/incidentals → Must have itemized proof
- Room rate different than booking → APPROVE if booking confirmation shows lower rate

### Section 5.4: Currency Conversion
- International transactions may show different amount due to exchange rates
- If DCC (Dynamic Currency Conversion) used without consent → APPROVE
- Exchange rate disputes → Check if rate reasonable (within 3% of market rate)

## Section 6: Calculation Examples

**Example 1: Promotional Price**
- Advertised: $79.99 (50% off)
- Charged: $159.99 (full price)
- **Resolution:** APPROVE $80 refund (bring to advertised price)

**Example 2: Tax Added**
- Cart showed: $100
- Charged: $108 (with tax)
- **Resolution:** DENY if tax clearly stated at checkout, APPROVE if hidden

**Example 3: Quantity Error**
- Ordered: 1 item at $50
- Charged: $150 (3x $50)
- **Resolution:** APPROVE $100 refund (charged for 3, only ordered 1)
"""
    },
    
    {
        "policy_id": "MCD-1000",
        "policy_name": "Zero Liability Protection Policy",
        "category": "Cardholder Rights",
        "content": """
# MCD-1000: Mastercard Zero Liability Protection

## Section 1: Policy Overview
Mastercard's Zero Liability Protection ensures cardholders are not held responsible for unauthorized transactions on their Mastercard accounts, provided they meet certain conditions.

## Section 2: Coverage

### Section 2.1: What's Covered
- Card-present transactions (in-store) made without authorization
- Card-not-present transactions (online, phone, mail order)
- Lost or stolen card transactions
- Counterfeit card transactions
- Account takeover fraud

### Section 2.2: What's NOT Covered
- Commercial/business cards (different policy applies)
- Transactions where PIN was used (PIN-based transactions)
- Gross negligence (e.g., writing PIN on card)
- Transactions reported >60 days after statement date

## Section 3: Eligibility Requirements

### Section 3.1: Cardholder Must:
1. Report unauthorized transaction within 60 days of statement
2. Not have been grossly negligent with card security
3. Have account in good standing (not abusing dispute process)
4. Cooperate with fraud investigation

### Section 3.2: Automatic Qualification
Zero Liability automatically applies to:
- Consumer credit cards
- Consumer debit cards (check if bank has opted in)
- Prepaid cards (most Mastercard prepaid)

## Section 4: Processing Guidelines

### Section 4.1: Immediate Provisional Credit
For transactions under $500:
- Issue provisional credit within 1-2 business days
- No wait for investigation
- Zero Liability assumed

For transactions $500-$5,000:
- Issue credit within 5 business days
- Standard investigation timeline

For transactions >$5,000:
- May require completed investigation
- Consider provisional credit based on history

### Section 4.2: Investigation Process
Even with Zero Liability, still investigate to:
- Identify fraud patterns
- Protect against future fraud
- Recover funds from fraudster
- Update security measures

## Section 5: Exceptions and Special Cases

### Section 5.1: PIN Transactions
If PIN was used:
- Zero Liability may NOT apply (depends on bank policy)
- Assume cardholder authorized unless proven card was physically stolen
- Higher burden of proof for cardholder

### Section 5.2: Family Fraud
If family member used card:
- Technically not "unauthorized" in legal sense
- Zero Liability may not apply
- Review case by case, consider domestic circumstances

### Section 5.3: Gross Negligence
Zero Liability void if:
- Cardholder wrote PIN on card
- Gave card to someone else willingly
- Left card unattended in public
- Shared account credentials on phishing site

## Section 6: Communication Requirements

### Section 6.1: Merchant Communication
If merchant provides evidence cardholder authorized:
- Review evidence carefully
- If strong evidence (signature, video, etc.) → May deny claim
- If weak evidence → Uphold Zero Liability

### Section 6.2: Cardholder Communication
Must inform cardholder:
- Zero Liability protection exists
- How to report fraud quickly
- Provisional credit timeline
- Investigation process

## Section 7: Common Scenarios

**Scenario A:** Online purchase, cardholder denies making it, no suspicious account activity
- **Resolution:** APPROVE. Zero Liability applies to CNP fraud.

**Scenario B:** In-store purchase with signature, cardholder claims card stolen
- **Resolution:** APPROVE. Card theft covered by Zero Liability. Merchant should have checked ID.

**Scenario C:** Cardholder shared Netflix password, account used for fraud
- **Resolution:** REVIEW. Negligence claim. May deny if cardholder shared credentials.

**Scenario D:** Child used parent's card without permission
- **Resolution:** DENY. Family member use typically not covered, advise cardholder it's a civil matter.
"""
    },
    
    {
        "policy_id": "MCD-7000",
        "policy_name": "Documentation Requirements",
        "category": "Processing Guidelines",
        "content": """
# MCD-7000: Documentation Requirements for Dispute Processing

## Section 1: Overview
Proper documentation is critical for fair and accurate dispute resolution.

## Section 2: Standard Documentation Required

### Section 2.1: From Cardholder (Always Required):
1. **Written dispute statement**
   - Description of issue in cardholder's words
   - Date of discovery
   - What resolution is sought

2. **Account information**
   - Last 4 digits of card
   - Transaction date and amount
   - Merchant name

3. **Contact information**
   - Current phone and email
   - Preferred contact method

### Section 2.2: Dispute-Specific Documentation

**For Fraud/Unauthorized Transactions:**
- Statement that transaction was not authorized
- Date card was lost/stolen (if applicable)
- Last transaction cardholder DID authorize
- Whether card is still in possession

**For Item Not Received:**
- Order confirmation
- Expected delivery date
- Tracking number (if provided by merchant)
- Proof of merchant contact attempts

**For Item Not As Described:**
- Product listing screenshot
- Photos of received item
- Description of discrepancy
- Proof of return attempt (if applicable)

**For Canceled Recurring:**
- Cancellation confirmation email/screenshot
- Date of cancellation
- Merchant's stated cancellation policy
- Number of charges after cancellation

## Section 3: Merchant Documentation

### Section 3.1: Merchant Must Provide:
1. **Transaction receipt**
2. **Delivery confirmation** (for goods)
3. **Communication with cardholder** (if any)
4. **Terms of sale** (relevant sections)

### Section 3.2: Enhanced Documentation (High-Value >$1,000):
- AVS/CVV results (online transactions)
- IP address logs
- Device fingerprinting data
- Video surveillance (in-store, if available)
- Signed delivery receipt

## Section 4: Quality Standards

### Section 4.1: Acceptable Documentation:
✅ Clear, legible photos/scans
✅ Unaltered screenshots
✅ Official correspondence (emails from official domains)
✅ Timestamped evidence
✅ Third-party verification (tracking numbers, police reports)

### Section 4.2: Unacceptable Documentation:
❌ Blurry/illegible images
❌ Clearly edited/photoshopped evidence
❌ Hearsay ("My friend said...")
❌ Screenshots without context
❌ Expired evidence (e.g., broken tracking link)

## Section 5: Insufficient Documentation Handling

### Section 5.1: Request Additional Info:
- Give cardholder 10 business days to provide
- Be specific about what's needed
- Provide examples if helpful

### Section 5.2: Processing Without Full Documentation:
**Can proceed without full docs if:**
- Clear-cut case (e.g., obvious fraud pattern)
- Merchant provides no rebuttal
- Small amount (<$50)

**Must have full docs for:**
- High-value disputes (>$1,000)
- Cardholder has dispute history
- Conflicting evidence

## Section 6: Documentation Timeline

### Section 6.1: Cardholder Submission:
- Initial claim: 60 days from statement date
- Additional documentation: 10 business days after request

### Section 6.2: Merchant Response:
- Standard: 30 days
- Expedited (fraud): 5-10 business days
- Extensions granted on request (valid reason)

## Section 7: Privacy and Redaction

### Section 7.1: Information to Redact:
When sharing documentation between parties:
- Full card numbers (show last 4 only)
- CVV/security codes
- Full SSN (show last 4 only)
- Sensitive personal info unrelated to dispute

### Section 7.2: Information to Keep:
- Transaction details
- Relevant correspondence
- Shipping information
- Evidence of purchase/delivery
"""
    },
    
    {
        "policy_id": "MCD-7100",
        "policy_name": "Time Limits and Deadlines",
        "category": "Processing Guidelines",
        "content": """
# MCD-7100: Dispute Time Limits and Deadlines

## Section 1: Cardholder Dispute Filing Deadlines

### Section 1.1: Standard Disputes
- **Filing deadline:** 60 days from transaction statement date
- **Exception:** Can extend to 120 days if:
  * Fraud was discovered later
  * Recurring charges (each charge has its own 60-day window)
  * Item delivery date was delayed

### Section 1.2: Special Circumstance Extensions

**Fraud/Unauthorized Transactions:**
- No hard deadline (regulatory protection)
- Best practice: File within 60 days
- After 60 days: Burden of proof increases

**Item Not Received:**
- Can wait until expected delivery date passes
- Then 60 days from expected delivery
- Maximum 540 days from transaction date

**Recurring Subscriptions:**
- Each charge has independent 60-day window
- Can dispute pattern of charges together
- If systemic issue: All related charges in one dispute

## Section 2: Processing Time Limits

### Section 2.1: Initial Review and Provisional Credit
- **Acknowledgment:** Within 24-48 hours of receipt
- **Provisional credit:** 
  * Fraud: 1-2 business days
  * Quality dispute: 5-10 business days
  * High-value: May wait for investigation

### Section 2.2: Investigation Timeline

**Expedited (fraud, clear-cut):**
- Investigation: 5-10 business days
- Final decision: 10-15 business days

**Standard:**
- Investigation: 30-45 days
- Final decision: 45-60 days

**Complex (high-value, conflicting evidence):**
- Investigation: 60-90 days
- Final decision: Up to 90 days

## Section 3: Merchant Response Deadlines

### Section 3.1: Standard Response Time:
- Merchant has **30 days** to respond to dispute notification
- Can request extension (up to 60 days total) with valid reason

### Section 3.2: Expedited Response (Fraud Claims):
- Merchant has **10 days** to respond
- If no response: Automatic approval of cardholder claim

### Section 3.3: No Response Consequences:
- After deadline: Merchant forfeits ability to contest
- Chargeback automatically processed
- Merchant may be liable for fees

## Section 4: Chargeback Reversal (Merchant Wins) Timeline

### Section 4.1: If Merchant Provides Compelling Evidence:
- Review evidence: 10-15 days
- Decision communicated: Within 5 days of decision
- Reversal processed: 3-5 business days

### Section 4.2: Cardholder Appeal (Second Chargeback):
- Cardholder has 30 days to appeal reversal
- Must provide new evidence or refute merchant evidence
- Second investigation: 30-60 days

## Section 5: Special Timing Rules

### Section 5.1: Holiday/Weekend Handling:
- Deadlines falling on weekend/holiday → Next business day
- "Business days" = Monday-Friday, excluding bank holidays
- International: Consider both cardholder and merchant country holidays

### Section 5.2: Multiple Disputes:
If cardholder files multiple related disputes:
- Can be consolidated into single case
- Deadline = earliest dispute filing date
- Processing time may extend to 90 days for complexity

### Section 5.3: Recurring Investigations:
If same cardholder-merchant pair has multiple disputes:
- May flag for pattern review
- Each dispute processed independently
- But pattern may inform decisions

## Section 6: Statute of Limitations

### Section 6.1: Hard Deadlines:
- **Fraud:** No limitation (criminal matter)
- **Civil disputes:** 540 days maximum from transaction
- **Recurring charges:** 540 days from LAST charge

### Section 6.2: Record Retention:
- Keep dispute records: 7 years minimum
- Transaction records: 7 years
- Fraud investigations: Indefinite (may be needed for law enforcement)

## Section 7: Common Timing Scenarios

**Scenario A:** Transaction Jan 1, Statement Jan 31, Dispute Filed March 31
- **Status:** Within 60-day window from statement (Jan 31 + 60 = April 1). ACCEPT.

**Scenario B:** Transaction Jan 1, Statement Jan 31, Dispute Filed May 15
- **Status:** Outside 60-day window. ACCEPT if fraud, DENY if quality dispute.

**Scenario C:** Subscription charged Jan 1, Feb 1, Mar 1. Cancel attempt Feb 15. Dispute filed April 5 for all three.
- **Status:** 
  * Jan charge: Outside 60-day window from Jan statement - DENY
  * Feb charge: Within window - ACCEPT
  * Mar charge: Within window - ACCEPT

**Scenario D:** Item shipped Jan 1, expected delivery Jan 10, not received. Dispute filed Feb 20.
- **Status:** Within reasonable window (expected delivery + 40 days). ACCEPT.
"""
    },

    {
        "policy_id": "MCD-8000",
        "policy_name": "International Transaction Rules",
        "category": "Special Circumstances",
        "content": """
# MCD-8000: International Transaction Dispute Rules

## Section 1: Overview
International transactions involve additional complexity: currency conversion, shipping delays, customs, and cross-border regulations.

## Section 2: Currency Conversion Disputes

### Section 2.1: Dynamic Currency Conversion (DCC)
- Merchant offers to charge in cardholder's home currency
- Rate may be unfavorable vs. Mastercard's rate
- **If DCC used without consent:** APPROVE reversal to Mastercard rate
- **If cardholder chose DCC:** DENY, it was their choice

### Section 2.2: Exchange Rate Disputes
- Mastercard sets daily exchange rates
- Rate varies from transaction date to posting date
- Typical variance: 1-3% is normal
- **If variance >5%:** Investigate for error, may approve adjustment
- **If variance <5%:** DENY, normal fluctuation

### Section 2.3: Foreign Transaction Fees
- Bank may charge 1-3% foreign transaction fee
- This is SEPARATE from amount dispute
- Fee disputes = contact bank, not merchant
- Only approve fee dispute if fee not disclosed

## Section 3: International Shipping Disputes

### Section 3.1: Extended Delivery Times
Normal international delivery windows:
- Canada/Mexico: 10-15 business days
- Europe: 15-25 business days
- Asia/Australia: 20-30 business days
- Africa/South America: 25-35 business days

**Processing Rule:** Do not approve "Item Not Received" until reasonable delivery window + 14 days

### Section 3.2: Customs Delays
- Customs can hold packages 7-60 days
- Not merchant's fault
- Defer dispute until customs clearance or 90 days (whichever first)
- If customs seizes item (prohibited): Usually merchant's fault → APPROVE

### Section 3.3: Import Fees/Duties
- Cardholder may owe customs duties separate from purchase
- If duties not disclosed by merchant → May approve dispute
- If duties clearly stated → DENY, cardholder's responsibility

## Section 4: Jurisdiction and Law Considerations

### Section 4.1: Applicable Law
When cardholder and merchant in different countries:
- Mastercard rules supersede local laws (usually)
- EU consumer protection: Very strong, favor cardholder
- Some countries restrict chargeback rights: Case-by-case

### Section 4.2: Language Barriers
- Merchant communication in different language
- Use translation services
- Cardholder cannot claim "didn't understand" if clear translation available
- If terms only in foreign language with no translation: Favor cardholder

## Section 5: Common International Scenarios

### Scenario A: AliExpress/International Marketplace
- Long shipping times expected (30-60 days)
- Item descriptions may be unclear (translation issues)
- **Item Not Received:** Wait 60 days before approving
- **Item Not As Described:** Photos are key evidence, approve if clear discrepancy

### Scenario B: European Merchants (Strong Consumer Protection)
- EU has 14-day return right by law
- If merchant doesn't honor: APPROVE chargeback
- May require cardholder to return item first

### Scenario C: Vacation/Travel Purchases
- Currency conversion disputes common
- Check if DCC was offered and chosen
- Resort fees in other countries: Check if disclosed
- Typical rule: If clearly disclosed → DENY

## Section 6: Cross-Border Fraud Patterns

### Section 6.1: High-Risk Countries
Certain countries have higher fraud rates:
- If transaction from high-risk country + cardholder denies: APPROVE quickly
- Enhanced verification for merchants in these regions
- Common pattern: Fake online stores in Eastern Europe/Asia

### Section 6.2: Travel Fraud
- Cardholder travels, card used in visited country, claims unauthorized
- Compare transaction dates to travel dates
- If overlap: May DENY (cardholder likely made purchase)
- If transaction after return home: Fraud more likely → APPROVE

## Section 7: Special International Rules

### Section 7.1: Timezones
- Transaction timestamp may differ from cardholder's timezone
- 24-hour difference common across Pacific
- Use UTC for official timestamps
- Don't penalize for timezone confusion

### Section 7.2: International Merchants No Longer Operating
- Merchant went out of business (common with small international sellers)
- Cannot get merchant response
- If legitimate purchase claim: May need to deny (goods received)
- If fraud/not received: Approve after reasonable attempt to contact

### Section 7.3: Sanctions and Restricted Countries
- If transaction with merchant in sanctioned country: Flag immediately
- May be illegal transaction
- Approve chargeback + report to compliance
- Cardholder may face investigation
"""
    },

    {
        "policy_id": "MCD-8100",
        "policy_name": "High-Value Transaction Rules",
        "category": "Special Circumstances",
        "content": """
# MCD-8100: High-Value Transaction Dispute Processing

## Section 1: Definition of High-Value

### Section 1.1: Thresholds
- **Enhanced Review:** $1,000 - $5,000
- **High-Value:** $5,000 - $25,000
- **Ultra-High-Value:** $25,000+

Different procedures apply at each tier.

## Section 2: Enhanced Documentation Requirements

### Section 2.1: Required Evidence for High-Value Claims

**From Cardholder:**
1. All standard documentation (MCD-7000)
2. Additional identity verification
3. Police report (for fraud claims >$5,000)
4. Notarized affidavit (for fraud claims >$10,000)
5. Proof of legitimate purchase capability (bank statements showing funds)

**From Merchant:**
1. All standard documentation
2. Enhanced delivery proof:
   - Signature required delivery
   - Photo of recipient with ID
   - GPS coordinates of delivery
3. AVS, CVV, 3D Secure results (online transactions)
4. Communication history with cardholder
5. Invoice and receipt
6. For luxury goods: Certificate of authenticity

## Section 3: Investigation Procedures

### Section 3.1: Enhanced Investigation ($1,000 - $5,000)
- Assigned to senior dispute analyst
- Timeline: 45-60 days (longer than standard)
- May include:
  * Third-party fraud verification
  * Address verification
  * Phone verification with cardholder
  * Review of account history

### Section 3.2: High-Value Investigation ($5,000 - $25,000)
- Assigned to specialist team
- Timeline: 60-90 days
- May include:
  * Law enforcement coordination
  * Forensic analysis
  * Site visit (for merchants)
  * Expert review (e.g., authenticator for luxury goods)

### Section 3.3: Ultra-High-Value ($25,000+)
- Executive review required
- Timeline: 90-120 days
- May include:
  * Private investigator
  * Legal team consultation
  * Mastercard corporate involvement
  * Possible criminal investigation referral

## Section 4: Provisional Credit Rules

### Section 4.1: Standard High-Value Processing
**$1,000 - $5,000:**
- Provisional credit: 5-10 business days
- Full investigation before final decision

**$5,000 - $25,000:**
- Provisional credit: After preliminary investigation (10-15 days)
- May be withheld pending fraud review

**$25,000+:**
- Provisional credit: Generally withheld until investigation complete
- Exception: Clear fraud with strong evidence

## Section 5: Special Verification Steps

### Section 5.1: Cardholder Verification
For high-value disputes, verify:
1. **Identity Confirmation:**
   - Government-issued ID
   - Match to account holder
   - Video call verification (for ultra-high-value)

2. **Transaction Authorization:**
   - Was cardholder capable of making this purchase?
   - Do they normally make purchases of this size?
   - What was the stated purpose?

3. **Fraud Indicators:**
   - Is account new?
   - Pattern of high-value disputes?
   - Recent address changes?

### Section 5.2: Merchant Verification
For high-value disputes, verify merchant:
1. **Business Legitimacy:**
   - How long in business?
   - Reputation (BBB, reviews)
   - Physical location exists?

2. **Transaction Legitimacy:**
   - Is this normal for this merchant?
   - Do they typically sell high-value items?
   - Proper security measures taken?

## Section 6: Common High-Value Scenarios

### Scenario A: Luxury Goods (Jewelry, Watches, Designer Items)
**Key Issues:**
- Counterfeits common
- Authentication critical
- Return fraud (return fake, keep real)

**Processing:**
- Require authentication certificate
- Photos of serial numbers
- If "not as described" → Expert authenticator review
- If approved: Require return for inspection before refund

### Scenario B: Electronics (Laptops, Cameras, etc.)
**Key Issues:**
- Return fraud (return broken item, claim arrived that way)
- Buyer's remorse common
- Specifications disputes

**Processing:**
- Check merchant's return policy first
- Require proof of defect (photos, videos)
- For "not as described": Compare specs carefully
- May approve partial refund vs full

### Scenario C: Travel Packages, Timeshares
**Key Issues:**
- High-pressure sales
- Misrepresented amenities
- Cancellation fee disputes

**Processing:**
- Review sales materials vs what was delivered
- Check consumer protection laws (strong for timeshares)
- If misrepresented: Usually APPROVE
- If buyer's remorse: Check cooling-off period laws

### Scenario D: Medical Procedures (International)
**Key Issues:**
- Complications
- Results not as promised
- Non-refundable deposits

**Processing:**
- Difficult disputes (services already rendered)
- If procedure not performed: APPROVE
- If complications: Not merchant's fault usually → DENY
- If misrepresented: May approve partial

## Section 7: Fraud Prevention Flags

### Section 7.1: High-Risk Patterns
Automatically flag for enhanced review if:
- First transaction on account >$5,000
- Multiple high-value transactions in short period
- High-value transaction shortly after address change
- Purchase inconsistent with account history
- Shipping address differs from billing (high-value)

### Section 7.2: Merchant Fraud Indicators
- New merchant with high-value transactions
- Merchant rushes shipping before fraud checks
- Merchant in high-risk country
- Merchant has high dispute rate

## Section 8: Settlement and Recovery

### Section 8.1: Chargeback Amounts
- For high-value chargebacks, merchant may face:
  * Chargeback amount
  * Chargeback fee ($25-$100)
  * Potential account penalties
  * Possible termination (if pattern)

### Section 8.2: Recovery Attempts
For ultra-high-value fraud:
- Work with law enforcement
- May pursue civil recovery
- Mastercard fraud database reporting
- Possible criminal prosecution referral

## Section 9: Escalation and Appeals

### Section 9.1: Cardholder Appeal Rights
If high-value claim denied:
- Cardholder can appeal within 30 days
- Must provide new evidence
- Executive review of appeal
- Final decision binding

### Section 9.2: Merchant Pre-Arbitration
For high-value chargebacks:
- Merchant can request arbitration
- Costs: $500+ (merchant pays if loses)
- Timeline: Additional 60-90 days
- Arbitration is final and binding
"""
    },

    {
        "policy_id": "MCD-9000",
        "policy_name": "Quality Assurance and Best Practices",
        "category": "Internal Guidelines",
        "content": """
# MCD-9000: Quality Assurance and Best Practices for Dispute Resolution

## Section 1: Decision-Making Framework

### Section 1.1: The Three-Step Approach
Every dispute should follow this process:

**Step 1: Gather Facts**
- Review all available documentation
- Check transaction details
- Verify account history
- Contact parties if needed

**Step 2: Apply Policy**
- Identify applicable policies
- Check for special circumstances
- Consider precedent
- Evaluate evidence quality

**Step 3: Make Fair Decision**
- Balance cardholder and merchant rights
- Document reasoning
- Ensure consistency
- Consider impact

### Section 1.2: When in Doubt
If unclear which way to decide:
1. **Check similar cases** - How were they resolved?
2. **Consult senior analyst** - Get second opinion
3. **Default to cardholder** - Consumer protection bias
4. **Document uncertainty** - Note for future training

## Section 2: Common Decision Errors to Avoid

### Section 2.1: Error: Automatic Denial
**Problem:** Auto-denying based on one factor
**Example:** "No receipt, so deny"
**Fix:** Look at full picture. Other evidence may suffice.

### Section 2.2: Error: Emotional Decision
**Problem:** Letting sympathy/frustration influence decision
**Example:** "This poor cardholder has been scammed so much, I'll approve even though evidence is weak"
**Fix:** Stick to policy. Empathy is good, but fairness requires objectivity.

### Section 2.3: Error: Ignoring Merchant Rights
**Problem:** Always favoring cardholder
**Example:** Approving dispute when merchant clearly followed rules
**Fix:** Merchants have rights too. If they did everything right, uphold the transaction.

### Section 2.4: Error: Insufficient Investigation
**Problem:** Deciding too quickly without full information
**Example:** Approving fraud claim without checking if cardholder's family member used card
**Fix:** Take time to investigate. Rush decisions lead to errors.

### Section 2.5: Error: Over-Complicating
**Problem:** Creating reasons to deny clear-cut cases
**Example:** "Well technically the cardholder could have..."
**Fix:** If it's straightforward, decide straightforwardly.

## Section 3: Quality Metrics

### Section 3.1: Decision Quality Targets
- **Accuracy:** 95%+ (measured by appeals upheld/overturned)
- **Consistency:** Same scenarios decided same way 90%+ of time
- **Timeliness:** 95% within SLA timeframes
- **Documentation:** 100% of decisions documented

### Section 3.2: Red Flags for Quality Review
Auto-flag cases for QA if:
- High-value (>$5,000)
- Complex multi-party dispute
- Overturned on appeal previously
- Cardholder has high dispute frequency
- New analyst handling unusual case type

## Section 4: Communication Best Practices

### Section 4.1: With Cardholders
**DO:**
- Use clear, simple language
- Explain decision and reasoning
- Provide timeline expectations
- Offer alternatives when denying
- Be empathetic to frustration

**DON'T:**
- Use jargon or policy numbers without explanation
- Make promises you can't keep
- Blame other departments
- Be defensive
- Provide legal advice

### Section 4.2: With Merchants
**DO:**
- Be professional and factual
- Clearly state what evidence is needed
- Provide adequate time to respond
- Acknowledge good documentation
- Explain decision basis

**DON'T:**
- Take sides with cardholder
- Make accusations
- Share cardholder's personal information unnecessarily
- Be condescending

## Section 5: Edge Cases and Gray Areas

### Section 5.1: Family Disputes
**Scenario:** Adult child used parent's card without permission
**Approach:**
- Technically unauthorized
- But family civil matter
- Usually DENY but educate
- May approve if elder abuse suspected

### Section 5.2: "Buyer's Remorse" vs Legitimate Issue
**Scenario:** Cardholder changed mind but claims item defective
**Approach:**
- Look for inconsistencies in story
- Check timing (immediate complaint vs weeks later)
- Review merchant return policy
- If clearly buyer's remorse → DENY + educate
- If genuine defect → APPROVE

### Section 5.3: Merchant Goodwill Refunds
**Scenario:** Merchant already issued refund, cardholder also disputed
**Approach:**
- Check if refund processed
- If yes → Close dispute as resolved
- If pending → Wait for confirmation
- Prevent double refund

## Section 6: Continuous Improvement

### Section 6.1: Learning from Appeals
- Track all overturned decisions
- Quarterly review of patterns
- Update training based on common errors
- Share learnings across team

### Section 6.2: Policy Updates
- Monitor for policy gaps
- Suggest updates based on emerging patterns
- Stay current on regulation changes
- Industry best practice review

### Section 6.3: Technology Use
- Leverage automation for routine checks
- Use AI to flag suspicious patterns
- But always human final decision on complex cases
- Technology assists, doesn't replace judgment

## Section 7: Ethical Guidelines

### Section 7.1: Conflicts of Interest
- Disclose if you know cardholder/merchant
- Recuse yourself from family/friend disputes
- No gifts or favors from merchants
- Report unethical behavior

### Section 7.2: Data Privacy
- Access customer data only as needed
- Never share data outside secure systems
- Follow data retention policies
- Report breaches immediately

### Section 7.3: Fairness Commitment
- Treat all parties with respect
- Apply policies consistently
- No discrimination based on protected characteristics
- Advocate for fair policies
"""
    },
]

# Write each policy to a file
for policy in POLICIES:
    filename = f"policies/{policy['policy_id']}_{policy['policy_name'].replace('/', '_').replace(' ', '_')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(policy['content'])
    
    print(f"✅ Created: {filename}")

# Also create a JSON index
with open("policies/policy_index.json", 'w', encoding='utf-8') as f:
    policy_index = [
        {
            "policy_id": p["policy_id"],
            "policy_name": p["policy_name"],
            "category": p["category"],
            "filename": f"{p['policy_id']}_{p['policy_name'].replace('/', '_').replace(' ', '_')}.md"
        }
        for p in POLICIES
    ]
    json.dump(policy_index, f, indent=2)

print("\n" + "="*60)
print(f"✅ Created {len(POLICIES)} policy documents")
print("✅ Created policy_index.json")
print("="*60)