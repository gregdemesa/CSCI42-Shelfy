from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Value, CharField
from django.db.models.functions import Concat

from user_library.models import UserLibraryItem


class AverageRatingView(ListView):
    model = UserLibraryItem
    template_name = "chartjs/index.html"

    def get_context_data(self, **kwargs): # from Django Book/ Lecture
        context = super().get_context_data(**kwargs) #overides the other get_context
        context['rating'] = UserLibraryItem.objects.raw("SELECT AVG(rating) FROM UserLibraryItem")
        return context
    
# class ReservationCreateView(LoginRequiredMixin, CreateView):
#     model = Reservation
#     template_name = "reservation_create.html"
#     form_class = ReservationForm

#     def form_valid(self, form):

#         previous_id = Reservation.objects.aggregate(Max('reservation_id'))['reservation_id__max']
#         real_id = previous_id + 1
#         form.instance.reservation_id = real_id #autoincrement
#         reservee = self.request.user.profile
#         form.instance.reservee_id = reservee
#         reservation = form.save()

#         #saving into reservationlocation:
#         venue = form.cleaned_data.get("venue")
#         reservation_location = Reservationlocation(reservation=reservation, venue=venue) #code wants the instance, and not the ids
#         reservation_location.save()

#         #saving into reservationreservee
#         reservee_id = self.request.user.profile.pk #getting the pk of the user
#         reservee_object = Reservee.objects.get(pk=reservee_id) #getting the object given the reservee_id of the user
#         reservation_reservee = Reservationreservee(reservation=reservation, reservee=reservee_object)
#         reservation_reservee.save()

#         #saving into reservationagent
#         agent_object = Venueagent.objects.get(venue=venue)
#         reservation_agent = Reservationagent(reservation=reservation, agent=agent_object.agent)
#         reservation_agent.save()

#         #saving into Reservationtimeslot
#         start_datetime = form.cleaned_data.get("start_datetime")
#         end_datetime = form.cleaned_data.get("end_datetime")
#         duration_base = end_datetime - start_datetime
#         hours, remainder = divmod(duration_base.seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         reservation_timeslot = Reservationtimeslot(reservation=reservation, duration=Concat(duration_base.days, Value(' days, '), hours, Value(' hours, '), minutes, Value(' minute'), output_field=CharField()))
#         reservation_timeslot.save()
        
#         return redirect('stateapp:search')
    

# class VenueListView(ListView):
#     model = Venue
#     template_name = "venues.html"

#     def get_context_data(self, **kwargs): # from Django Book/ Lecture
#         context = super().get_context_data(**kwargs) #overides the other get_context
#         #https://docs.djangoproject.com/en/5.1/topics/db/sql/#executing-custom-sql-directly
#         context['venueinformation'] = Venue.objects.raw("SELECT v.Venue_ID, v.Venue_Name, v.Venue_Type, vt.Venue_Capacity, a.Amenity_Type \
#                                                         FROM VENUE v, VENUETYPE vt, VENUEAMENITY va, AMENITY a \
#                                                         WHERE v.Venue_Type = vt.Venue_Type AND a.Amenity_ID = va.Amenity_ID AND v.Venue_ID = va.Venue_ID ORDER BY v.Venue_Name ;")
#         context['venuename'] = Venue.objects.raw("SELECT venue_id, venue_name FROM VENUE;")
#         context['venuetype'] = Venue.objects.raw("SELECT v.Venue_ID, v.Venue_Type, v.Venue_Name, b.Building_Name \
#                                                  FROM VENUE v, BUILDING b, VENUEBUILDING vb \
#                                                  WHERE v.Venue_ID = vb.Venue_ID AND b.Building_ID = vb.Building_ID \
#                                                  ORDER BY v.Venue_Type;")
#         context['distinctvenuetype']= Venuetype.objects.raw("SELECT venue_type FROM VENUETYPE;")
#         context['venuecontacts'] = Venue.objects.raw("SELECT DISTINCT v.Venue_ID, v.Venue_Name, CONCAT(ag.Agent_First_Name, ' ', ag.Agent_Last_Name) AS Agent_Name, CONCAT(ag.Contact_Number, ', ', ag.Email) AS Contact_Details \
#                                                      FROM VENUE v, AGENT ag, VENUEAGENT va \
#                                                      WHERE v.Venue_ID = va.Venue_ID AND va.Agent_ID = ag.Agent_ID ORDER BY v.Venue_Name;")
#         return context


# class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Reservation
#     template_name = 'reservation_update.html'
#     form_class = ReservationForm

#     def test_func(self):
#         obj = self.request.user.profile
#         return obj.user == self.request.user
    

#     def form_valid(self, form):
#         form.instance.reservation = self.get_object()
#         reservation = form.save(commit=False)

#         #saving into reservationlocation:
#         venue = form.cleaned_data.get("venue")
#         reservation_location = Reservationlocation(reservation=reservation, venue=venue) #code wants the instance, and not the ids
#         reservation_location.save()

#         #saving into reservationagent
#         agent_object = Venueagent.objects.get(venue=venue)
#         reservation_agent = Reservationagent(reservation=reservation, agent=agent_object.agent)
#         reservation_agent.save()

#         #saving into Reservationtimeslot
#         start_datetime = form.cleaned_data.get("start_datetime")
#         end_datetime = form.cleaned_data.get("end_datetime")
#         duration_base = end_datetime - start_datetime
#         hours, remainder = divmod(duration_base.seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         reservation_timeslot = Reservationtimeslot(reservation=reservation, duration=Concat(duration_base.days, Value(' days, '), hours, Value(' hours, '), minutes, Value(' minutes'), output_field=CharField()))
#         reservation_timeslot.save()
        
#         reservation.save()
#         return super().form_valid(form)
    

# class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Reservation
#     template_name = 'reservation_delete.html'
#     success_url = reverse_lazy('stateapp:search')

#     def test_func(self):
#         obj = self.request.user.profile
#         return obj.user == self.request.user
