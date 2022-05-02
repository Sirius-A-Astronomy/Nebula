"""
    Creates the question view.
"""
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user
from wtforms import Form, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired
from nebula import db
from nebula.models import Course, Question, Comment, User

bp = Blueprint('question', __name__,
               url_prefix='/course/<course_code>/question')


class CommentForm(Form):
    class Meta:
        locales = ['en_US', 'en']
    content = TextAreaField('Add a comment', validators=[
                            DataRequired()])
    is_suggestion = BooleanField('Comment is a suggestion')
    submit = SubmitField('Submit')


@bp.route('/<question_uuid>', methods=['GET', 'POST'])
def question(course_code, question_uuid, new_comment_uuid=None):
    new_comment_uuid = (request.args.get('new_comment_uuid'))

    comment_form = CommentForm(request.form)
    question = Question.query.filter_by(uuid=question_uuid).first()
    course = Course.query.filter_by(code=course_code).first()

    user = User.query.filter_by(uuid=current_user.uuid).first()
    if request.form and comment_form.validate():
        content = comment_form.content.data
        is_suggestion = comment_form.is_suggestion.data
        comment = Comment(
            content=content, is_suggestion=is_suggestion, user=user, question=question)

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('question.question', course_code=course_code,
                                question_uuid=question_uuid, new_comment_uuid=str(comment.uuid)))
    return render_template('main/question.html', course=course, question=question,
                           comment_form=comment_form, new_comment_uuid=new_comment_uuid)
