from marketplace.models import Listing

def recently_viewed(request):
    ids = request.session.get('recently_viewed', [])
    listings = []
    if ids:
        listings_by_id = Listing.objects.in_bulk(ids)
        listings = [listings_by_id[i] for i in ids if i in listings_by_id]
    return {'recently_viewed_listings': listings}