from django.db import models
import uuid
#class order
class Payment(models.Model):
    _PAYMENT_METHODS = [
        ('credit_card','credit card'),
        ('cash','cash'),
        ('paypal','paypal'),
        ('coupon','coupon')
    ]
    
    payment_req = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length = 20,
        choices = _PAYMENT_METHODS, 
        default = 'cash'
    )
    cost = models.FloatField(blank = True)
    invoice = models.CharField(max_length = 100)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    session_id = models.OneToOneField(Session,on_delete=models.CASCADE)

    def __str__(self):
        return str((self.session_id, self.user_id))


class Session(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user_comments_ratings = models.TextField()
    #cluster = models.CharField(max_length=100)   #potential fk Null
    kwh_delivered = models.IntegerField() #check type
    site_id = models.UUIDField(editable=False,default=uuid.uuid4)
    connect_time = models.DateTimeField(null = True)
    disconnect_time = models.DateTimeField(null = True)
    done_charging_time = models.DateTimeField(null = True)
    charging_point = models.ForeignKey(ChargingPoint, on_delete=models.SET_NULL,related_name="sessions")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL,related_name="sessions")

    def __str__(self):
        return str((self.vehicle_id, self.charging_point_id,self.connect_time,self.kwh_delivered))




    
