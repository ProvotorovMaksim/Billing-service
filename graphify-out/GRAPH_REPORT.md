# Graph Report - Billing-service  (2026-11-12)

## Corpus Check
- В структурный анализ включено файлов исходного кода: 12. Сторонние зависимости, документация и файлы окружения исключены.

## Summary
- 101 nodes · 224 edges · 7 communities
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- payments.py
- models.py
- env.py
- db_provider.py
- settings.py
- schemas.py
- create_tariff

## God Nodes (most connected - your core abstractions)
1. `create_payment()` - 11 edges
2. `Payment` - 10 edges
3. `get_tariff()` - 10 edges
4. `Subscription` - 9 edges
5. `PaymentStatus` - 9 edges
6. `SubscriptionStatus` - 8 edges
7. `Tariff` - 8 edges
8. `payment_callback()` - 8 edges
9. `create_subscription()` - 8 edges
10. `activate_subscription()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `get_subscription()` --uses--> `Subscription`  [INFERRED]
  db_provider.py → models.py
- `create_tariff()` --uses--> `Tariff`  [INFERRED]
  tariffs.py → models.py
- `get_all_tariffs()` --uses--> `Tariff`  [INFERRED]
  tariffs.py → models.py
- `payment_callback()` --uses--> `PaymentStatus`  [INFERRED]
  db_provider.py → models.py
- `create_payment()` --uses--> `PaymentStatus`  [INFERRED]
  payments.py → models.py

## Import Cycles
- None detected.

## Communities (7 total, 0 thin omitted)

### Community 0 - "payments.py"
Cohesion: 0.19
Nodes (10): add_payment(), get_subscription(), payment_callback(), set_payment_id(), produce_message(), producer_callback(), publish_payment_success(), Payment (+2 more)

### Community 1 - "models.py"
Cohesion: 0.15
Nodes (7): activate_subscription(), Base, Subscription, SubscriptionStatus, create_subscription(), get_subscription(), get_user_subscription()

### Community 2 - "env.py"
Cohesion: 0.15
Nodes (5): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online(), upgrade()

### Community 3 - "db_provider.py"
Cohesion: 0.33
Nodes (4): get_db(), get_tariff(), read_route(), Tariff

### Community 4 - "settings.py"
Cohesion: 0.17
Nodes (3): Settings, Config, YookassaService

### Community 5 - "schemas.py"
Cohesion: 0.33
Nodes (6): PaymentStatus, Payment, PaymentConfirmationRequest, PaymentRequest, Subscription, Tariff

### Community 6 - "create_tariff"
Cohesion: 0.25
Nodes (3): create_tariff(), get_all_tariffs(), get_tariff()

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_tariff()` connect `db_provider.py` to `payments.py`, `models.py`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `create_payment()` (e.g. with `Payment` and `PaymentStatus`) actually correct?**
  _`create_payment()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `models.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14619883040935672 - nodes in this community are weakly interconnected._
- **Why does `Tariff` connect `db_provider.py` to `models.py`, `create_tariff`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Payment` (e.g. with `add_payment()` and `payment_callback()`) actually correct?**
  _`Payment` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Why does `create_subscription()` connect `models.py` to `db_provider.py`, `schemas.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `Subscription` (e.g. with `activate_subscription()` and `get_subscription()`) actually correct?**
  _`Subscription` has 5 INFERRED edges - model-reasoned connections that need verification._