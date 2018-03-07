"""add a column content_summary in table posts

Revision ID: 074177278e20
Revises: 64ea34e32b40
Create Date: 2018-03-06 15:32:58.878812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '074177278e20'
down_revision = '64ea34e32b40'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('content_summary', sa.Text()))


def downgrade():
    with op.batch_alter_table('post') as batch_op:
        batch_op.drop_column('content_summary')
