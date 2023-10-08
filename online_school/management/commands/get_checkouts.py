from django.core.management import BaseCommand
import stripe

stripe.api_key = 'sk_test_51NrIuYEr4bPb9axLqE4JA5i65jeKiqFMIenTkPJpqY8e2ngTKGjrpl5I4pEq5V1iTB2yiFP3TuImcneVz6k3461u00Ifn7stOf'


class Command(BaseCommand):
    def handle(self, *args, **options):
        checkouts = stripe.checkout.Session.list()['data'][-1]['url']
        # checkout_urls = [checkout['url'] for checkout in checkouts]
        # for checkout_url in checkout_urls:
        #     print(f'{checkout_url}\n')
        print(checkouts)
