# Public API contract

Base URL: `/api/v1`.

- `GET /health/` — unauthenticated readiness check.
- `GET /categories/` — active categories with active, admin-managed `subcategories` and their available brands.
- `GET /products/?category=&subcategory=&brand=&attr_<attribute-slug>=&q=` — published products. `brand` may be repeated. Product data includes ordered `images` and normalized `attributes`.
- `GET /products/<slug>/` — product detail.
- `POST /orders/` — creates an order. Required: `customer_name`, Ukrainian `phone`, and 1–20 `items` (`slug`, `quantity`). Optional: email, comment, payment method.

`POST /orders/` accepts an optional UUID `Idempotency-Key` header. A retry with the same key returns the original order (`200`) rather than creating another one. A newly accepted request returns `201`.

Public endpoints expose only products in `published` status. Admin-only catalogue maintenance happens through Django Admin, never through the public API.
