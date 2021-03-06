from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, AvailabilityForm, MainCaptionForm, SubCaptionForm
from app.models import User, CarouselPhoto, Photo
from werkzeug.urls import url_parse


#@login_required
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    # TODO: find a better way of doing this
    # get id's of photos to be displayed in carousel
    carouselphotos = CarouselPhoto.query.all()
    photos = []
    for photo in carouselphotos:
        photos.append(Photo.query.get(photo.photo_id))
    startingPhotoID = photos[1].id


    availabilityForm = AvailabilityForm()

    if availabilityForm.validate_on_submit():
        flash("Availability form submitted", "alert-info")

    return render_template('index.html', title="Homepage", photos=photos, startingPhoto=startingPhotoID, availabilityForm=availabilityForm)


@app.route('/login', methods=["GET", "POST"])
def login():
    # redirect to homepage if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        # get user from database
        user = User.query.filter(User.username.ilike(form.username.data)).first()

        # validate username and password, redirect to login if invalid
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "alert-danger")
            return redirect(url_for("login"))

        # valid credentials, login user
        login_user(user, remember=form.remember_me.data)

        # redirect users to appropriate page
        next_page = request.args.get("next")

        # validate next_page, set to index if invalid
        # url_parse netloc check ensures next_page url is relative, so avoid
        # malicious redirects
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)

    return render_template('login.html', form=form, title="Sign in")


@app.route('/logout')
def logout():
    logout_user()
    # redirect users to appropriate page
    next_page = request.args.get("next")

    # validate next_page, set to index if invalid
    # url_parse netloc check ensures next_page url is relative, so avoid
    # malicious redirects
    if not next_page or url_parse(next_page).netloc != "":
        next_page = url_for("index")

    return redirect(next_page)


@app.route('/register', methods=["GET", "POST"])
def register():
    # redirect to homepage if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        newuser = User(username=form.username.data, email=form.email.data)
        newuser.set_password(form.password.data)
        db.session.add(newuser)
        db.session.commit()

        flash("Registration successful, you may now login.", "alert-success")

        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route('/adminhome', methods=["GET", "POST"])
def adminhome():
    # Redirect unauthorized used to homepage
    if not current_user.is_authenticated:
        flash("You may not access this section", "alert-danger")
        return redirect(url_for("index"))

    if not current_user.is_admin:
        flash("You may not access this section", "alert-danger")
        return redirect(url_for("index"))

    # get id's of photos currently in the carousel on the homepage
    carouselphotos = CarouselPhoto.query.all()
    photos = []
    for photo in carouselphotos:
        photos.append(Photo.query.get(photo.photo_id))

    # TODO: combine both the forms below - wtform is a struggle
    # Main Caption form
    main_caption_form = MainCaptionForm();
    if main_caption_form.validate_on_submit():
        # Get the photo to change
        photo = Photo.query.get(main_caption_form.whichPic.data)

        # Deal with no photo found
        if photo is None:
            flash("Photo not found in database. Contact an admin with code P=" + main_caption_form.whichPic.data, "alert-warning")
            return redirect(url_for("adminhome"))

        # Change main caption
        photo.main_caption = main_caption_form.caption.data
        db.session.commit()

        flash("Caption changed successfully.", "alert-success")
        return redirect(url_for("adminhome"))

    # Sub Caption form
    sub_caption_form = SubCaptionForm();
    if sub_caption_form.validate_on_submit():
        # Get the photo to change
        photo = Photo.query.get(sub_caption_form.whichPic.data)

        # Deal with no photo found
        if photo is None:
            flash("Photo not found in database. Contact an admin with code P=" + sub_caption_form.whichPic.data,
                  "alert-warning")
            return redirect(url_for("adminhome"))

        # Change main caption
        photo.sub_caption = sub_caption_form.caption.data
        db.session.commit()

        flash("Caption changed successfully.", "alert-success")
        return redirect(url_for("adminhome"))

    return render_template("adminhome.html", title="Admin Dashboard", photos=photos, numphotos=len(photos), \
                           maincapform=main_caption_form, subcapform=sub_caption_form)


@app.route('/bookings')
def bookings():
    return render_template("bookings.html", title="Bookings")


@app.route('/offers')
def offers():
    return render_template("offers.html", title="Offers")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Gallery")


@app.route('/contact')
def contact():
    return render_template("contactus.html", title="Contact Us")
