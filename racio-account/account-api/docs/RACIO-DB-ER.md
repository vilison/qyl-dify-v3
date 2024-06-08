## RACIO Accounts ER Diagrams

### Mermaid Live Editor

```mermaid
---
title: RACIO ACCOUNTS ER DIAGRRAM
--- 
erDiagram
    ACCOUNTS_INTEGRATES ||--o{ ACCOUNTS : "account_id"
    MEMBER_INVITE }o--o{ ACCOUNTS : "invited_by"
    ACCOUNTS {
        uuid id PK "DEFAULT uuid_generate_v4()"
    }
    ACCOUNTS_INTEGRATES {
        uuid id PK "DEFAULT uuid_generate_v4()"
        uuid account_id FK
    }
    MEMBER_INVITE {
        uuid id PK "DEFAULT uuid_generate_v4()"
        uuid invited_by FK 
        uuid tenant_id 
    }
    ALEMBIC_VERSION {
        varchar version_num PK "varchar(32)"
    }
```

```mermaid
erDiagram
    CUSTOMER }|..|{ DELIVERY-ADDRESS : has
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER ||--o{ INVOICE : "liable for"
    DELIVERY-ADDRESS ||--o{ ORDER : receives
    INVOICE ||--|{ ORDER : covers
    ORDER ||--|{ ORDER-ITEM : includes
    PRODUCT-CATEGORY ||--|{ PRODUCT : contains
    PRODUCT ||--o{ ORDER-ITEM : "ordered in"
```

[![](https://mermaid.ink/img/pako:eNqtUstuwjAQ_BXLJyqRS9tTbmkwKIJAlQROliw3XsASsStjR0KQf6-T8GzVU7vywfuY3Rl7j7jUAnCIgyCgykq7gxBlUZwsUBTHi-W8yBHJ0CiJJlkWpVT5OkQVmJHkG8MrqpC3SylL5gWZZFFBcnQ6BYE-3rqEiGJeltopy6SguEemJH0jmcetkoKgRv_ESFVLC4J9HC6Ya_rY-605JwXy533qISMyjpazoguyDXi23AKrXwdPlxat9bfmdwV_a99BboLRePow8FH4P4y6vZMfhb4lLSje03hUPfMskpitSJYni_k9jZqbcssNqsHspVZMuaqndE4MXp6vHBo8xBWYikvhN6lrQrHdQgUUt18oYM3dzrblbSl3VucHVeLQGgdDbLTbbHG45ru999yn8BrP63WNgpBWm7Tf1W5lmy9XC9HT?type=png)](https://mermaid.live/edit#pako:eNqtUstuwjAQ_BXLJyqRS9tTbmkwKIJAlQROliw3XsASsStjR0KQf6-T8GzVU7vywfuY3Rl7j7jUAnCIgyCgykq7gxBlUZwsUBTHi-W8yBHJ0CiJJlkWpVT5OkQVmJHkG8MrqpC3SylL5gWZZFFBcnQ6BYE-3rqEiGJeltopy6SguEemJH0jmcetkoKgRv_ESFVLC4J9HC6Ya_rY-605JwXy533qISMyjpazoguyDXi23AKrXwdPlxat9bfmdwV_a99BboLRePow8FH4P4y6vZMfhb4lLSje03hUPfMskpitSJYni_k9jZqbcssNqsHspVZMuaqndE4MXp6vHBo8xBWYikvhN6lrQrHdQgUUt18oYM3dzrblbSl3VucHVeLQGgdDbLTbbHG45ru999yn8BrP63WNgpBWm7Tf1W5lmy9XC9HT)
