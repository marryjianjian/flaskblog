"""add a column

Revision ID: 64ea34e32b40
Revises: f7428eea438e
Create Date: 2018-02-13 23:21:38.541554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64ea34e32b40'
down_revision = 'f7428eea438e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('up_date', sa.DateTime))


def downgrade():
    with op.batch_alter_table('post') as batch_op:
        batch_op.drop_column('up_date')
