# Roles, Moderation, Affiliate and Refunds

NEXORA extends the Command Deck with a **permission matrix enforced at the database**. The UI is only a convenience layer; Supabase RLS and RPCs make the final decision. Every role change, affiliate approval, content moderation and refund is written to the audit log.

> Never grant access by editing browser JavaScript. Use the **Roles & moderation** workspace or the matching RPC so rules and audit logs stay intact.

## Role matrix

| Role | Command Deck | Main permissions | Important limits |
| --- | --- | --- | --- |
| `customer` | No | Shop, manage profile/balance, post comments, request refunds. | Cannot create articles or administer. |
| `affiliate` | No | Create articles in the Account Center, get a referral link once approved. | Cannot self-approve articles or view customer/order data. |
| `marketing` | Yes | Draft articles and submit for review. | No role, order, balance or CMS management. |
| `order_manager` | Yes | Process orders; approve/reject/refund. | Cannot export ledger CSV or change branding/site settings. |
| `moderator` | Yes | Assign non-`admin` roles; approve affiliates, reviews, comments and articles. | Cannot change the `admin` role, adjust balances or edit the CMS. |
| `admin` | Yes, highest | All of the above, plus balance credit/debit, CMS, payment config, favicon, effects and CSV. | Must still follow audit, reconciliation and legal review. |

Admin is the highest level. A moderator can manage the operational roles an admin allows but cannot grant, demote or change `admin`.

### Custom roles and capabilities

Admins can use **Command Deck → Roles & moderation → Create & edit role permissions** to create a new role, rename its display name, add/remove capabilities, or delete a custom role that nobody holds. The role code is a fixed technical identifier after creation, while the display name can change. System roles cannot be deleted; admins can still adjust their names/capabilities, but `admin` always keeps every capability and cannot be assigned by a moderator.

| Capability | Effect |
| --- | --- |
| `commandDeck` | Allows entering the Command Deck. |
| `articles` | Allows creating and submitting articles. |
| `moderation` | Approve/hide reviews, comments and articles. |
| `orders` | Manage orders and refund requests. |
| `roles` | Assign user roles within the `assignable_by_moderator` limit. |
| `siteSettings` | Edit storefront identity/CMS. |

## Roles & moderation

In **Command Deck → Roles & moderation**, admins and moderators see basic profiles and current roles. Choosing a new role requires a note and calls `assign_user_role`, which updates `user_roles`, syncs `admin_users` when the role is `admin`, then appends a `role_assigned` row to `account_audit_log`.

Reviews, comments and articles all pass through the moderation queue. A product review can only be submitted if the customer received the product or the order is completed; comments require a signed-in user. Public content is visible only with status `approved` or, for articles, `published`.

The public article page is `/article.html?slug=<slug>`. It queries only `published` articles, escapes content before rendering and returns an empty state for invalid, missing or unpublished slugs.

| Content type | Submitter | Initial status | Reviewer | Public status |
| --- | --- | --- | --- | --- |
| Product review | Customer who received the item | `pending` | Moderator or admin | `approved` |
| Product comment | Signed-in customer | `pending` | Moderator or admin | `approved` |
| Article | Marketing, moderator, admin or approved affiliate | `draft`/`pending` | Moderator or admin | `published` |

## Affiliate and the 15% commission

An affiliate starts with a request in **Account & balance → Affiliate**. The default condition is at least one `delivered` order; the program can require moderator/admin approval. Once approved, the user receives the `affiliate` role and a link like:

```text
https://<your-domain>/?ref=<REFERRAL_CODE>
```

A referral is linked once to a buyer after they sign in; users cannot use their own link. When a referred order has a valid payment status and fulfillment is `delivered`, the system creates a **default 15% commission** using `floor(total_amount × commission_rate / 100)`, writes an `affiliate_commission` ledger entry and credits the affiliate balance. The rate, order conditions and approval requirement live in `affiliate_program_settings`.

> On a refund, the order's commission moves to `pending_reversal` so it is not treated as final. Reversing the commission is a follow-up reconciliation task; a clear accounting process is needed before paying out real money.

## Refunds and CSV

A customer can create a refund request for orders in `paid`, `processing` or `completed`. Order managers/admins can approve, reject or refund. With the `wallet` method, the system credits the customer balance and writes a `refund` entry; with `manual`, an administrator must reconcile the transaction outside the system.

| Action | Allowed roles | Trail |
| --- | --- | --- |
| Create a refund request | Order owner | `refund_requests`, order status `requested` |
| Approve/reject/refund | `order_manager`, `admin` | `refund_reviewed`, order and request status |
| Refund to balance | `order_manager`, `admin` | `refund` ledger row and new balance |
| Export ledger/top-up CSV | `admin` | Download in the Command Deck; store the file per internal data policy |

Never push CSV exports to GitHub, send them over public channels or treat them as the original record. The database and audit log remain the primary source for reconciliation.

## Featured products per shop

Each `products.shop_id` links directly to `shops.id`. In **Command Deck → Products**, admins choose the shop when creating/editing the catalog; the catalog table shows the shop name or an **Unassigned shop** label to avoid confusion. The storefront prefers this mapping when building per-shop featured products and only falls back to category when a shop has no assigned products.

## Advanced CMS for admins

The **Branding, icons & SEO** section lets an admin, or a role with `siteSettings`, update the site name, logo, favicon, SEO title/description, Open Graph share image, banners, contact details and storefront content without editing files. The **Advanced settings** workspace is admin-only and updates the bank code/account number/recipient name, MoMo number, HTTPS ZaloPay QR image URL, storefront effects, automatic bank transfer and the affiliate program. Admins can toggle automatic transfer, choose SePay/Casso/VietQR Host2Host and see the webhook URL and masked secret status; they cannot view, enter or save merchant secrets/API keys in the CMS. The ZaloPay QR URL is for manual reconciliation only.

Admins can toggle affiliate, set the **commission rate from 0–100%**, the minimum number and total value of `delivered` orders, and the approval requirement. Saving calls the `admin_update_affiliate_program` RPC, which checks admin rights in the database and writes `affiliate_program_updated` to the audit log. The rate applies when the trigger creates commissions for qualifying orders later; it is not retroactive to existing entries.

| Effect setting | Meaning | Recommendation |
| --- | --- | --- |
| `none` | Effects off. | Use as the default. |
| `snow` | Falling snow with adjustable color/density. | Low density on mobile; check `prefers-reduced-motion` when extending. |
| `cherry_blossom` | Falling cherry blossoms with custom color/density. | Enable only for suitable seasons/campaigns. |

Receiving-account information is sensitive operational data. Enter it only after confirming with the shop owner, and keep it out of public files and GitHub commit history.

## Testing before opening permissions

| Test | Expected result |
| --- | --- |
| Customer opens `/admin.html` | Blocked. |
| Marketing enters the Command Deck | Sees only the areas suited to creating/reviewing articles. |
| Moderator changes the `admin` role | Rejected by the database. |
| New review/comment | Not publicly visible before approval. |
| Delivered referral order | Creates one commission entry, unique per `order_id`. |
| Wallet refund | Balance and `wallet_ledger` change together in the approval flow. |
| CSV export | Only admins see/download the export button. |

See also [Account & Wallet](ACCOUNT_WALLET.md), the [Supabase guide](SUPABASE.md), [verification notes](VERIFICATION_NOTES.md) and [expansion scope](FEATURE_EXPANSION_SCOPE.md).
