# import from DRF
from rest_framework import serializers

# Local Import
from .models import Student


#validators
def start_with_r(value):
      if value[0].lower()!='r':
        raise serializers.ValidationError("Name doesn't start with R")


class StudentSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(read_only= True) # we can define fields also,
    # the name field is set as read_only, we cannot change this.
    # rest of the fields will be changed

    # Validators


    name = serializers.CharField(validators=[start_with_r])  # applying validation on particular field, this will pass the value of name field to start_with_r() for validation

    class Meta:
        model = Student
        fields = ['id','name','roll','city'] # required fields
        # read_only_fields = ['name','roll'] # these fields will be read_only and will not change during update
        # extra_kwargs = {'name':{'read_only':True}} # we can write like this also

    # we can also do field level and object level validation like in normal Serializer class class
    # field level validation in ModelSerilizer
    def validate_roll(self,value):
        print("In Validating Value...")
        if value > 200:
            raise serializers.ValidationError("Seat Full")
        return value

    # object level validation in ModelSerilizer
    def validate(self, data):
        print("Running Validate Func")
        nm = data.get('name')
        ct = data.get('city')
        if nm.lower() == 'veeru' and ct.lower() !='ranchi':
            raise serializers.ValidationError("City must be Ranchi")

        return data



'''
below is the implementation of normal Serializer, in which we have to declare each field correspond to the moded
and create and update method for database and validators for validations.
But in above, Using ModelSerilizer, we don't have to do all these things.
Same thing we can achieve using ModelSerializer



#    Priority: 1- Validators, 2-Field Level Validation 3- Object Level Validation

# Validators
def start_with_r(value):
    if value[0].lower()!='r':
        raise serializers.ValidationError("Name doesn't start with R")

def roll_num_check(value):
    if int(value) > 100:
        raise serializers.ValidationError("Seats Full")

class StudentSerializer(serializers.Serializer):
    # id = serializers.IntegerField() # to get id along with, otherwise id wil not be returned
    name = serializers.CharField(max_length=50, validators=[start_with_r]) # applying validation on particular field, this will pass the value of name field to start_with_r() for validation
    roll = serializers.IntegerField(validators=[roll_num_check])
    city = serializers.CharField(max_length=50)
   # state = serializers.CharField(max_length=50), error, Original exception text was: 'Student' object has no attribute 'state'.

    # Will be called when we run .save() on serializer object in post request
    def create(self,validate_data):
        return Student.objects.create(**validate_data)

    # Will be called when we run .save() on serializer object in post request
    def update(self,instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        print(instance.roll)
        instance.roll = validated_data.get('roll', instance.roll)
        print(instance.roll)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance


    # field level validation, value parameter corresponds to the value passed to roll attribute
    # this method will be invoked with is_valid() method in serializer object
    def validate_roll(self,value):
        print("In Validating Value...")
        if value > 200:
            raise serializers.ValidationError("Seat Full")
        return value

    # object level validation
    # data contains all field of model
    # this method will be invoked with is_valid() method in serializer object
    def validate(self, data):
        print("Running Validate Func")
        nm = data.get('name')
        ct = data.get('city')
        if nm.lower() == 'Rohit' and ct.lower() =='ranchi':
            raise serializers.ValidationError("City must be Ranchi")

        return data

'''