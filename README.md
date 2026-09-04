# WFH Blog Application

A Django blog platform built for the Work From Home internship task. Supports email and social login, admin-gated user approval, user-submitted blog posts with admin approval, and reader comments.

## Features Implemented

1. **User login with email and social login (Google, Facebook)**
   Custom email-based authentication using a `CustomUser` model, plus Google and Facebook OAuth via `django-allauth`.

2. **Admin approval of user accounts**
   New signups (email or social) default to `is_approved = False`. Unapproved users cannot log in — they're shown a "pending admin approval" message. An admin flips `is_approved` to `True` in Django admin to grant access. This is enforced at multiple layers (login view, post creation, comment posting, and a signal that catches the social-signup edge case).

3. **Users can add blog posts**
   Approved users submit posts via a front-end form. New posts default to "Pending Approval" status and are not publicly visible until approved.

4. **Admin approval of blog posts**
   Admin panel includes a custom `Post` admin with bulk "Approve" / "Reject" actions and status filtering.

5. **Viewers can read and post comments**
   Blog posts and their comments are publicly readable by anyone, including logged-out visitors. Only approved, logged-in users can submit a comment.

## Tech Stack

- Python / Django
- `django-allauth` for social authentication
- Bootstrap 5 (via CDN) for styling
- SQLite (default Django dev database)

## Project Structure

- `accounts/` — custom user model, email auth, admin-approval logic, social login adapter/signal
- `blog/` — post model, creation form, admin approval actions, public list/detail views
- `comments/` — comment model, form, and submission view
- `core/` — project settings, root URLs, shared `base.html` template

## Setup Instructions

1. Clone the repo and create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000/`

## Social Login Setup

Social login credentials are stored as `SocialApp` entries in Django admin (`/admin/socialaccount/socialapp/`), not hardcoded in settings. To enable a provider:

1. Create OAuth credentials on the provider's developer console (Google Cloud Console / Facebook for Developers), with the redirect URI:
   ```
   http://127.0.0.1:8000/accounts/<provider>/login/callback/
   ```
2. Add a Social Application in Django admin with the provider's Client ID and Secret.

**Status:**
- **Google** — fully implemented and live-tested end-to-end (new signup, approval gate, existing-account linking).
- **Facebook** — implemented using the identical `django-allauth` pattern as Google (same adapter, same approval-enforcement signal, same admin registration flow). Not live-tested, since it requires a personal Facebook Developer account. It will function as soon as valid Facebook App credentials are added under Social Applications in Django admin — no code changes needed.

## Known Simplifications

- Social app secrets are stored in the database via Django admin rather than environment variables — acceptable for local development, but should move to environment variables before any production deployment.
- No automated test suite yet (`tests.py` files are scaffolded but empty).
- Styling is intentionally minimal/functional (Bootstrap defaults) rather than custom-branded.
