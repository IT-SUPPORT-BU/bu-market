# Internship Teaching Curriculum & Guide — BU-MARKET

This guide outlines a week-by-week teaching plan to instruct interns in Python/Django backend programming, HTML/CSS/JavaScript web basics, and Git collaborative project management using the BU-MARKET codebase.

---

## 📅 Course Outline: 4-Week Practical Roadmap

### 📦 Week 1: Web Basics (HTML/CSS) & Git Workflows
- **Objective**: Get every student familiar with the DOM structure, CSS styles, Bootstrap grid systems, and the basics of distributed version control using GitHub.
- **Topics**:
  - HTML structure: headings, sections, links (`<a>`), images, divs.
  - CSS layout: styling colors, text typography, margin vs. padding.
  - Bootstrap 5 utilities: container, row, cols, responsive visibility (`d-none`, `d-md-block`).
  - Git flow: Forking, cloning, committing changes, and opening Pull Requests.
- **Class Lab Exercise (First Win)**:
  1. Have every student fork the repository `IT-SUPPORT-BU/bu-market`.
  2. Clone it locally and run: `python manage.py runserver`
  3. Navigate to `templates/base.html` and customize the footer text (e.g., add "Intern Cohort 2026").
  4. Edit `static/css/style.css` to add a style (e.g., custom hovering color for list items).
  5. Stage, commit, push, and submit a Pull Request to the central repository's `develop` branch.
  6. **Teaching Tip**: Approve and merge these pull requests live during class! Seeing their change go live instantly builds student confidence.

---

### 🗺️ Week 2: Django MVT Pattern & Routing
- **Objective**: Explain the Model-View-Template (MVT) pattern that controls web server flow.
- **Topics**:
  - Request-Response lifecycle: How Django processes a URL request.
  - URL mapping: `urls.py` config paths and regex/slug matching.
  - Django views: Class-based views (`ListView`, `DetailView`) and functional views.
- **Class Lab Exercise (Building a Page)**:
  1. Guide students to build a static "About BU-MARKET" page.
  2. Add path in `core/urls.py`:
     ```python
     path('about/', views.about_page, name='about'),
     ```
  3. Write a view in `core/views.py`:
     ```python
     def about_page(request):
         return render(request, 'core/about.html')
     ```
  4. Create `templates/core/about.html` extending `base.html`.
  5. Link to it from the navbar using the DTL tag:
     ```html
     <a href="{% url 'core:about' %}">About Us</a>
     ```

---

### 📝 Week 3: Database Models & Django Forms
- **Objective**: Learn databases, migrations, and user data capture.
- **Topics**:
  - Database schema: Django fields (CharField, DecimalField, ForeignKey).
  - Migrations: `makemigrations` (records changes) and `migrate` (updates schema).
  - Django Forms: Binding POST requests, validating inputs, displaying fields in Bootstrap template.
- **Class Lab Exercise (Modifying Forms)**:
  1. Add a `phone_number` field to the listing model in `marketplace/models.py`.
  2. Run migration commands:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
  3. Add the field to the form layout in `marketplace/forms.py`.
  4. Modify `templates/core/listing_detail.html` to display the phone number next to the seller's contact details.

---

### 🛡️ Week 4: Business Logic & Unit Testing
- **Objective**: Introduce backend data safety, permission validation, and automated quality checks.
- **Topics**:
  - Server-side validations inside the model's `clean()` method.
  - Role check middleware and custom view decorators (`@login_required`).
  - Writing test cases (`TestCase`) to assert business rule correctness.
- **Class Lab Exercise (Quality Testing)**:
  1. Open `marketplace/tests.py` and review tests.
  2. Run testing suite:
     ```bash
     python manage.py test
     ```
  3. Write a new unit test checking that if a seller listing is set to `is_promoted=True` under the BASIC subscription plan, it raises a `ValidationError` when `clean()` is called.

---

## 🚀 How to Manage Collaborations & PR Reviews

1. **GitHub Issues Boards**:
   - Direct students to the **Issues** tab on GitHub populated from `GITHUB_ISSUES.md`.
   - Have them assign themselves to a specific issue based on their team assignments.
2. **Pull Request Peer Reviews**:
   - Instruct students to open PRs from their forks to the original repository's `develop` branch.
   - Hold live code review sessions where students review each other's code syntax, logic correctness, and styling.
   - Merge the approved code into the centralized `develop` branch!
