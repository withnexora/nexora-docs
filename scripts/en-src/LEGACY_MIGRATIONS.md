# SQL Schema Policy

The NEXORA repository keeps **exactly one SQL file**: [`supabase-unified.sql`](../supabase-unified.sql). It is the source of truth for the catalog, CMS, Account Center, roles/capabilities, moderation, affiliate, refunds, Realtime and all required RLS/RPC.

> Do not add standalone `.sql` migrations to the repository. When a production Supabase project that already has data needs an upgrade, create and apply a managed DDL migration from the difference to the canonical schema, after taking a backup and testing on staging.
