# Gundam Online Store

A Django-based e-commerce platform for Gundam model kits, featuring product listings, discounts, and multiple images per product.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kalpakjian/gundam-store.git
   cd gundam-store
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```

7. Access the site at `http://127.0.0.1:8000/` and the admin interface at `http://127.0.0.1:8000/admin/`.

## Current Features
- Homepage with featured (discounted) products
- Product list with prices, scales, and cover images
- Admin interface for managing categories, products, and images
- Support for discounts and multiple product images

## Planned Features
- Product detail pages
- Shopping cart functionality
- Search and category filtering
- PostgreSQL database migration

## Notes
- Ensure `.env` is configured with `DJANGO_SECRET_KEY` (see `.env.example`).
- Media files (e.g., product images) are stored in `media/`, which is ignored by Git.
