from apps import db

class FileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_path(cls, path):
        return cls.query.filter_by(path=path).first()