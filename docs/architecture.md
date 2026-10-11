# Store architecture

The system follows the MoneyMind split that is relevant for a web-only store: a standalone Django service owns data and an independent Next.js application renders the customer experience.

- **Django + PostgreSQL**: source of truth, media, admin and REST API.
- **Django Admin + Unfold**: back-office for a small team; products are published only when ready.
- **Next.js App Router**: server-rendered catalogue and product pages, metadata and sitemap for search engines.
- **REST contract**: browser does not access the database. The public API exposes only published products.

The product model includes a unique slug, SEO title/description, image alt text, stock and a publication status. Categories and subcategories are separate admin-managed entities: a product belongs to one category and can belong to one managed subcategory. This keeps menu navigation, URLs and filters consistent rather than relying on a free-text label.

Characteristics are normalized as `AttributeDefinition` (specific to a category) and `ProductAttributeValue`. The definition controls its display name, possible choices and whether it is filterable. The legacy `specifications` JSON field is retained only to avoid losing old content; new data must be entered through the Characteristics inline in Django Admin.

Order creation is transactional: the database locks each product row, checks available stock, creates an immutable price/name snapshot and decrements stock in the same transaction. The storefront sends an `Idempotency-Key`; repeating the same request returns the same order without decrementing stock again.

## Demo media policy

Demo products are intentionally model-specific. The seed command only attaches a gallery URL when its source corresponds to the named model; generic stock photos are not permitted as a fallback. Current URLs are temporary external supplier/retailer references for local visual prototyping. Before public launch, upload licensed original/brand-authorized assets through Django Admin and remove the external URLs.
