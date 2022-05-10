"""
    Creates the question view.
"""
from re import A
from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user
from wtforms import Form, SubmitField, TextAreaField, BooleanField, SelectField, StringField
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
    comment_submit = SubmitField('Submit')


class QuestionEditForm(Form):
    class Meta:
        locales = ['en_US', 'en']
    title = StringField(
        'Edit Title',
        validators=[DataRequired(
            'Please enter a title')])
    content = TextAreaField(
        'Edit Question Content',
        validators=[
            DataRequired(
                'Please enter a question content')])
    difficulty = SelectField(
        'Edit Difficulty',
        choices=[(1, "Easy"), (2, "Medium"), (3, "Hard")],
        coerce=int,
        validators=[DataRequired(
            'Please select a difficulty')])

    question_edit_submit = SubmitField('Submit')


@bp.route('/<question_uuid>', methods=['GET', 'POST'])
def question(course_code, question_uuid, new_comment_uuid=None):
    new_comment_uuid = (request.args.get('new_comment_uuid'))
    question = Question.query.filter_by(uuid=question_uuid).first()
    course = Course.query.filter_by(code=course_code).first()
    if current_user.is_anonymous:
        return render_template(
            'main/question.html', course=course, question=question,
            new_comment_uuid=new_comment_uuid)
    comment_form = CommentForm(request.form)

    question_edit_form = QuestionEditForm(request.form)

    user = User.query.filter_by(uuid=current_user.uuid).first()

    if request.method == 'POST':
        if comment_form.comment_submit.data == True and comment_form.validate():
            content = comment_form.content.data
            is_suggestion = comment_form.is_suggestion.data
            comment = Comment(
                content=content, is_suggestion=is_suggestion, user=user, question=question)

            db.session.add(comment)
            db.session.commit()

            return redirect(url_for(
                'question.question', course_code=course_code,
                comment_form=comment_form, question_edit_form=question_edit_form,
                question_uuid=question_uuid, new_comment_uuid=str(comment.uuid)))

        if question_edit_form.question_edit_submit.data == True and question_edit_form.validate():
            question.title = question_edit_form.title.data
            question.content = question_edit_form.content.data
            question.difficulty = "Easy" if question_edit_form.difficulty.data == 1 \
                else "Medium" if question_edit_form.difficulty.data == 2 else "Hard"
            print(question)
            db.session.commit()
            return redirect(url_for(
                'question.question', course_code=course_code,
                comment_form=comment_form, question_edit_form=question_edit_form,
                question_uuid=question_uuid))

    question_edit_form.title.default = question.title
    question_edit_form.content.default = question.content
    question_edit_form.difficulty.default = question.difficulty
    question_edit_form.process()

    return render_template(
        'main/question.html', course=course, question=question,
        question_edit_form=question_edit_form, comment_form=comment_form,
        new_comment_uuid=new_comment_uuid)
