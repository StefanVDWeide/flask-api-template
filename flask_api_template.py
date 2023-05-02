from datetime import datetime

from dateutil.relativedelta import relativedelta

from app import create_app, db

app = create_app()


@app.cli.command()
def remove_old_jwts():
    """
    Scan the database for JWT tokens in the Revoked Token table older than 5 days
    and remove them.
    """

    # Import within the function to prevent working outside of application context
    # when calling flask --help
    from app.models import RevokedTokenModel

    delete_date = datetime.utcnow() - relativedelta(days=5)

    old_tokens = (
        db.session.query(RevokedTokenModel)
        .filter(RevokedTokenModel.date_revoked < delete_date)
        .all()
    )

    if old_tokens:
        for token in old_tokens:
            db.session.delete(token)

        db.session.commit()

        print(
            "{} old tokens have been removed from the database".format(len(old_tokens))
        )

    else:
        print("No JWT's older than 5 days have been found")

    return old_tokens
