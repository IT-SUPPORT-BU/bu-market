# MVP Scope and Roadmap — BU-MARKET

This document outlines the scope of the Bugema University community marketplace MVP (BU-MARKET) and lists out-of-scope features deferred to future phases.

---

## 🟢 In Scope (MVP Features)
1. **User Accounts & Roles**:
   - Custom accounts for Buyer, Seller, Accountant, Moderator, and Admin.
   - Separate dashboards and view authorization permissions for each role.
2. **Subscriptions & Membership Plans**:
   - Seeded pricing plans (Basic, Silver, Gold).
   - Server-side enforcement of listing caps (2, 5, or 10 active listings).
   - Payment upload receipts for subscription approvals.
   - Flat buyer memberships (20,000 UGX).
3. **Marketplace Listings**:
   - Categories listing (seeded: Phones, Electronics, Hostels, etc.).
   - Product details: title, condition, price, location, image, view count.
   - Server-side validation of active subscription state prior to listing.
4. **Search and Filtering**:
   - Keyword search in titles/descriptions.
   - Filter by Category, Price range, and Condition (NEW/USED).
   - Ordering: Promoted-first, newest-first.
5. **Mobile-First UI Layout**:
   - Header bar, bottom mobile fixed nav, custom Outfit typography.
   - Custom Bugema colors: Blue (#003B8E) and Gold (#D4AF37).
6. **Listing Moderation**:
   - Review queue for moderators to toggle listing status to ACTIVE or REJECTED.

---

## 🔴 Out of Scope (Deferred to Phase 2)
1. **Messaging / Chat**:
   - Currently, buyer contacts seller via email mailto links. Real-time chat is deferred.
2. **Escrow & Payment Gateways**:
   - Financial verification is done manually by the Accountant reviewing screenshots. Direct integration with MTN Mobile Money or Airtel Money APIs is deferred.
3. **Escrow System**:
   - Safe delivery and fund holdings are managed offline.
4. **Real-time Notifications**:
   - Email alerts or browser push notifications are deferred.
5. **Ratings and Reviews**:
   - Star ratings and comment feedback on sellers are deferred.
