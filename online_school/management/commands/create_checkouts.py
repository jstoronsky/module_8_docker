from django.core.management import BaseCommand
import stripe

stripe.api_key = 'sk_test_51NrIuYEr4bPb9axLqE4JA5i65jeKiqFMIenTkPJpqY8e2ngTKGjrpl5I4pEq5V1iTB2yiFP3TuImcneVz6k3461u00Ifn7stOf'


class Command(BaseCommand):
    def handle(self, *args, **options):

        prices = stripe.Price.list()['data']
        prices_ids = [price['id'] for price in prices]
        for price_id in prices_ids:
            stripe.checkout.Session.create(
                success_url="https://example.com/success",
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 2,
                    },
                ],
                mode="subscription",
            )
