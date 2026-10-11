# Public API contract

Base URL: `/api/v1/`

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/categories/` | Active categories |
| GET | `/products/?category=&q=&featured=true` | Published product catalogue |
| GET | `/products/{slug}/` | Product page data |
| POST | `/orders/` | Create an order from `{ customer_name, phone, email?, comment?, payment_method: "cod"|"bank", items: [{ slug, quantity }] }` |

The order endpoint validates availability and captures the product name and price at time of purchase. Payment is intentionally external to this first version.
