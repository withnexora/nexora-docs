# UI Verification Notes

## Roles & moderation — 2026-08-25

The Command Deck shows the **Roles & moderation**, **Refunds & CSV** and **Advanced settings** sections for an account with the `admin` role. The Roles & moderation workspace loaded two existing accounts (`admin` and `customer`); the affiliate, review/comment and article queues show clear empty states when nothing needs review. The UI check made no role changes, content approvals, CSV exports or balance adjustments.

## Product–shop mapping — 2026-08-25

The Command Deck catalog now shows an **Unassigned shop** state on every product without a `shop_id`, so admins can spot products to assign before using the per-shop featured section. This check was read-only and did not edit the catalog.

## Article reader — 2026-08-25

Opened `article.html?slug=kiem-tra-tuyen-duong` directly. The route loads its own article bundle, sets the title **Article | NEXORA** and shows a safe empty state when the slug does not exist or the article is unpublished. No sample content, reviews or comments were created for testing.

## Refunds, CSV and database guards — 2026-08-25

The **Refunds & CSV** workspace loads for admins, shows an empty-state table when no refund requests exist and clearly separates the order manager's right to approve requests from the admin's right to export ledger/top-up CSVs. Both export buttons are present but were not triggered, to avoid creating files with unnecessary internal financial data.

Database helpers confirm a customer has no rights to manage roles, moderation, orders, create articles or use the Command Deck; an admin has every corresponding capability. Two affiliate triggers had `EXECUTE` revoked from `authenticated`, while the affiliate/refund request RPCs stay available to signed-in users and check rights/conditions themselves. An ineligible customer was rejected by `request_affiliate_access()` without creating `affiliate_profiles`; a refund request for a non-existent order was also rejected before creating a request or changing a balance.

A temporary role probe confirmed `moderator` can manage non-admin roles, moderate, write articles and enter the Command Deck, but cannot manage orders or act as admin. Re-assigning the `admin` role to the admin account was correctly rejected by the guard, and the test role record was deleted within the same probe. No role audit, order, refund, review/comment, commission or balance change was created.

## Affiliate commission settings — 2026-08-25

After adding the admin RPC and reloading the Command Deck, **Advanced settings** shows the affiliate toggle, commission percentage, minimum delivered orders, minimum order value and approval requirement. Current runtime values: 15%, 1 delivered order, minimum value 0 and approval required. The UI states the setting only affects referral orders delivered later, with no retroactive change to existing commission entries. **12.5%** was temporarily entered and saved through the admin form and the Command Deck showed a confirmation toast; the value was restored to 15% right after the UI check.

## Admin CSV export — 2026-08-25

The Refunds & CSV workspace shows export buttons only for admin sessions. The ledger CSV export was triggered to verify the local download flow; the file was not uploaded, attached, shared or published, and only the internal column structure was checked. The browser confirmed `so-cai-nexora-2026-08-25.csv` was created; it was then deleted locally, and no ledger data was read or kept in the workspace.

## Confirmed E2E: affiliate, refund and moderation — 2026-08-25

With the owner's confirmation, a **20,000 ₫** order fixture was created to test commission/refund and deleted afterwards. Moving the order to `delivered` wrote **3,000 ₫** commission at **15%** to the test affiliate wallet. A **20,000 ₫** wallet refund created a refund ledger row and moved the commission to `pending_reversal`. The order, refund request, commission and ledger fixtures were deleted, and both wallets returned to their exact pre-test values. The affiliate-settings audit was kept as a legitimate operational trace.

A technical (non-user) article fixture went from `pending` to `published` with `published_at` and `reviewed_by`, then was deleted together with its audit fixture. No fake reviews, comments, ratings or testimonials were created in any test.

## Remaining Supabase advisories — 2026-08-25

The Security Advisor keeps warning about `SECURITY DEFINER` RPCs granted to `authenticated`: checkout, account, role, moderation, affiliate, refund and the new affiliate-settings RPC. These are intentional public RPCs for signed-in users; each executes an `auth.uid()` guard and/or a role check in its body. The internal triggers `attach_affiliate_to_order` and `create_affiliate_commission` had `EXECUTE` revoked from `authenticated` and were verified separately. A linter warning does not mean these runtime guards were bypassed; keep reviewing periodically using the [Supabase linter guide](https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable).

## Clean catalog and runtime — 2026-08-25

