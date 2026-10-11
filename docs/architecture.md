# Store architecture

The system follows the MoneyMind split that is relevant for a web-only store: a standalone Django service owns data and an independent Next.js application renders the customer experience.

- **Django + PostgreSQL**: source of truth, media, admin and REST API.
- **Django Admin + Unfold**: back-office for a small team; products are published only when ready.
- **Next.js App Router**: server-rendered catalogue and product pages, metadata and sitemap for search engines.
- **REST contract**: browser does not access the database. The public API exposes only published products.

The product model includes a unique slug, SEO title/description, image alt text, stock, structured specifications and a publication status. This keeps the catalogue manageable without introducing a heavyweight commerce platform.
