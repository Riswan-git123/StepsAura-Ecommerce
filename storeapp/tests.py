import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Cart_item, Products


class StorefrontFlowTests(TestCase):
    def setUp(self):
        Products.objects.create(
            ecommerce_name="STEPSAURA",
            brand_name="Test Runner",
            details="A test sneaker",
            image="https://example.com/shoe.jpg",
            price=2500,
        )

    def test_storefront_links_open(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("contact")).status_code, 200)
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("signup")).status_code, 200)
        self.assertEqual(self.client.get(reverse("cart")).status_code, 200)
        self.assertEqual(self.client.get(reverse("details", args=[1])).status_code, 200)

    def test_add_and_remove_cart_item_updates_count_and_total(self):
        response = self.client.post(
            reverse("home"),
            data=json.dumps({"id": 1, "action": "add"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

        response = self.client.post(
            reverse("home"),
            data=json.dumps({"id": 1, "action": "add"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["count"], 2)

        response = self.client.get(reverse("cart"))
        cart_item = response.context["carts"][0]
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(response.context["total"], 5000)

        response = self.client.post(
            reverse("cart"),
            data=json.dumps({"id": cart_item.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "Deleted",
            "empty": True,
            "total": 0,
            "count": 0,
        })
        self.assertEqual(Cart_item.objects.count(), 0)

    def test_cart_is_private_to_each_browser_session(self):
        self.client.post(
            reverse("home"),
            data=json.dumps({"id": 1, "action": "add"}),
            content_type="application/json",
        )
        another_client = Client()
        response = another_client.get(reverse("cart"))
        self.assertEqual(response.context["count"], 0)
        self.assertEqual(response.context["carts"], [])

    def test_direct_cart_add_route_works(self):
        response = self.client.post(reverse("cart_item", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
