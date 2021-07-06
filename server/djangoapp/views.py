from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_review_request_to_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def about_request(request):
    context={}
    return render(request, 'djangoapp/about.html', context)

def contact_request(request):
    context={}
    return render(request, 'djangoapp/contact.html', context)
# ...
def index_request(request):
    context={}
    return  render(request, 'djangoapp/index.html', context)

def get_dealerships(request, state=None):
    """ for DEBUGING purpose """
    if request.method == "GET": 
        dealerships = get_dealers_from_cf(state) # Get dealers from the URL  
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships]) # Concat all dealer's short name
        return HttpResponse(dealer_names) # Return a list of dealer short name

def get_reviews(request,dealer_id=0):
    """ for DEBUGING purpose """
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(dealer_id)                         #reviews from the URL  
        reviewers_names = ' '.join([review.name for review in reviews]) # Concat all reviewers's name
        return HttpResponse(reviewers_names) # Return a list of reviewers short name

def add_review(request, dealer_id):
        review_done=""
        user = request.user
        if user.is_authenticated:
            json_payload_dict={}
            review ={}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = "BETA TESTER"
            review["dealership"] = 19
            review["purchase"]=True
            review["another"]=""
            review["purchase_date"]="2021-07-08"
            review["car_make"]="Ligier"
            review["car_model"]=""
            review["car_year"]="2021-01-01"
            review["review"]="revue du 2021-01-01"
            print(review)
            response = post_review_request_to_cf(review)
            print(response)
            review_done=response
        return HttpResponse(review_done)
            
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

