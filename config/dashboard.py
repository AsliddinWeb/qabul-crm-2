# from unfold.contrib.admin import UnfoldDashboard
# from unfold.components import Card, Chart
# from applications.models import Application
# from django.utils.timezone import now, timedelta


# class ApplicationDashboard(UnfoldDashboard):
#     def get_cards(self, request):
#         return [
#             Card(title="Jami arizalar", value=str(Application.objects.count())),
#             Card(title="Tasdiqlangan", value=str(Application.objects.filter(status='approved').count()), color="green"),
#             Card(title="Yangi qabul", value=str(Application.objects.filter(admission_type='1st_year').count()), color="blue"),
#         ]

#     def get_charts(self, request):
#         labels = []
#         data = []
#         for i in range(7):
#             date = now().date() - timedelta(days=i)
#             labels.insert(0, date.strftime('%b %d'))
#             data.insert(0, Application.objects.filter(created_at__date=date).count())

#         return [
#             Chart(
#                 title="Oxirgi 7 kun arizalari",
#                 labels=labels,
#                 datasets=[{
#                     "label": "Arizalar",
#                     "data": data,
#                     "backgroundColor": "rgba(54, 162, 235, 0.6)",
#                 }],
#                 type="bar",
#             )
#         ]
