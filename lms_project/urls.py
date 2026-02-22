from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('users.urls')),
    path('api/', include('courses.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Frontend Pages
    path('', TemplateView.as_view(template_name='index.html')),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html')),
    path('courses/', TemplateView.as_view(template_name='courses.html')),
    path('courses/<int:id>/', TemplateView.as_view(template_name='assignments.html')),
    path('cart/', TemplateView.as_view(template_name='cart.html')),
    path('payment/', TemplateView.as_view(template_name='payment.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
