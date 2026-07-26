from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRoleTestCase(TestCase):
    def test_user_creation_with_roles(self):
        # Create Buyer
        buyer = User.objects.create_user(username='buyer1', email='buyer@test.com', password='pass', role=User.Role.BUYER)
        self.assertTrue(buyer.is_buyer)
        self.assertFalse(buyer.is_seller)
        self.assertFalse(buyer.is_accountant)
        self.assertFalse(buyer.is_moderator)
        self.assertFalse(buyer.is_admin_role)

        # Create Seller
        seller = User.objects.create_user(username='seller1', email='seller@test.com', password='pass', role=User.Role.SELLER)
        self.assertFalse(seller.is_buyer)
        self.assertTrue(seller.is_seller)
        self.assertFalse(seller.is_accountant)
        self.assertFalse(seller.is_moderator)
        self.assertFalse(seller.is_admin_role)

        # Create Accountant
        accountant = User.objects.create_user(username='acc1', email='acc@test.com', password='pass', role=User.Role.ACCOUNTANT)
        self.assertFalse(accountant.is_buyer)
        self.assertFalse(accountant.is_seller)
        self.assertTrue(accountant.is_accountant)
        self.assertFalse(accountant.is_moderator)
        self.assertFalse(accountant.is_admin_role)

        # Create Moderator
        moderator = User.objects.create_user(username='mod1', email='mod@test.com', password='pass', role=User.Role.MODERATOR)
        self.assertFalse(moderator.is_buyer)
        self.assertFalse(moderator.is_seller)
        self.assertFalse(moderator.is_accountant)
        self.assertTrue(moderator.is_moderator)
        self.assertFalse(moderator.is_admin_role)

        # Create Admin
        admin = User.objects.create_user(username='admin_role', email='admin_role@test.com', password='pass', role=User.Role.ADMIN)
        self.assertFalse(admin.is_buyer)
        self.assertFalse(admin.is_seller)
        self.assertFalse(admin.is_accountant)
        self.assertFalse(admin.is_moderator)
        self.assertTrue(admin.is_admin_role)


from django.urls import reverse

class UserRoleAccessControlTestCase(TestCase):
    def setUp(self):
        self.password = 'password123'
        self.buyer = User.objects.create_user(username='buyer', password=self.password, role=User.Role.BUYER)
        self.seller = User.objects.create_user(username='seller', password=self.password, role=User.Role.SELLER)
        self.accountant = User.objects.create_user(username='accountant', password=self.password, role=User.Role.ACCOUNTANT)
        self.moderator = User.objects.create_user(username='moderator', password=self.password, role=User.Role.MODERATOR)
        self.admin = User.objects.create_user(username='admin_role', password=self.password, role=User.Role.ADMIN)
        self.superuser = User.objects.create_superuser(username='super', password=self.password)

    def test_anonymous_user_redirects(self):
        urls = [
            reverse('dashboard:seller_dashboard'),
            reverse('dashboard:buyer_dashboard'),
            reverse('dashboard:accountant_dashboard'),
            reverse('dashboard:moderator_dashboard'),
            reverse('dashboard:admin_dashboard'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('accounts:login'), response.url)

    def test_seller_dashboard_access(self):
        url = reverse('dashboard:seller_dashboard')
        # Seller should access
        self.client.login(username='seller', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Others should be denied (403)
        for username in ['buyer', 'accountant', 'moderator', 'admin_role']:
            self.client.login(username=username, password=self.password)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.client.logout()

        # Superuser should access
        self.client.login(username='super', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_buyer_dashboard_access(self):
        url = reverse('dashboard:buyer_dashboard')
        # Buyer should access
        self.client.login(username='buyer', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Others should be denied (403)
        for username in ['seller', 'accountant', 'moderator', 'admin_role']:
            self.client.login(username=username, password=self.password)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.client.logout()

        # Superuser should access
        self.client.login(username='super', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_accountant_dashboard_access(self):
        url = reverse('dashboard:accountant_dashboard')
        # Accountant should access
        self.client.login(username='accountant', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Others should be denied (403)
        for username in ['buyer', 'seller', 'moderator', 'admin_role']:
            self.client.login(username=username, password=self.password)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.client.logout()

        # Superuser should access
        self.client.login(username='super', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_moderator_dashboard_access(self):
        url = reverse('dashboard:moderator_dashboard')
        # Moderator should access
        self.client.login(username='moderator', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Others should be denied (403)
        for username in ['buyer', 'seller', 'accountant', 'admin_role']:
            self.client.login(username=username, password=self.password)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.client.logout()

        # Superuser should access
        self.client.login(username='super', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_access(self):
        url = reverse('dashboard:admin_dashboard')
        # Admin should access
        self.client.login(username='admin_role', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # Others should be denied (403)
        for username in ['buyer', 'seller', 'accountant', 'moderator']:
            self.client.login(username=username, password=self.password)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403)
            self.client.logout()

        # Superuser should access
        self.client.login(username='super', password=self.password)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


