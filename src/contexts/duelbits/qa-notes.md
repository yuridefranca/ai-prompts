# QA Notes Generator (Duelbits)

Generates QA handover notes following Duelbits QA team requirements. These notes help QA understand the scope and testing requirements.

**⚠️ CRITICAL**: QA notes are ONLY displayed in the chat for developer reference. They are NEVER added to the PR description.

## Purpose

QA notes provide:
- Technical changes introduced
- Impacted areas/touch points
- Testing considerations and limitations
- Verification evidence

## Guidelines (from Duelbits QA Process)

A good handover from Developer to QA should:

1. **Provide testing environment** including known considerations/limitations
2. **Explain HOW to test** due to environment limitations (not WHAT to test)
3. **Explain details** like toast notifications, features not working yet but expected
4. **For backend tickets**: Show potential tests using API calls or functions on dev
5. **Include verification**: Screenshot or short recording of core change working on preview branch
6. **For Contentful changes**: Link to Contentful development environment

## Generation Process

### Step 1: Identify Technical Changes

Based on changed files and description, categorize:

**Frontend changes**:
- New components created
- Modified components
- State management changes
- API integration changes
- Routing changes

**Backend changes**:
- New endpoints
- Modified endpoints
- Database schema changes
- Service logic changes
- Authentication/authorization changes

**Full-stack changes**:
- Both frontend and backend modifications
- Integration points

### Step 2: Determine Impacted Areas

**Map changes to user-facing features**:

```typescript
function mapToImpactedAreas(changedFiles: string[]): string[] {
  const areas = [];
  
  // Example mapping
  if (changedFiles.some(f => f.includes('wallet'))) {
    areas.push('Wallet functionality');
  }
  
  if (changedFiles.some(f => f.includes('auth'))) {
    areas.push('Authentication/Login');
  }
  
  // ... more mappings
  
  return areas;
}
```

### Step 3: Generate Testing Considerations

**Include**:
- Environment-specific limitations
- Data requirements (e.g., test users, mock data)
- Third-party dependencies that might not work on dev
- Features intentionally not working yet (part of future tickets)

**Example considerations**:
```
- Test on {branchName} preview environment
- Login functionality works, but password reset emails go to console (check logs)
- TOS modal not implemented yet (part of MW-150)
- Use test wallet: 0x1234... for testing transactions
```

### Step 4: Provide Testing Instructions (HOW, not WHAT)

**Focus on environment-specific instructions**:

✅ **Good (HOW)**:
- "Clear site data to simulate logout"
- "Check browser console for password reset link (emails disabled on dev)"
- "Use Postman collection at /docs/api-tests.postman.json"

❌ **Bad (WHAT)**:
- "Test the login functionality"
- "Verify wallet balance displays"
- "Check all payment methods"

### Step 5: Request/Generate Verification Evidence

**Ask developer**:
```
For QA verification, please provide:
- Screenshot of the core functionality working on {branchName} preview
- OR brief screen recording (< 30 seconds) showing the feature

This helps QA confirm the change is deployed before starting tests.

Upload now or add later?
- I'll upload now
- I'll add it to Jira ticket later
- Skip (not applicable)
```

### Step 6: Format QA Notes

**Template**:

```markdown
### QA Handover Notes

**Environment**: {branchName} preview environment
**Link**: {previewUrl if available}

**Technical Changes**:
{List of technical changes in bullet points}

**Impacted Areas**:
{List of user-facing features affected}

**Testing Considerations**:
{Environment limitations and special setup requirements}

**How to Test**:
{Environment-specific instructions for HOW to test}

**Backend Testing** (if applicable):
{API endpoints or functions to test, with examples}

**Contentful Changes** (if applicable):
{Link to Contentful dev environment}

**Verification**:
{Screenshot/recording showing core change working}

**Known Limitations**:
{Features not working yet but expected as part of future work}
```

## Example Outputs

### Example 1: Frontend Feature (Wallet Switcher)

```markdown
### QA Handover Notes

**Environment**: MW-142-wallet-switcher preview environment

**Technical Changes**:
- Created WalletSwitcher component in src/components/wallet/
- Added wallet state management using Zustand
- Integrated with existing WalletProvider
- Updated wallet display in header and sidebar

**Impacted Areas**:
- Wallet selection and display
- User profile page (wallet section)
- Transaction history view
- Deposit/Withdrawal flows

**Testing Considerations**:
- Test with multiple wallet types: MetaMask, WalletConnect, Coinbase Wallet
- Preview environment uses testnet (Goerli)
- Test wallets available in /docs/test-wallets.md

**How to Test**:
- Connect wallet via "Connect Wallet" button
- Add a second wallet using wallet switcher dropdown in header
- Switch between wallets and verify balance updates
- Clear browser local storage to reset wallet connections

**Verification**:
[Screenshot: Wallet switcher dropdown showing 2 connected wallets with balances]

**Known Limitations**:
- Hardware wallet support not included (part of MW-150)
- Wallet nicknames feature coming in MW-145
```

