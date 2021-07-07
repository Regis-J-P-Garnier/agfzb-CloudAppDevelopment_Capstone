from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_review_request_to_cf, get_dealer_by_id
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
            #return render(request, 'djangoapp/dealer_details.html', context)
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
    """ retrieve and presents data of dealers """
    context={}
    if request.method == "GET":
        context["dealership_list"] = get_dealers_from_cf(state) # Get dealers from the URL  
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships]) # Concat all dealer's short name
        #return HttpResponse(dealer_names) # Return a list of dealer short name
    return render(request, 'djangoapp/index.html', context)    


def get_reviews(request,dealer_id=0):
    """ retrieve and presents data of reviews """
    context={}    
    if request.method == "GET":
        context["review_list"] = get_dealer_reviews_from_cf(dealer_id)
        context["dealer"] = get_dealer_by_id(dealer_id)
        if  len(context["review_list"]) == 0:
            context["review_list_is_empty"]=True
        else:
            context["review_list_is_empty"]=False
        #reviews from the URL  
        #reviewers_names = ' '.join([review.name for review in reviews]) # Concat all reviewers's name
        #return HttpResponse(reviewers_names) # Return a list of reviewers short name
    return render(request, 'djangoapp/dealer_details.html', context)   

def add_review(request, dealer_id):
        context={} 
        context["dealer_id"]  = dealer_id  
        if request.method == "GET":
            context["dealer"] = get_dealer_by_id(dealer_id)
            context["cars"] = CarModel.objects.filter(dealerId=dealer_id) # REFACTOR : name of delear ID somewhere
            
            return render(request, 'djangoapp/add_review.html', context) 
        if request.method == "POST":
            user = request.user
            if user.is_authenticated:
                json_payload_dict={}
                review={}
                #required fields
                review["name"] = user.username
                review["dealership"] = dealer_id
                #review["purchase"]=request.POST["purchasecheck"]
                checked_values = request.POST.getlist("purchasecheck")
                if len(checked_values)==1:
                    review["purchase"]= True
                else:
                    review["purchase"]= False
                review["review"]=request.POST["content"]# REFACTOR : rename in HTML form
                #optionals
                car_object=CarModel.objects.filter(id=request.POST["car"])
                review["car_make"]=car_object[0].name
                review["car_model"]=car_object[0].type # REFACTOR : mode of type
                review["car_year"]=car_object[0].year.strftime("%Y")
                review["purchase_date"]=request.POST["purchasedate"]
                # out of form
                review["another"]=None
                # not persistant
                review["time"] = datetime.utcnow().isoformat()
                response = post_review_request_to_cf(review)
                #TODO error analysis
        return redirect("djangoapp:dealer_details", dealer_id)
            
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

