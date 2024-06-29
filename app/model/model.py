# model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(250), default="user", nullable=False)


class ClientList(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    public_id = Column(String(200))
    url = Column(String(200))


class AboutSlide(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    public_id = Column(String(200))
    url = Column(String(200))


class YoutubeVideosLinks(db.Model):
    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)


class SlideVideoDb(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    public_id = Column(String(200))
    url = Column(String(200))


class SliderDb(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    public_id = Column(String(200))
    url = Column(String(200))


class ActionHistory(db.Model):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    action = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(200))
    description = Column(String(500))

    def log_action(self, action, description):
        new_action = ActionHistory(
            action=action,
            description=description
        )
        db.session.add(new_action)
        db.session.commit()


class AppliedJob(db.Model):
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, db.ForeignKey('job.id'), nullable=False)
    first_name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    applicant_email = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)
    cv_path = Column(String(255), nullable=False)

    job = db.relationship('Job', backref='applied_jobs')

    def log_action(self, action, description):
        new_action = ActionHistory(
            action=action,
            description=description
        )
        db.session.add(new_action)
        db.session.commit()


class Job(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    requirements = Column(String(500), nullable=False)
    deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)

    def log_action(self, action, description):
        new_action = ActionHistory(
            action=action,
            description=description
        )
        db.session.add(new_action)
        db.session.commit()


class BlogPost(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)


class Event(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String(100), nullable=False)


class NewsArticle(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    author = Column(String(50), nullable=False)


class TeamMember(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    job_title = Column(String(50), nullable=False)
    photo_url = Column(String(200))

    def __repr__(self):
        return f"TeamMember(id={self.id}, name='{self.name}', job_title='{self.job_title}')"
