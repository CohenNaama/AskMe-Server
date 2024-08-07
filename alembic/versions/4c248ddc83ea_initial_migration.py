"""Initial migration

Revision ID: 4c248ddc83ea
Revises: 
Create Date: 2024-07-07 01:50:26.612988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine


# revision identifiers, used by Alembic.
revision: str = '4c248ddc83ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Connect to the database engine
    engine = create_engine(op.get_bind().engine.url)
    inspector = Inspector.from_engine(engine)

    # Check if the 'inquiries' table exists
    if 'inquiries' not in inspector.get_table_names():
        # ### commands auto generated by Alembic - please adjust! ###
        op.create_table('inquiries',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
            sa.Column('question', sa.String(length=500), nullable=False),
            sa.Column('answer', sa.String(length=500), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_inquiries_answer'), 'inquiries', ['answer'], unique=False)
        op.create_index(op.f('ix_inquiries_created_at'), 'inquiries', ['created_at'], unique=False)
        op.create_index(op.f('ix_inquiries_question'), 'inquiries', ['question'], unique=False)
        # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_inquiries_question'), table_name='inquiries')
    op.drop_index(op.f('ix_inquiries_created_at'), table_name='inquiries')
    op.drop_index(op.f('ix_inquiries_answer'), table_name='inquiries')
    op.drop_table('inquiries')
    # ### end Alembic commands ###
