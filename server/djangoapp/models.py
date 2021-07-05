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


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
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
        

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
