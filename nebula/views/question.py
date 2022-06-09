"""
    Creates the question view.
"""
import json
from urllib.parse import urlparse

from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user
from wtforms import Form, SubmitField, TextAreaField, BooleanField, SelectField, StringField, HiddenField
from wtforms.validators import DataRequired, Optional
from nebula import db
from nebula.models import Course, Question, Comment, User, Answer, SubjectTag

bp = Blueprint('question', __name__,
               url_prefix='/q/<course_level_code>/<course_code>')


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
    subject_tags = HiddenField(
        "Subject Tags (optional)", validators=[Optional()])
    difficulty = SelectField(
        'Edit Difficulty',
        choices=[(1, "Easy"), (2, "Medium"), (3, "Hard")],
        coerce=int,
        validators=[DataRequired(
            'Please select a difficulty')])

    question_edit_submit = SubmitField('Submit')


class AnswerForm(Form):
    class Meta:
        locales = ['en_US', 'en']
    content = TextAreaField('Answer content', validators=[
        DataRequired()])
    sources = TextAreaField('Add sources', validators=[
        Optional()])

    add_answer_submit = SubmitField('Submit')


@ bp.route('/<question_uuid>', methods=['GET', 'POST'])
def question(course_code, question_uuid, course_level_code, new_comment_uuid=None, edit=None):
    new_comment_uuid = (request.args.get('new_comment_uuid'))
    question = Question.query.filter_by(uuid=question_uuid).first()
    edit = request.args.get('edit')
    if edit is not None and edit.lower() == 'true':
        edit = True
    else:
        edit = False
    course = Course.query.filter_by(code=course_code).first()
    if current_user.is_anonymous:
        return render_template(
            'main/question.html', course=course, question=question,
            new_comment_uuid=new_comment_uuid)
    comment_form = CommentForm(request.form)

    question_edit_form = QuestionEditForm(request.form)
    add_answer_form = AnswerForm(request.form)

    user = User.query.filter_by(uuid=current_user.uuid).first()

    if request.method != 'POST':

        question_edit_form.title.default = question.title
        question_edit_form.content.default = question.content
        question_edit_form.difficulty.default = question.difficulty
        question_edit_form.subject_tags.default = json.dumps(
            [tag.name for tag in question.subject_tags])
        question_edit_form.process()

        return render_template(
            'main/question.html', course=course, question=question,
            question_edit_form=question_edit_form, comment_form=comment_form,
            new_comment_uuid=new_comment_uuid, add_answer_form=add_answer_form, edit=edit)

    # POST

    if comment_form.comment_submit.data == True and comment_form.validate():
        if (current_user.is_anonymous):
            flash('You must be logged in to comment', 'warning')
            return redirect(url_for('main.login'))

        content = comment_form.content.data.strip()
        is_suggestion = comment_form.is_suggestion.data
        comment = Comment(
            content=content, is_suggestion=is_suggestion, user=user, question=question)

        db.session.add(comment)
        db.session.commit()

        flash('Comment added', 'success')
        return redirect(url_for(
            'question.question', course_code=course_code, course_level_code=course_level_code,
            question_uuid=question_uuid, new_comment_uuid=str(comment.uuid)))

    if question_edit_form.question_edit_submit.data == True and question_edit_form.validate():
        if (current_user.is_anonymous or (current_user != question.user and current_user.access_level <= 2)):
            flash('You must be the owner of the question to edit it', 'warning')
            return redirect(url_for('question.question', course_code=course_code,
                                    course_level_code=course_level_code, question_uuid=question_uuid))
        question.title = question_edit_form.title.data.strip()
        question.content = question_edit_form.content.data.strip()

        subject_tags = []
        if question_edit_form.subject_tags.data != "":
            for tag in json.loads(question_edit_form.subject_tags.data):
                tag = tag.strip()
                if not tag:
                    continue
                existing_tag = SubjectTag.query.filter(
                    SubjectTag.name.ilike(tag)).one_or_none()
                if existing_tag is None:
                    subject_tags.append(SubjectTag(name=tag))
                    print("Added not existing tag: " + tag)
                    continue
                subject_tags.append(existing_tag)
        question.subject_tags = subject_tags

        question.difficulty = "Easy" if question_edit_form.difficulty.data == 1\
            else "Medium" if question_edit_form.difficulty.data == 2 else "Hard"
        db.session.commit()
        flash('Question edited successfully', 'success')
        return redirect(url_for(
            'question.question', course_code=course_code, course_level_code=course_level_code,
            question_uuid=question_uuid))

    if add_answer_form.add_answer_submit.data == True and add_answer_form.validate():
        if (current_user.is_anonymous):
            flash('You must be logged in to answer a question', 'warning')
            return redirect(url_for('main.login'))
        content = add_answer_form.content.data.strip()
        sources = [
            urlparse(source, scheme="https", allow_fragments=True).geturl().replace("///", "//") for source in add_answer_form.sources.data.split(";") if source]
        answer = Answer(
            content=content, sources=sources, user=user, question=question)
        db.session.add(answer)
        db.session.commit()
        flash('Your answer has been submitted and is awaiting review', 'success')
        return redirect(url_for('question.question', course_code=course_code, course_level_code=course_level_code, question_uuid=question_uuid))
