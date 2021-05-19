from app import db, ma, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# User loader function which uses the JWT identity to retrieve a user object. Method is called on protected routes
@jwt.user_lookup_loader
def user_loader_callback(identity):
    """[summary]

    Parameters
    ----------
    identity : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
    return Users.query.filter_by(id=identity).first()


# defines the Users database table
class Users(db.Model):
    """[summary]

    Parameters
    ----------
    db : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow())

    def set_password(self, password):
        """[summary]

        Parameters
        ----------
        password : [type]
            [description]
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """[summary]

        Parameters
        ----------
        password : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        return check_password_hash(self.password_hash, password)


# Defines the revoked token database (blacklisted) table
class RevokedTokenModel(db.Model):
    """[summary]

    Parameters
    ----------
    db : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        """[summary]"""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """[summary]

        Parameters
        ----------
        jti : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


# Create Users model schema so user table data can be returned as JSON object
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
