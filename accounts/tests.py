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

