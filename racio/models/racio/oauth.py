import time
from sqlalchemy.dialects.postgresql import UUID
from extensions.ext_database import db
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)

class OAuth2Client(db.Model, OAuth2ClientMixin):
    __bind_key__ = 'racio_db'
    __tablename__ = 'oauth2_client'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(UUID, db.ForeignKey('accounts.id', ondelete='CASCADE'))
    account = db.relationship('Account')


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __bind_key__ = 'racio_db'
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(UUID, db.ForeignKey('accounts.id', ondelete='CASCADE'))
    account = db.relationship('Account')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __bind_key__ = 'racio_db'
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(UUID, db.ForeignKey('accounts.id', ondelete='CASCADE'))
    account = db.relationship('Account')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()
