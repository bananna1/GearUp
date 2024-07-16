"""empty message

Revision ID: 9ec09c052841
Revises: 
Create Date: 2024-07-16 09:52:25.929567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ec09c052841'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gear',
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('gender', sa.CHAR(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('warmth', sa.String(), nullable=False),
    sa.Column('waterproof', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('huts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('photo reference', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('favourite_gear',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('gearid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['email'], ['users.email'], ),
    sa.ForeignKeyConstraint(['gearid'], ['gear.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trails',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start', sa.String(), nullable=False),
    sa.Column('hut', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hut'], ['huts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favourite_trails',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('trailid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['email'], ['users.email'], ),
    sa.ForeignKeyConstraint(['trailid'], ['trails.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favourite_trails')
    op.drop_table('trails')
    op.drop_table('favourite_gear')
    op.drop_table('users')
    op.drop_table('huts')
    op.drop_table('gear')
    # ### end Alembic commands ###