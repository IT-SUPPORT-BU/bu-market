from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from marketplace.models import Category, Listing


class BrowseViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='seller1',
            email='seller1@example.com',
            password='password123',
            role=User.Role.SELLER,
        )
        self.category = Category.objects.create(name='Electronics', slug='electronics', icon='bi-phone')
        self.image = SimpleUploadedFile(
            'test.jpg',
            b'file-content',
            content_type='image/jpeg'
        )

    def test_browse_filters_by_location_and_sorts_by_price_ascending(self):
        Listing.objects.create(
            seller=self.user,
            category=self.category,
            title='Laptop',
            description='Fast laptop',
            price=300000,
            condition=Listing.Condition.NEW,
            location='Main Campus',
            image=self.image,
            status=Listing.Status.ACTIVE,
        )
        Listing.objects.create(
            seller=self.user,
            category=self.category,
            title='Phone',
            description='Budget phone',
            price=150000,
            condition=Listing.Condition.USED,
            location='Kampala Road',
            image=self.image,
            status=Listing.Status.ACTIVE,
        )
        Listing.objects.create(
            seller=self.user,
            category=self.category,
            title='Tablet',
            description='Portable tablet',
            price=220000,
            condition=Listing.Condition.NEW,
            location='Kampala Road',
            image=self.image,
            status=Listing.Status.ACTIVE,
        )

        response = self.client.get(reverse('core:browse'), {'location': 'kampala', 'sort': 'price_asc'})

        self.assertEqual(response.status_code, 200)
        listings = list(response.context['listings'])
        self.assertEqual([listing.title for listing in listings], ['Phone', 'Tablet'])
