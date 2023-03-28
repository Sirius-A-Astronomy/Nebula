"""Make UUID non-nullable

Revision ID: adbbd3371037
Revises: 53300c80a02f
Create Date: 2023-03-28 12:15:49.811359

UUIDs should not be allowed to be null.
They already have a default value, so this should
not give any issues. This is just to make sure
that they can't accidentally be set to null.

"""
from alembic import op
import sqlalchemy as sa
import nebula


# revision identifiers, used by Alembic.
revision = 'adbbd3371037'
down_revision = '53300c80a02f'
branch_labels = None
depends_on = None


def upgrade():
    """
        Will fail with SQLite

        SQLite does not support ALTER TABLE <name> ALTER COLUMN.
    """

    op.alter_column('course_level', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('subject_tag', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('user', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('course', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('notification', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('question', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('answer', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('comment', 'uuid', nullable=False, existing_nullable=True)
    op.alter_column('subscription', 'uuid', nullable=False, existing_nullable=True)



def downgrade():
    op.alter_column('course_level', 'uuid', nullable=True)
    op.alter_column('subject_tag', 'uuid', nullable=True)
    op.alter_column('user', 'uuid', nullable=True)
    op.alter_column('course', 'uuid', nullable=True)
    op.alter_column('notification', 'uuid', nullable=True)
    op.alter_column('question', 'uuid', nullable=True)
    op.alter_column('answer', 'uuid', nullable=True)
    op.alter_column('comment', 'uuid', nullable=True)
    op.alter_column('subscription', 'uuid', nullable=True)
