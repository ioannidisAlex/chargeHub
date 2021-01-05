from django.db import models

class Payment(models.Model):
    _paymentMethods = [
        ('credit_card','credit card'),
        ('cash','cash'),
        ('paypal','paypal'),
        ('coupon','coupon')
    ]
    
    payment_req = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length = 20,
        choices = _paymentMethods, 
        default = 'cash'
    )
    cost = models.FloatField(blank = True)
    invoice = models.CharField(max_length = 100)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    session_id = models.OneToOneField(Session,on_delete=models.CASCADE)

    def __str__(self):
        return (self.session_id, self.user_id)


class Session(models.Model):
    id = models.CharField(max_lenght=100)
    user_comments_ratings = models.TextField()
    cluster_id = models.CharField(max_length=100)   #potential fk
    kwh_delivered = models.IntegerField()
    site_id = models.CharField(max_lenth=100)
    connect_time = models.DateTimeField()
    disconnect_time = models.DateTimeField()
    done_charging_time = models.DateTimeField()
    charging_point_id = models.ForeignKey(ChargingPoint, on_delete=models.SET_NULL)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_NULL)

    def __str__(self):
        return (self.vehicle_id, self.charging_point_id,self.connect_time,self.kwh_delivered)




    
