from flask import (render_template, redirect, url_for, 
                   flash, request, abort, current_app, Blueprint)
from flask_login import current_user, login_required
from website.transcriptions.forms import SaveWTranscriptionForm, SaveDTranscriptionForm, PostForm
from website.models import User, Transcripts, Post
from website import db, share
import os

transcripts = Blueprint('transcripts', __name__)

@transcripts.route("/account/transcripts", methods=['GET', 'POST'])
@login_required
def account_transcripts():
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    transcript = Transcripts.query.filter_by(user_id=current_user.id)
    return render_template('account_transcripts.html', transcripts=transcript, image_file=image_file)

@transcripts.route('/account/transcriptions/<int:id>', methods=['GET', 'POST'])
def transcript(id):
    transcript = Transcripts.query.get_or_404(id)
    user = User.query.get_or_404(transcript.user_id)
    return render_template('transcript.html', transcript=transcript, share=share, user=user)

@transcripts.route('/account/transcriptions/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_transcript(id):
    transcript = Transcripts.query.get_or_404(id)
    if transcript.user_id != current_user.id:
        abort(403)
    form = SaveWTranscriptionForm()
    if form.validate_on_submit():
        with current_app.app_context():
            transcript.title = form.title.data
            transcript.content = form.content.data
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('transcripts.transcript', id=transcript.id))
    elif request.method == 'GET':
        form.title.data = transcript.title
        form.content.data = transcript.content
    return render_template('update_transcript.html', form=form)

@transcripts.route('/account/transcriptions/<int:id>/delete', methods=['POST'])
@login_required
def delete_transcript(id):
    transcript = Transcripts.query.get_or_404(id)
    if transcript.user_id != current_user.id:
        abort(403)
    db.session.delete(transcript)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))



@transcripts.route("/transcriptions/<f_name>", methods=["GET", "POST"])
@login_required
def transcriptions(f_name):
    w_form = SaveWTranscriptionForm()
    d_form = SaveDTranscriptionForm()
    dir_path = os.getcwd()
    deepspeech_transcription_path = f'{dir_path}/deepspeech_transcription/'
    for item in os.listdir(deepspeech_transcription_path):
            if item.endswith('.txt'):
                with open(str(deepspeech_transcription_path + item), 'r') as g:
                    deepspeech_text = g.read()
    whisper_transcription_path = f"{dir_path}/whisper_transcription/"
    for item in os.listdir(whisper_transcription_path):
        if item.endswith('.txt'):
            with open(str(whisper_transcription_path + item), "r") as f:
                whisper_text = f.read()
    if w_form.validate_on_submit():
        with current_app.app_context():
            transcript = Transcripts(title=w_form.title.data,
                                        content=w_form.content.data,
                                        user_id=current_user.id)
            db.session.add(transcript)
            db.session.commit()
            return redirect(url_for('users.account'))
    if d_form.validate_on_submit():
        with current_app.app_context():
            transcript = Transcripts(title=d_form.title.data,
                                        content=d_form.content.data,
                                        user_id=current_user.id)
            db.session.add(transcript)
            db.session.commit()
            return redirect(url_for('users.account'))
    elif request.method == "GET":
        w_form.title.data = f"Whisper: {f_name}"
        d_form.title.data = f"DeepSpeech: {f_name}"
        w_form.content.data = whisper_text
        d_form.content.data = deepspeech_text
    return render_template('transcriptions.html', whisper_form=w_form, deepspeech_form=d_form)

@transcripts.route("/blog")
def blog():
    posts = Post.query.filter_by(user_id=1)
    return render_template('blog.html', posts=posts)

@transcripts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        with current_app.app_context():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('transcripts.blog'))
    return render_template('create_post.html', form=form,
                           legend='New Post')

@transcripts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@transcripts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('transcripts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', post=post, 
                           form=form, legend='Update Post')


@transcripts.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('transcripts.blog'))