After a restart, the storefront loads the six-product catalog and shows the CPU/Chip, RAM and Storage filter module together with categories, price and SALE. Snapshots of `/`, `/admin.html` and `article.html?slug=kiem-tra-tuyen-duong` all render; the article shows the correct empty state for a non-existent slug. The console/network after restart show no runtime, import or new 4xx/5xx errors.

## Articles and comments by role — 2026-08-25

The `save_my_article` RPC was tested directly with `marketing`, `moderator`, `affiliate` and `admin`: all four could create drafts with the correct test author; the fixtures were then deleted and the original customer role restored. A neutral technical comment record was created as `pending`, admin moderation set it to `hidden` with `reviewed_by`/`reviewed_at`, and it was deleted with its audit fixture. No fake reviews, ratings or testimonials were created for testing, as content policy forbids it. The review feature uses the same moderation RPC and database guards, but should be verified with real reviews submitted by customers in production.

## Comment CTA and sign-out — 2026-08-25

After the build, the storefront shows a labelled **Comment** button with its own `aria-label` on all six product cards, no longer depending on the hard-to-see Quick View icon. Activating the CTA via the DOM confirmed Quick View opens (`hidden=false`) and focus lands in `#commentBody` after one render tick, with no storefront console errors. The Account Center visibly shows a **Sign out** button in the header while keeping the one in the Security tab; both call the same `db.auth.signOut()` flow. Logout was not clicked during the check so the admin session in use was not cut.

A disposable Supabase client with a separate storage key registered a test session, confirmed the session existed before logout, called `signOut()` without error and received a `null` session afterwards. The admin session in the storefront remained. The probe account was then removed and a query confirmed `0` test accounts remain. The advanced comment fixture clearly went `pending` → `hidden` with `reviewed_by`/`reviewed_at`, and after cleanup neither the comment nor the moderation audit remains.

The `submit_product_review` guard was called with invalid input and correctly rejected it, requiring a 1–5 star rating and minimum content before any review was inserted. No fake review/rating was created; the pending → moderation state for reviews needs real reviews from customers who received their orders.

After a restart, the Command Deck `/admin.html` loads completely with the Roles & moderation, Refunds & CSV and Advanced settings menus; the new session's console is empty. The earlier import warnings for `admin-roles-content.js` and `mountProductShopSelector` did not recur. A 390 × 844 mobile snapshot shows the catalog still responsive; the **Comment** CTA sits on its own row beneath the buy/quick-view buttons so product-card actions are not squeezed.

## Realtime moderation notifications — 2026-08-25

The Command Deck registered the Realtime channel `nexora-moderation-notifications` in the `joined` state for the review and comment tables.

- A pending comment fixture updated the Command Deck instantly: the **Roles & moderation** nav shows a `1` badge, the workspace shows an alert panel “1 item needs moderation”, and the queue holds exactly the fixture with Approve/Hide actions, with no reload needed.
- Hiding the fixture from the moderation queue returned the badge and panel to hidden and the queue to its empty state. Both the comment fixture and its moderation audit were deleted afterwards.
- After the subscription was extended to both `INSERT` and `UPDATE`, the channel reloaded and returned to `joined`. A technical comment moved hidden → pending confirmed the UPDATE event: the badge returned to `1` immediately on the overview screen without reload, and hiding it again through the moderation UI hid the badge/panel and emptied the queue. This is the E2E verification of the `UPDATE → pending` mechanism; the same unit guard applies to the review upsert payload without creating fake reviews/ratings. The transition fixture and its moderation audit were deleted successfully.

## Mobile menu, CMS and custom roles — 2026-08-26

The storefront hamburger was replaced with an open/close flow featuring `aria-expanded`, `aria-hidden`, a tap-to-close backdrop, the Escape key, focus returning to the menu button and background scroll lock while open. A **390 × 844** snapshot confirmed the storefront stays responsive; a fresh session console had no new JavaScript or import errors.

The canonical schema gained `role_definitions`, dynamic capabilities and CMS SEO/icon metadata, and production Supabase has the matching migration applied. An admin probe created the technical role `support_editor_e2e` with Command Deck/article capabilities, confirmed the capabilities were stored, then deleted the role and verified `0` records remain. No user roles or financial data changed. The Command Deck now gives admins a form to create, rename, edit capabilities of and delete custom roles; the Branding CMS manages the site name, logo, favicon, SEO title/description, share image and banner.

All standalone SQL migrations in the repository were merged/removed as requested; only `supabase-unified.sql` remains. Unit tests (**12**), the TypeScript check and the production build all passed before the UI verification.