### Example 2: Backend API (Payment Processing Fix)

```markdown
### QA Handover Notes

**Environment**: CORE-456-fix-payment-bug preview environment

**Technical Changes**:
- Fixed race condition in PaymentService.processPayment()
- Added transaction locking mechanism
- Updated payment status validation logic
- Added retry logic for failed webhook deliveries

**Impacted Areas**:
- Payment processing (deposits and withdrawals)
- Transaction status updates
- Webhook delivery to payment providers

**Testing Considerations**:
- Preview environment uses Stripe test mode
- Test card: 4242 4242 4242 4242
- Webhook logs available in admin panel > System > Webhooks

**How to Test**:
Use Postman collection at /docs/api/payment-tests.postman.json

**Backend Testing**:
1. Test concurrent payment processing:
```bash
# Run this function in dev console
curl -X POST https://dev.duelbits.com/api/payments \
  -H "Authorization: Bearer {test_token}" \
  -d '{"amount": 100, "currency": "USD", "method": "card"}'
```

2. Verify webhook retry logic:
   - Trigger payment in UI
   - Check admin panel > Webhooks for retry attempts
   - Failed webhooks should retry 3 times with exponential backoff

**Verification**:
[Screenshot: Admin webhook logs showing successful payment and webhook delivery]

**Known Limitations**:
- None - this is a bug fix
```

### Example 3: Contentful Changes

```markdown
### QA Handover Notes

**Environment**: CAS-789-promo-banner preview environment

**Technical Changes**:
- Added new Contentful content type: "PromoBanner"
- Created promo banner component
- Added banner display logic to homepage

**Impacted Areas**:
- Homepage banner section
- Promo campaigns management

**Testing Considerations**:
- Contentful changes must be tested in Contentful dev environment first
- Preview deploy will fetch latest Contentful content on build

**Contentful Changes**:
🔗 Contentful Dev Environment: https://app.contentful.com/spaces/{space_id}/environments/development

Entry to test: "Welcome Bonus Promo" (entry ID: abc123)

**How to Test**:
1. Log into Contentful dev environment (link above)
2. Navigate to Content > Promo Banners
3. Verify "Welcome Bonus Promo" entry exists with correct fields
4. Publish the entry in Contentful
5. Trigger preview rebuild or wait for auto-deploy
6. Check homepage for banner display

**Verification**:
[Screenshot: Contentful entry showing promo banner configuration]
[Screenshot: Homepage showing rendered banner]

**Known Limitations**:
- Banner scheduling feature not included (part of CAS-790)
```

## Output Format (in Chat)

**Display QA notes in chat after PR creation**:

```markdown
✅ Pull Request created successfully!

🔗 PR URL: https://github.com/duelbits/frontend/pull/142

---

### 📋 QA Handover Notes
*For your reference - NOT included in PR. Copy to Jira ticket if needed.*

{Generated QA notes here}

---

**Next Steps**:
1. Copy QA notes to Jira ticket comment
2. Request code review
3. Monitor CI/CD pipeline
4. Await QA testing after approval
```

## Brevity Requirements

**Keep QA notes BRIEF**:
- ✅ Bullet points, not paragraphs
- ✅ Technical changes: 3-5 bullets max
- ✅ Impacted areas: 2-4 items
- ✅ Testing considerations: Only critical info
- ✅ How to test: Concise steps

**Avoid**:
- ❌ Long explanations
- ❌ Implementation details
- ❌ Code snippets (unless API examples)
- ❌ Redundant information

## Evals

- [ ] QA notes generated in chat only
- [ ] QA notes NOT added to PR description
- [ ] Technical changes listed (3-5 bullets)
- [ ] Impacted areas identified (2-4 items)
- [ ] Testing considerations provided
- [ ] HOW to test instructions (not WHAT)
- [ ] Backend testing examples included (if applicable)
- [ ] Contentful link provided (if applicable)
- [ ] Verification evidence requested/included
- [ ] Known limitations documented
- [ ] Notes are brief and concise
