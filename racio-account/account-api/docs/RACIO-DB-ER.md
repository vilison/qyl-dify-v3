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
        string name "VARCHAR"
        string email 
        string phone 
        string account_role 
        string password  
        string password_salt  
        string avatar 
        string interface_language 
        string interface_theme  
        string timezone  
        timestamp last_login_at 
        string last_login_ip 
        timestamp last_active_at
        string status "active"
        timestamp initialized_at
        timestamp created_at
        timestamp updated_at
    }
    ACCOUNTS_INTEGRATES {
        uuid id PK "DEFAULT uuid_generate_v4()"
        uuid account_id FK
        string provider 
        string open_id 
        string encrypted_token
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP(0)"
        timestamp updated_at "DEFAULT CURRENT_TIMESTAMP(0)"
    }
    MEMBER_INVITE {
        uuid id PK "DEFAULT uuid_generate_v4()"
        uuid invited_by FK 
        uuid tenant_id "NULL"
        string role
        string remark "DEFAULT ''"
        string domain "DEFAULT ''"
        timestamp created_at "DEFAULT CURRENT_TIMESTAMP(0)"
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

[![](https://mermaid.ink/img/pako:eNqtVV9vmzAQ_yqWX5pKjTRte8obS2iHGpKKkDwhoRtciFWwkTmY0jbffQaaQgepJnUWL9zvj3znO_uZRypGPuPT6TSQJCjFGfOsubNm1ny-3q78DbM9tnCsO8-z3EAaHgsk6oWAREMWSGbWmRo6K9--8yzf3rCXl-lUPXcuMxZwiCJVSgpFHPBW6druD9szup3j2-ykhhohK0EYh7-OZ80b_Nz-16ssRczM93BvJAv71tou_SYYJmh2C4Rh9X1yfbaoV0FayIRJyNBodpY3_2l5IwTMQKRsEM4PSuIwfE5Rq3QEzaEofisds8tQWEBKIzhUQKCHcSEJ9R4iDFOQSQkJfsShA5p0hwwSGT7VCfWgOlYQZDlLoaAwVYmQIdBQ3INFftkAIhIVGoeBgSFRWTQNUlP6h9B5CClIQCqeTDP0PTpGpBHoIlrm8Tv0dLl3P9dYjaRrdXZ7PzxsrSoR48hxqhxlLRq2oYz0Ma8TIPWI8uP8e3udbz3PXvmh77j2xrfch8mX6_ECdwX6R_lpbIb_Q-26kTe1Y3-BhBLaugZ8tV0uRya2nr1h0Myxfuxt5OpqRBorM-3yIusTtT6329JUy5mHO9vbOOtVv1wV6OhgRrxCXQglQ1lmbelegcm3r50bv-EZarPZ2FzejUnAm-EOeH1rxriHMqWaXlOhJLU5yojPSJd4w7UqkwOf7SEtzF978K83-lsUY0FKu-3z0LwSpz-TQ-Pf?type=png)](https://mermaid.live/edit#pako:eNqtVV9vmzAQ_yqWX5pKjTRte8obS2iHGpKKkDwhoRtciFWwkTmY0jbffQaaQgepJnUWL9zvj3znO_uZRypGPuPT6TSQJCjFGfOsubNm1ny-3q78DbM9tnCsO8-z3EAaHgsk6oWAREMWSGbWmRo6K9--8yzf3rCXl-lUPXcuMxZwiCJVSgpFHPBW6druD9szup3j2-ykhhohK0EYh7-OZ80b_Nz-16ssRczM93BvJAv71tou_SYYJmh2C4Rh9X1yfbaoV0FayIRJyNBodpY3_2l5IwTMQKRsEM4PSuIwfE5Rq3QEzaEofisds8tQWEBKIzhUQKCHcSEJ9R4iDFOQSQkJfsShA5p0hwwSGT7VCfWgOlYQZDlLoaAwVYmQIdBQ3INFftkAIhIVGoeBgSFRWTQNUlP6h9B5CClIQCqeTDP0PTpGpBHoIlrm8Tv0dLl3P9dYjaRrdXZ7PzxsrSoR48hxqhxlLRq2oYz0Ma8TIPWI8uP8e3udbz3PXvmh77j2xrfch8mX6_ECdwX6R_lpbIb_Q-26kTe1Y3-BhBLaugZ8tV0uRya2nr1h0Myxfuxt5OpqRBorM-3yIusTtT6329JUy5mHO9vbOOtVv1wV6OhgRrxCXQglQ1lmbelegcm3r50bv-EZarPZ2FzejUnAm-EOeH1rxriHMqWaXlOhJLU5yojPSJd4w7UqkwOf7SEtzF978K83-lsUY0FKu-3z0LwSpz-TQ-Pf)