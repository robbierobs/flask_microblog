"""new fields in user model

Revision ID: 240098363b9b
Revises: 67fa86d2837c
Create Date: 2020-03-03 12:05:48.264372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '240098363b9b'
down_revision = '67fa86d2837c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###