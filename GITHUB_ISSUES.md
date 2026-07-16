# GitHub Issues for BU-MARKET MVP

This document contains 20+ GitHub-ready issues categorized by development teams. Use these to populate the GitHub repository Project board.

---

## 🔑 Authentication Team (Accounts App)

### #1 Implement Custom User Model with Roles
- **Description**: Set up the custom `User` model inheriting from `AbstractUser` with choices for roles: `BUYER`, `SELLER`, `ACCOUNTANT`, `MODERATOR`, and `ADMIN`.
- **Labels**: `backend`, `accounts`, `priority:high`

### #2 Configure Django Custom User Admin
- **Description**: Subclass `UserAdmin` as `CustomUserAdmin` and register it in `accounts/admin.py` to ensure roles are visible and editable within the Django Admin console.
- **Labels**: `backend`, `accounts`, `priority:medium`

### #3 Build Campus Registration Form and View
- **Description**: Implement user registration view utilizing a subclassed `UserCreationForm` containing a radio choice field for SELLER and BUYER roles.
- **Labels**: `backend`, `frontend`, `accounts`, `priority:high`

### #4 Implement Login and Post-Logout Redirects
- **Description**: Add built-in `LoginView` and `LogoutView` configurations mapping to custom templates and verify redirection settings in `settings.py`.
- **Labels**: `backend`, `accounts`, `priority:medium`

---

## 🛒 Marketplace Team (Marketplace App)

### #5 Establish Dynamic Categories Model and Slugs
- **Description**: Implement the `Category` model with `name`, `slug` (auto-generated), `icon` (bootstrap class), and `is_active` fields.
- **Labels**: `backend`, `marketplace`, `priority:high`

### #6 Implement Marketplace Listing Model
- **Description**: Create the `Listing` model containing links to categories and sellers, condition (NEW/USED), listing status, promoted status, views count, and created/updated timestamps.
- **Labels**: `backend`, `marketplace`, `priority:high`

### #7 Add Auto-slug generation for Marketplace Listings
- **Description**: Write a custom `save()` method override on the `Listing` model that converts the title into a unique slug, appending a counter if conflicts arise.
- **Labels**: `backend`, `marketplace`, `priority:medium`

### #8 Implement Search and Filter Query Logic
- **Description**: Write backend filters inside `BrowseView` supporting full text queries (`q`), category filters, price range constraints, condition, and promoted sorting.
- **Labels**: `backend`, `marketplace`, `priority:high`

---

## 💳 Subscription & Payments Team (Subscriptions/Payments App)

### #9 Seed Subscription Plans
- **Description**: Define the `SubscriptionPlan` model with Basic, Silver, and Gold settings, and write automatic seeding logic (via command or migrations).
- **Labels**: `backend`, `subscriptions`, `priority:high`

### #10 Implement Seller Subscription Receipt Request
- **Description**: Build the model `SellerSubscription` and form supporting plan choice, receipt image upload, payment reference, and PENDING status.
- **Labels**: `backend`, `subscriptions`, `priority:high`

### #11 Implement Buyer Membership Application
- **Description**: Build `BuyerMembership` model and form capturing 20,000 UGX flat payments and receipt uploads.
- **Labels**: `backend`, `subscriptions`, `priority:high`

### #12 Enforce Listing Creation Caps on Server-Side
- **Description**: Overwrite the `clean()` method on the `Listing` model to throw validations if a BASIC/SILVER/GOLD seller exceeds their listing cap.
- **Labels**: `backend`, `subscriptions`, `priority:high`

### #13 Restrict Promoted Ads to Silver and Gold Plans
- **Description**: Implement server-side check ensuring `is_promoted` can only be set to `True` if the seller's active plan allows it.
- **Labels**: `backend`, `subscriptions`, `priority:medium`

---

## 🛡️ Moderation Team (Moderation App)

### #14 Create Listing Approval/Rejection Actions
- **Description**: Set up moderator views to change product statuses between ACTIVE and REJECTED, returning messages to the dashboard.
- **Labels**: `backend`, `moderation`, `priority:high`

### #15 Build Moderator Pending Queue view
- **Description**: Implement a portal dashboard that filters only `PENDING` listing items for review by users with the Moderator role.
- **Labels**: `backend`, `moderation`, `priority:medium`

---

## 🎨 Frontend Team (Templates & Static Assets)

### #16 Design Responsive Mobile Navigation and Desktop Header
- **Description**: Implement the `base.html` structure featuring top desktop navigation and a fixed mobile-friendly bottom navigation bar with tap targets.
- **Labels**: `frontend`, `templates`, `priority:high`

### #17 Design Marketplace Home and Hero Banner
- **Description**: Construct a home page template showing custom Bugema color schemes, category grid buttons, and a highlighted carousel of promoted products.
- **Labels**: `frontend`, `templates`, `priority:high`

### #18 Create Mobile-Friendly Listing Grid and Filter Sidepane
- **Description**: Create the browse template showing items in clean cards, alongside form controls for keyword, price, category, and condition filters.
- **Labels**: `frontend`, `templates`, `priority:high`

---

## 🧪 Testing Team (Tests App)

### #19 Write Unit Tests for User Roles and Access Controls
- **Description**: Add tests verifying role properties, custom user creation, and role-based decorator access constraints.
- **Labels**: `testing`, `priority:medium`

### #20 Test Subscription Limit Violations
- **Description**: Write test cases attempting to add active listings beyond plan caps, validating that the backend clean() triggers database errors.
- **Labels**: `testing`, `priority:high`
