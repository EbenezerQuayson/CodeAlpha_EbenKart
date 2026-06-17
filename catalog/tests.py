from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='test@example.com')
        
    def test_profile_created_automatically(self):
        """Test that a UserProfile is created via post_save signal when a User is created."""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        profile = self.user.profile
        self.assertEqual(profile.payment_method, 'COD')
        
    def test_profile_view_redirects_anonymous(self):
        """Test that profile view redirects to login if user is not authenticated."""
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 302)
        
    def test_profile_view_authenticated(self):
        """Test that authenticated user can access the profile view."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/profile.html')
        
    def test_profile_update(self):
        """Test updating profile details via POST request."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('profile_view'), {
            'first_name': 'Eben',
            'last_name': 'Kart',
            'email': 'eben@example.com',
            'phone_number': '1234567890',
            'address': 'Main Street 123',
            'city': 'Accra',
            'country': 'Ghana',
            'payment_method': 'Visa'
        })
        self.assertEqual(response.status_code, 302)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Eben')
        self.assertEqual(self.user.last_name, 'Kart')
        self.assertEqual(self.user.email, 'eben@example.com')
        
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.phone_number, '1234567890')
        self.assertEqual(self.user.profile.address, 'Main Street 123')
        self.assertEqual(self.user.profile.city, 'Accra')
        self.assertEqual(self.user.profile.country, 'Ghana')
        self.assertEqual(self.user.profile.payment_method, 'Visa')

