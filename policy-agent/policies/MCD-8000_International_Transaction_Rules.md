
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
