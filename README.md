# WFH Blog & Store Application

A Django platform built for the Work From Home internship. Combines a blog (with admin-gated user/post approval and comments) and an e-commerce store (product listings, cart, and Stripe checkout).

**Live site:** https://wfh-blog-app.onrender.com
**Repo:** https://github.com/SalmanShahzadAli/Python-Blog-Application

## Features Implemented

### Blog
1. **Email + social login (Google, Facebook)** — custom email-based `CustomUser` model, Google/Facebook OAuth via `django-allauth`.
2. **Admin approval of user accounts** — new signups default to `is_approved = False` and are blocked from logging in until an admin approves them. Enforced at login, post creation, and comment posting, plus a signal that closes the social-signup edge case.
3. **Users add blog posts** — approved users submit posts via a front-end form; new posts default to "Pending Approval."
4. **Admin approval of blog posts** — custom admin with bulk Approve/Reject actions and status filtering.
5. **Viewers read + comment** — posts and comments are publicly readable; only approved, logged-in users can post a comment.

### Store (E-commerce)
1. **Product add/edit/delete** — any approved user can list, edit, or delete their own products (marketplace-style). Ownership is enforced server-side (403 if you try to edit someone else's listing).
2. **Order viewing** — logged-in users can view their own order history and order details.
3. **Frontend product display** — public product grid and detail pages, with images, price, and stock status.
4. **Add to cart** — database-backed cart per user; add, update quantity, remove items.
5. **Stripe payment** — checkout creates an `Order`, redirects to Stripe Checkout (test mode), and verifies payment server-side via the Stripe API before marking the order "Paid."

## Tech Stack

- Python / Django
- `django-allauth` — social authentication
- `stripe` — payment processing (test mode)
- `Pillow` — image upload handling
- Bootstrap 5 (CDN) — styling
- PostgreSQL (Neon, production) / SQLite (local dev)
- Hosted on Render (free tier)

## Project Structure

- `accounts/` — custom user model, email auth, admin-approval logic, social login adapter/signal
- `blog/` — post model, creation form, admin approval actions, public list/detail views
- `comments/` — comment model, form, and submission view
- `store/` — product, cart, and order models; product CRUD, cart, and Stripe checkout views
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

3. Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   STRIPE_PUBLIC_KEY=pk_test_...
   STRIPE_SECRET_KEY=sk_test_...
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000/`

## Social Login Setup

Social login credentials are stored as `SocialApp` entries in Django admin (`/admin/socialaccount/socialapp/`), not hardcoded in settings. To enable a provider:

1. Create OAuth credentials on the provider's developer console (Google Cloud Console / Facebook for Developers), with the redirect URI:
   ```
   https://<your-domain>/accounts/<provider>/login/callback/
   ```
2. Add a Social Application in Django admin with the provider's Client ID and Secret.

**Status:**
- **Google** — fully implemented and live-tested end-to-end, both locally and in production.
- **Facebook** — implemented using the identical `django-allauth` pattern as Google. Not live-tested, since it requires a personal Facebook Developer account. It will function as soon as valid Facebook App credentials are added under Social Applications in Django admin — no code changes needed.

## Payment Testing

Stripe is configured in **test mode** — no real charges occur. Use Stripe's test card to complete a checkout:
```
Card number: 4242 4242 4242 4242
Expiry: any future date
CVC: any 3 digits
ZIP: any 5 digits
```

## Deployment Notes

- Hosted on Render's free web service tier, with a Neon PostgreSQL database (Render's own free database tier requires card verification with no persistent access via shell; Neon was used instead as a fully free alternative).
- Since the free tier has no shell access, a custom management command (`create_admin`) creates the superuser automatically on deploy, from environment variables (`DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`).
- Free instances spin down after inactivity; the first request after idling can take 30–60 seconds to respond.
- Uploaded product images are stored on local disk (`MEDIA_ROOT`), which is ephemeral on Render's free tier and may be cleared on redeploy. For persistent image storage in a real production setting, this should move to a service like Cloudinary or AWS S3.

## Known Simplifications

- Social app secrets and Stripe keys are managed via environment variables (Render) / `.env` (local) rather than a secrets manager — sufficient for this project's scope.
- No automated test suite yet (`tests.py` files are scaffolded but empty).
- Styling uses Bootstrap defaults rather than custom branding.
- Product images are not persisted long-term on the free hosting tier (see Deployment Notes above).