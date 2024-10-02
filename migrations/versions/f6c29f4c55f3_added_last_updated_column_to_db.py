"""Added Last updated column to db

Revision ID: f6c29f4c55f3
Revises: 
Create Date: 2024-01-10 22:43:09.078593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6c29f4c55f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('passwords', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('passwords', schema=None) as batch_op:
        batch_op.drop_column('last_updated')

    # ### end Alembic commands ###
