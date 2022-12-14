from django.contrib import messages


def loginController(req):
    from django.contrib.auth import authenticate, login
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
        messages.success(req, f"{username} successfully loggedin!")
        context = {'status': True}
        return context

    messages.error(req, 'Please provide correct details.')
    context = {'status': False}
    return context


def userRegisterController(req):
    from home.forms import UserRegisterForm
    form = UserRegisterForm(req.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(req, f"Account created for {username}!")
        context = {"status": True}
        return context

    for error in form.errors:
        messages.error(req, error + " " + form.errors[error])
    context = {"status": False}
    return context


def companyRegisterController(req):
    from home.forms import CompanyRegisterForm
    import json

    form = CompanyRegisterForm(req.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(req, f"Account created for {username}!")
        context = {"status": True, "form": form}
        return context

    for errorLabel in form.errors:
        message = errorLabel + " - "
        errorMessages = json.loads(form.errors[errorLabel].as_json())
        for errorMessage in errorMessages:
            message += errorMessage['message'] + " "
        print(message)
        messages.error(req, message)
    context = {"status": False, "form": form}
    return context


def indexController(req):
    from home.models import Jobposting
    jobPostings = Jobposting.objects.all()
    context = {"status": True,
               "image": req.user.userprofile.image, "jobs": jobPostings}
    return context
