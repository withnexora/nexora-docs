# Mobile and Email URL Verification

Verification date: **2026-08-26**.

| Scope | Result |
| --- | --- |
| Storefront at 390 × 844 | Header, search, cart, menu and account shortcut fit the viewport; the hero keeps CTAs with clear touch targets. |
| Orders at 390 × 844 | Title, order number, status chips and the Zalo CTA stack vertically with no horizontal overflow at the top. |
| Command Deck at 390 × 844 | Navigation becomes a horizontal scroll strip with icon plus label; workspaces stay reachable instead of relying on icons alone. |
| Auth email URL | The helper accepts only public HTTPS; `localhost`, previews and HTTP fall back to the production domain. |

No real email was sent in this check because SMTP/provider secrets were not configured. Finish Site URL, Redirect URLs and the SMTP/Send Email Hook in the Supabase Dashboard before verifying real mailboxes.

## Command Deck: Email & Domain

Checked live with an admin account: the **Email & Domain** workspace shows the production fallback, the SMTP metadata form has no password/API-key field, and the Supabase Auth checklist is present. The **Accounts & balances** workspace shows the password-reset button and a confirmed close/anonymize action per customer. The browser console showed no errors while viewing these workspaces.

It lists direct SMTP, Resend Hook, Postmark Hook and other providers; each has its own checklist and no secret input. The Forgot password email form shows the content, a preview and a copy-HTML button that keeps the fixed `{{ .ConfirmationURL }}` placeholder. Selecting **Resend Hook** updates the Edge Function/secret-manager checklist instantly, and changing the template heading updates the preview instantly without writing data until the admin presses save. The **Copy Supabase HTML** button produced the recovery HTML with a success message and the placeholder intact.

## Recovery and login

- With the `/?recovery=1` callback on an authenticated session, the modal opens in new-password mode, shows only two password fields, validates match/length before calling update and uses dedicated copy for the recovery session. No real email was sent and no real password changed.
- With the error callback `?recovery=1&error=access_denied&error_code=otp_expired`, the URL is cleaned to `/`, the modal switches to **Forgot password**, the user can request a new link and sees a clear error. This relies on the callback error parameters, not on timeouts guessing the session state.
- After the login fix, `#authPassword` stays in the DOM with `type=password`, is not disabled/hidden and receives focus. The earlier cause was the translator overwriting the `textContent` of the label that contains the input. A non-sensitive value (`demo-pass-123`) confirmed the field accepts and keeps data, without submitting or signing in.

## Catalog fallback

Production reproduced the catalog fallback notice while six fallback products still rendered. The console had no runtime exception. A read-only production query (`products.select('*').order('featured').order('created_at')`) returned six rows with no error, so the warning was a false fallback or a transient load failure at startup, not missing catalog data or RLS. After making `hidden` the priority CSS state, the storefront preview loaded six real products and no longer rendered the “Cannot sync the latest catalog” panel.

## Menu, payments and sessions

- The hamburger button opens the menu with `aria-expanded=true`, the nav is no longer hidden and the scrim works; clicking the scrim closes it, returning `aria-expanded=false` and `hidden=true`. A 390 px snapshot confirmed the closed header/menu does not cover the hero content.
- The balance payment flow only creates the `/orders.html?paid=wallet&order=…` URL when the RPC returns an order with `status=paid` and `payment_method=wallet`; the real payment RPC was not called to avoid changing balances. The Orders destination loaded with this URL. The transfer-confirmation RPC only writes `zalo_confirmation_requested_at` and never sets `status=paid`.
- Command Deck access review found the backend/preview still serving the page; the browser error was `refresh_token_not_found` from Supabase Auth. The admin flow now clears the stale local session before signing in again and shows a clearer recovery message. The sign-out event ordering was also fixed so the “old session is no longer valid” message is no longer overwritten by a generic Supabase callback message.

## ZaloPay QR

ZaloPay was added in manual QR/transfer mode: the checkout tab and the VietQR/MoMo/ZaloPay labels render correctly on the storefront. Tests only confirmed UI presence and HTTPS URLs; no order or real transaction was created.

- With fake display data, the QR frame turns a prominent purple, the three-step scan panel appears and no real order or transaction is created. QR, amount, order code, three steps and the security warning appear in one flow, with no console runtime errors.
- The modal keeps scroll state when content is long, the QR frame is 270px on desktop and the instructions stay reachable.
- The two copy buttons (**Copy transfer content** and **Copy account number**) wrote the correct fake order code and fake value to the clipboard. They are clearly labelled and shown when the ZaloPay QR is valid.
- At a 390px viewport the buttons stack into one column, each 44px tall, and the modal does not overflow horizontally.

## Automatic bank transfer

Tested with a pure data module and a server status endpoint: SePay/Casso/VietQR Host2Host accept only valid NEXORA order codes, incoming-money transactions and valid signature/timestamp. The Command Deck endpoint only returns configured/not-configured status, never secrets. The tests did not call providers, create orders, change payment status or generate real money transactions.
