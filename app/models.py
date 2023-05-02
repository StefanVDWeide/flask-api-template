from app import db, jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import redis
import rq


@jwt.user_lookup_loader
def user_loader_callback(jwt_header: dict, jwt_data: dict) -> object:
    """
    HUser loader function which uses the JWT identity to retrieve a user object.
    Method is called on protected routes

    Parameters
    ----------
    jwt_header : dictionary
        header data of the JWT
    jwt_data : dictionary
        payload data of the JWT

    Returns
    -------
    object
        Returns a users object containing the user information
    """
    return Users.query.filter_by(id=jwt_data["sub"]).first()


# defines the Users database table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship("Posts", backref="user", lazy="dynamic")
    comments = db.relationship("Comments", backref="user", lazy="dynamic")
    tasks = db.relationship("Tasks", backref="user", lazy="dynamic")

    def set_password(self, password: str):
        """
        Helper function to generate the password hash of a user

        Parameters
        ----------
        password : str
            The password provided by the user when registering
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Helper function to verify the password hash agains the password provided
        by the user when logging in

        Parameters
        ----------
        password : str
            The password provided by the user when logging in

        Returns
        -------
        bool
            Returns True if the password is a match. If not False is returned
        """
        return check_password_hash(self.password_hash, password)

    def launch_task(self, name: str, description: str, **kwargs) -> object:
        """
        Helper function to launch a background task

        Parameters
        ----------
        name : str
            Name of the task to launch
        description : str
            Description of the task to launch

        Returns
        -------
        object
            A Tasks object containing the task information
        """
        rq_job = current_app.task_queue.enqueue(
            "app.tasks.long_running_jobs" + name, **kwargs
        )
        task = Tasks(
            task_id=rq_job.get_id(), name=name, description=description, user=self
        )
        db.session.add(task)

        return task

    def get_tasks_in_progress(self) -> list:
        """
        Helper function which retrieves the background tasks that are still in progress

        Returns
        -------
        list
            A list of Tasks objects
        """
        return Tasks.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name: str) -> object:
        """
        Helper function to retrieve a task in progress based on name

        Parameters
        ----------
        name : str
            name of the task to be retrieved

        Returns
        -------
        object
            A task object
        """
        return Tasks.query.filter_by(name=name, user=self, complete=False).first()

    def get_completed_tasks(self) -> dict:
        """
        Helper function to retrieve all completed tasks

        Returns
        -------
        dict
            A dictionary of Tasks objects
        """
        return Tasks.query.filter_by(user=self, complete=True).all()


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship("Comments", backref="post", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    date_revoked = db.Column(db.DateTime, default=datetime.utcnow)

    def add(self):
        """
        Helper function to add a JWT to the table
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        """
        Helper function to check if a JWT is in the Revoked Token table

        Parameters
        ----------
        jti : str
            The JWT unique identifier

        Returns
        -------
        bool
            Return True if the JWT is in the Revoked Token table
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(36), index=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)

        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None

        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get("progress", 0) if job is not None else 100
