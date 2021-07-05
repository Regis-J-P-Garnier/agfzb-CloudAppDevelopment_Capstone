from django.db import models
from django.utils.timezone import now
from django.template.defaultfilters import default


class CarMake(models.Model):
    id=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(null=False, max_length=100)
    description = models.TextField()
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description   


class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    SPORT = 'SPORT'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
        (SPORT, 'SPORT')
    ]
    id=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    make=models.ForeignKey(CarMake, on_delete=models.CASCADE) 
    dealerId=models.IntegerField()
    name = models.CharField(null=False, max_length=100)
    type = models.CharField(null=False, max_length=100, default=SEDAN, choices=CAR_TYPES)
    year = models.DateField(default=now, blank=True) # return .year
    def __str__(self):
        return str( self.make.name) +" "+ self.name +" "+str( self.year.year)+ "," + self.type + ", from " + str(self.dealerId) # upgrade with dealers name ??
        
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment=None, id=None):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Reviewer name: " + self.name  + ", " + "Reviaw: " + self.review
    
    
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
       
        self.address = address # Dealer address
        self.city = city # Dealer city
        self.full_name = full_name # Dealer Full Name
        self.id = id # Dealer id
        self.lat = lat # Location lat
        self.long = long # Location long
        self.short_name = short_name # Dealer short name
        self.st = st # Dealer state
        self.zip = zip # Dealer zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
