from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from catalog.models import Product, UserProfile
from cart.models import Cart, CartItem, Order

class CartCheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcheckout', password='password123', email='checkout@example.com')
        self.product = Product.objects.create(name='Boutique Watch', description='Gold timepiece', price=150.00, stock_quantity=5)
        
        # Add item to user's cart
        self.cart, _ = Cart.objects.get_or_create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        
    def test_checkout_requires_post(self):
        """Test that checkout view redirects if request is not POST."""
        self.client.login(username='testcheckout', password='password123')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        
    def test_checkout_delivery_with_save_profile(self):
        """Test checking out with Delivery option and saving details to UserProfile."""
        self.client.login(username='testcheckout', password='password123')
        
        # Perform checkout POST request
        response = self.client.post(reverse('checkout'), {
            'delivery_type': 'Delivery',
            'shipping_address': '55 Boutique Road',
            'shipping_city': 'Accra',
            'shipping_country': 'Ghana',
            'shipping_phone': '+233 55 999 8888',
            'payment_method': 'Visa',
            'save_to_profile': 'true'
        })
        
        # Should redirect to order success page
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        
        # Verify order details
        self.assertEqual(order.delivery_type, 'Delivery')
        self.assertEqual(order.shipping_address, '55 Boutique Road')
        self.assertEqual(order.shipping_city, 'Accra')
        self.assertEqual(order.shipping_country, 'Ghana')
        self.assertEqual(order.shipping_phone, '+233 55 999 8888')
        self.assertEqual(order.payment_method, 'Visa')
        
        # Verify user profile was updated
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.address, '55 Boutique Road')
        self.assertEqual(self.user.profile.city, 'Accra')
        self.assertEqual(self.user.profile.country, 'Ghana')
        self.assertEqual(self.user.profile.phone_number, '+233 55 999 8888')
        self.assertEqual(self.user.profile.payment_method, 'Visa')
        
        # Cart should be empty
        self.assertEqual(self.cart.items.count(), 0)

    def test_checkout_pickup_without_save_profile(self):
        """Test checking out with Store Pickup and not saving details to UserProfile."""
        self.client.login(username='testcheckout', password='password123')
        
        # Ensure profile starts clean
        profile = self.user.profile
        profile.address = None
        profile.phone_number = None
        profile.payment_method = 'COD'
        profile.save()
        
        # Perform checkout POST request
        response = self.client.post(reverse('checkout'), {
            'delivery_type': 'Pickup',
            'shipping_phone': '+233 24 111 2222',
            'payment_method': 'MobileMoney',
            'save_to_profile': 'false'
        })
        
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        
        # Verify order details
        self.assertEqual(order.delivery_type, 'Pickup')
        self.assertEqual(order.shipping_address, 'Store Pickup')
        self.assertEqual(order.shipping_phone, '+233 24 111 2222')
        self.assertEqual(order.payment_method, 'MobileMoney')
        
        # Verify user profile remained unchanged (address and phone should still be None/payment COD)
        self.user.profile.refresh_from_db()
        self.assertIsNone(self.user.profile.address)
        self.assertIsNone(self.user.profile.phone_number)
        self.assertEqual(self.user.profile.payment_method, 'COD')

