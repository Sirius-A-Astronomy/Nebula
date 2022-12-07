from flask import abort, url_for

from nebula import db
from nebula.models import (
    Answer,
    Comment,
    Course,
    Notification,
    Question,
    SubjectTag,
    Subscription,
    User,
)


class QuestionController:
    def __init__(self, question):
        self.question = question

    @staticmethod
    def get_question(question__uuid, abort_if_not_found=True):
        question = Question.query.filter_by(uuid=question__uuid).first()
        if question is None:
            if abort_if_not_found:
                abort(404)
            else:
                return None
        return question

    @staticmethod
    def get_questions_by_course(course_code, abort_if_not_found=True):
        questions = Course.query.filter_by(code=course_code).first().questions

        if questions is None:
            if abort_if_not_found:
                abort(404)
            else:
                return None
        return questions

    @staticmethod
    def create_question(title, content, user, **kwargs):
        question = Question(title, content, user, **kwargs)
        db.session.add(question)
        db.session.add(Subscription(user, question))
        db.session.commit()

        return question

    def add_comment(self, content, user, **kwargs):
        comment = Comment(content, user, self.question, **kwargs)
        db.session.add(comment)
        db.session.commit()

        # Notify subscribers of the question
        for subscription in Question.subscriptions:
            for user in subscription.users:
                if subscription.user == self.question.user:
                    notification = Notification(
                        user=subscription.user,
                        content=f"{user.name} commented on your question: {self.question.title}",
                        link=url_for(
                            "question.question",
                            course_code=self.question.course.code,
                            course_level_code=self.question.course_level.code,
                            question_uuid=self.question.uuid,
                        ),
                    )
                    db.session.add(notification)
                    db.session.commit()
                else:
                    notification = Notification(
                        user=subscription.user,
                        content=f"{user.name} commented on a question you subscribed to: {self.question.title}",
                        link=url_for(
                            "question.question",
                            course_code=self.question.course.code,
                            course_level_code=self.question.course_level.code,
                            question_uuid=self.question.uuid,
                        ),
                    )
                    db.session.add(notification)
                    db.session.commit()
        return comment
