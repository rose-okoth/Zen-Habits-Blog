"""Added in the blog model structure

Revision ID: 592cbaeca506
Revises: 4f3b76d89807
Create Date: 2021-03-06 11:52:20.395308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '592cbaeca506'
down_revision = '4f3b76d89807'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('blog_title', sa.String(), nullable=True),
    sa.Column('blog_content', sa.String(length=1000), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('posted', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    # ### end Alembic commands ###
