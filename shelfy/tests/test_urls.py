from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from shelfy.views import MediaAPI
from user_management.views import ProfileUpdateView, UserRegistrationView, DashboardView

User = get_user_model()

class TestUrls(TestCase):

    def setUp(self):
        """Setup a test user for authenticated routes."""
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_admin_url_resolves(self):
        url = reverse('admin:index')
        self.assertEqual(resolve(url).func.__name__, 'index')

    def test_media_search_url_resolves(self):
        url = reverse('media_search')
        self.assertEqual(resolve(url).func.view_class, MediaAPI)

        # Fix: Add a query parameter to prevent 400 error
        response = self.client.get(url, {'q': 'movie'})
        self.assertEqual(response.status_code, 200)

    def test_media_detail_url_resolves(self):
        url = reverse('media_detail', args=['movie', '123'])
        self.assertEqual(resolve(url).func.view_class, MediaAPI)

        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 404])  # 404 if ID is invalid

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

        # Fix: Use POST instead of GET for logout
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_update_profile_url_resolves(self):
        url = reverse('user_management:update_profile')
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)

        self.client.login(username="testuser", password="password123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_url_resolves(self):
        url = reverse('user_management:register')
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_resolves(self):
        url = reverse('user_management:dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardView)

        self.client.login(username="testuser", password="password123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
