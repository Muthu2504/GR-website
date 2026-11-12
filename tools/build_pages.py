"""Build the Groods sub-pages from index.html.

Run from anywhere:   python tools/build_pages.py

Pages it writes (do not edit these by hand, re-run this script instead):
  food-/parcel-/medicine-/grocery-delivery-tirupur/index.html   (SERVICES below)
  restaurants/index.html and restaurants/<name>-tirupur/index.html
  blog/biryani-delivery-tirupur/index.html                     (POST below)

The header icons, contact block, mobile bar and after-hours popup are copied
from index.html, so change them there and re-run.

Add a restaurant:
  1. Put a 480x360 .webp in assets/partners/.
  2. Copy one <li class="pcard">...</li> in the partners section of index.html,
     change the name, image, alt text and the WhatsApp message, and the
     /restaurants/<name>-tirupur/ link (lowercase, spaces -> hyphens).
  3. Run this script. It creates the restaurant page and adds it to the
     /restaurants/ list and the food delivery page.
  4. Add the new page URL to sitemap.xml (or run with --sitemap).

Bump CSS_V / JS_V below (and the ?v= in index.html) after changing
assets/site.css or assets/site.js so browsers fetch the new file.
"""
import html, json, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

def block(start, end):
    i = idx.index(start); j = idx.index(end, i) + len(end)
    return idx[i:j]

GTAG = block('<!-- Google tag (gtag.js) -->', '</script>\n')
SPRITE = block('<!-- icons -->', '</svg>\n\n<header')[:-len('\n\n<header')]
CONTACT = block('<!-- CONTACT -->', '</section>')
BAR = block('<!-- mobile sticky actions -->', '</dialog>')
SITE = 'https://groods.in'
WA = 'https://wa.me/919092162170?text='
REVIEWS = 'https://share.google/To2bdziSfGjPuQKso'

SERVICES = {
 'food': dict(slug='food-delivery-tirupur', name='Food delivery', short='Food',
   title='Food Delivery in Tirupur – Order on WhatsApp | Groods',
   desc='Food delivery in Tirupur from Hotel Sri Surya, Sasi Briyani Hotel, Junior Kuppanna and any restaurant you like. Order on WhatsApp or call 90921 62170.',
   h1='Food delivery in <em>Tirupur</em>',
   lead='Hungry? Tell us the restaurant and the dishes. Our rider picks up your meal hot and brings it to your door, from our partner restaurants or any restaurant in Tirupur.',
   wa='Hi Groods, I would like to order food.', img=('rider-food.webp', 373, 543, False),
   alt='Groods rider delivering food in Tirupur',
   h2='Your favourite Tirupur restaurants, delivered',
   body=['Groods is a local food delivery service in Tirupur. You do not need an app or an account. Send us your order on WhatsApp or call us, and we pick it up from the restaurant and deliver it to your home or office.',
         'Order from one of our partner restaurants below, or ask us to pick up from any other restaurant in Tirupur. Biryani, meals, parottas, grills, sandwiches, pizza and desserts are all welcome.'],
   box='What you can order', points=[('Biryani and meals','From Tirupur’s favourite biryani hotels and messes.'),('Snacks, sandwiches and pizza','For a quick bite at home or at work.'),('Cakes and desserts','Handled carefully so they arrive in one piece.'),('Any restaurant you choose','Not on our list? Just tell us where to pick up.')],
   faq=[('Which restaurants can I order from in Tirupur?','You can order from our partner restaurants, including Junior Kuppanna, Sasi Briyani Hotel, Hotel Sri Surya, The Biryani Theory and Padayappa Chettinad Hotel. You can also ask us to pick up from any other restaurant in Tirupur.'),
        ('How do I order food for delivery?','Message us on WhatsApp or call 90 921 621 70 with the restaurant name, your dishes and your delivery address. We confirm the price with you and send a rider.'),
        ('Do you deliver cakes for birthdays and functions?','Yes. Customers regularly use Groods for cake and dessert delivery in Tirupur, and our riders handle them with care.'),
        ('What time can I order food?','We deliver food every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm.'),
        ('Do I need to download an app?','No. Just WhatsApp or call us. Our app is coming soon.')]),
 'parcels': dict(slug='parcel-delivery-tirupur', name='Parcel delivery', short='Parcels',
   title='Parcel & Courier Delivery in Tirupur | Groods',
   desc='Local parcel and courier delivery in Tirupur. Pickup and drop of parcels, documents and packages across the city. WhatsApp or call 90921 62170.',
   h1='Parcel delivery in <em>Tirupur</em>',
   lead='Need something sent across town? We pick up your parcel, document or package and deliver it safely anywhere in Tirupur city.',
   wa='Hi Groods, I would like to send a parcel.', img=('parcels.webp', 520, 426, True),
   alt='Parcels ready for delivery in Tirupur',
   h2='Local pickup and drop, made simple',
   body=['Groods is a local parcel delivery service for Tirupur. Whether it is a document for your office, a package for a customer or something you forgot at home, our riders pick it up and hand it over at the other end.',
         'Share the pickup address, the drop address and what you are sending. We confirm the price with you before we pick it up.'],
   box='What we pick up and drop', points=[('Documents and files','Office papers, forms and important documents.'),('Packages for your customers','For shops and home businesses in Tirupur.'),('Gifts and personal items','Send something to family and friends in the city.'),('Things you left behind','Keys, chargers, lunch boxes and more.')],
   faq=[('Do you deliver parcels within Tirupur?','Yes. We pick up and drop parcels, documents and packages anywhere across Tirupur city.'),
        ('How do I book a parcel pickup?','Message us on WhatsApp or call 90 921 621 70 with the pickup address, drop address and what you are sending.'),
        ('How much does parcel delivery cost?','It depends on the distance. We confirm the price with you before we pick up your parcel.'),
        ('Can businesses use Groods for deliveries?','Yes. Shops and home businesses in Tirupur use Groods to deliver to their customers. Message us to get started.'),
        ('When can I send a parcel?','We deliver every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm.')]),
 'medicines': dict(slug='medicine-delivery-tirupur', name='Medicine delivery', short='Medicines',
   title='Medicine Home Delivery in Tirupur | Groods',
   desc='Medicine home delivery in Tirupur. We pick up prescription and everyday medicines from licensed medical shops. WhatsApp or call 90921 62170.',
   h1='Medicine delivery in <em>Tirupur</em>',
   lead='Stay home and rest. We pick up your prescription and everyday medicines from licensed medical shops in Tirupur and bring them to your door.',
   wa='Hi Groods, I need to order medicines.', img=('medicines.webp', 509, 390, True),
   alt='Medicines delivered at home in Tirupur',
   h2='Medicines at your door, from shops you trust',
   body=['Groods delivers medicines at home across Tirupur. We buy them from licensed medical shops, so you get the right medicines without stepping out.',
         'Send us the list of medicines, or a photo of your prescription, on WhatsApp. Tell us if you prefer a particular medical shop and we will go there.'],
   box='How we help', points=[('Prescription medicines','Share your prescription on WhatsApp.'),('Everyday medicines','Pain relief, cold and fever, first aid and more.'),('Your preferred medical shop','Tell us where you usually buy.'),('Care for elders at home','Order for your parents, wherever they are in Tirupur.')],
   faq=[('Can I get medicines delivered at home in Tirupur?','Yes. We pick up medicines from licensed medical shops in Tirupur and deliver them to your home.'),
        ('How do I order prescription medicines?','Send the list of medicines or a photo of your prescription on WhatsApp to 90 921 621 70. We confirm the price with you before we buy them.'),
        ('Can you buy from a specific medical shop?','Yes. Tell us the medical shop you prefer and we will pick up your medicines from there.'),
        ('Can I order medicines for my parents?','Yes. Place the order from anywhere and give us their address in Tirupur. We will deliver to them.'),
        ('When do you deliver medicines?','We deliver every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm.')]),
 'groceries': dict(slug='grocery-delivery-tirupur', name='Grocery delivery', short='Groceries',
   title='Grocery Delivery in Tirupur – Daily Essentials | Groods',
   desc='Grocery delivery in Tirupur. Send your list on WhatsApp and we bring daily essentials and fresh items from the shop to your home. Call 90921 62170.',
   h1='Grocery delivery in <em>Tirupur</em>',
   lead='Skip the trip to the shop. Send us your grocery list and we will bring your daily essentials and fresh items to your home.',
   wa='Hi Groods, I would like to order groceries.', img=('groceries-cart.webp', 703, 720, False),
   alt='Grocery cart for home delivery in Tirupur',
   h2='Your grocery list, delivered',
   body=['Groods is a local grocery delivery service in Tirupur. Send us your list on WhatsApp, and we buy the items from the shop and deliver them to your door.',
         'Have a favourite store? Tell us which one and we will shop there for you. We confirm the price with you before we deliver.'],
   box='What we can bring', points=[('Daily essentials','Rice, dal, oil, milk, bread and more.'),('Fresh items','Vegetables, fruits and everyday fresh produce.'),('Household needs','Cleaning supplies and other home items.'),('From your favourite store','Tell us where you like to shop.')],
   faq=[('Do you deliver groceries in Tirupur?','Yes. Send us your grocery list and we will deliver your daily essentials and fresh items to your home in Tirupur.'),
        ('How do I order groceries?','Message your grocery list on WhatsApp to 90 921 621 70, or call us. Tell us the shop if you have a favourite.'),
        ('How do I pay for groceries?','We confirm the price with you first. You can pay online or pay on delivery.'),
        ('When do you deliver groceries?','We deliver every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm.'),
        ('Is there a minimum order?','Just tell us what you need and we will confirm the price with you before we deliver.')]),
}

def rslug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-') + '-tirupur'
# (group, name, img, wa) from the homepage partner cards, in page order
REST = []
for gm in re.finditer(r'<h3 class="p-title">([^<]+)</h3>\s*<ul class="p-grid">(.*?)</ul>', idx, re.S):
    grp = html.unescape(gm.group(1))
    for m in re.finditer(r'<img src="([^"]+)"[^>]*><h4>([^<]+)</h4></a><a class="p-cta" href="([^"]+)"', gm.group(2)):
        REST.append(dict(group=grp, img='/' + m.group(1), name=m.group(2), wa=m.group(3), slug=rslug(m.group(2))))
PARTNERS = [(r['wa'], r['name']) for r in REST]
PARTNER_URL = {r['name']: r['wa'] for r in REST}
PAGE_URL = {r['name']: f"/restaurants/{r['slug']}/" for r in REST}
PROMO = '''<a class="promo rv" href="/blog/biryani-delivery-tirupur/">
      <div>
        <span class="promo-tag"><i></i>New food guide</span>
        <h3>Craving biryani tonight?</h3>
        <p>7 biryani spots in Tirupur you can order from on WhatsApp, delivered hot to your door.</p>
        <p class="names">Hotel Sri Surya · Chettiar Kadai · Sasi Briyani · Dindigul Sri Alagappa · The Biryani Theory · Junior Kuppanna · Padayappa</p>
        <span class="promo-cta">See the biryani list <svg><use href="#i-arrow"/></svg></span>
      </div>
      <div class="promo-art" aria-hidden="true"><span class="promo-badge"><span><b>7</b>biryani spots</span></span><img src="/assets/rider-food.webp" width="373" height="543" alt="" loading="lazy"></div>
    </a>'''
CSS_V = 'v=7'
JS_V = 'v=3'

AREAS = ['Avinashi Road', 'Palladam Road', 'Kangeyam Road', 'Dharapuram Road', 'P.N. Road', 'Kumar Nagar',
         'Anupparpalayam', '15 Velampalayam', 'Veerapandi', 'Nallur', 'Rayapuram', 'Mannarai',
         'New Bus Stand', 'Old Bus Stand']
CITY = {"@type": "City", "name": "Tirupur", "alternateName": ["Tiruppur", "திருப்பூர்"]}
CALL_TA = 'WhatsApp அல்லது அழைக்கவும்: 90 921 621 70.'
TA = {
  'home': 'திருப்பூர் முழுவதும் உணவு, பார்சல், மருந்து மற்றும் மளிகை பொருட்கள் டெலிவரி.',
  'food': 'திருப்பூரில் உணவு டெலிவரி – உங்களுக்கு பிடித்த உணவகங்களிலிருந்து உங்கள் வீட்டிற்கு.',
  'parcels': 'திருப்பூரில் பார்சல் டெலிவரி – நகரம் முழுவதும் பிக்கப் மற்றும் டிராப்.',
  'medicines': 'திருப்பூரில் மருந்து டெலிவரி – உரிமம் பெற்ற மருந்தகங்களிலிருந்து உங்கள் வீட்டிற்கு.',
  'groceries': 'திருப்பூரில் மளிகை பொருட்கள் டெலிவரி – தினசரி தேவைகள் உங்கள் வீட்டு வாசலுக்கு.',
}

def areas_section(what, ta):
    chips = ''.join(f'<li>{a}</li>' for a in AREAS)
    return f'''<section class="sec areas-sec" id="areas">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">Areas we cover</span>
      <h2>Delivering across Tirupur</h2>
      <p>Groods delivers {what} across Tirupur (also spelt Tiruppur), including these areas:</p>
    </div>
    <ul class="area-list rv">{chips}</ul>
    <p class="area-note rv">Don’t see your area? <a href="{WA}{quote('Hi Groods, do you deliver to my area?')}" target="_blank" rel="noopener">Ask us on WhatsApp</a>. We cover most of Tirupur city.</p>
    <p class="ta-line rv" lang="ta">{ta} {CALL_TA}</p>
  </div>
</section>'''

def shell(*, title, desc, url, img, w, h, lds, wa, main, og_type='website'):
    title = html.escape(title); desc = html.escape(desc)
    lds = '\n'.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False)}\n</script>' for x in lds)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GTAG}<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F45146">
<meta name="geo.region" content="IN-TN">
<meta name="geo.placename" content="Tirupur">
<link rel="icon" href="/favicon.svg?v=4" type="image/svg+xml">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Groods">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/{img}">
<meta property="og:image:width" content="{w}">
<meta property="og:image:height" content="{h}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700&family=Funnel+Sans:wght@400;500;600&display=swap" rel="stylesheet">
{lds}
<link rel="stylesheet" href="/assets/site.css?{CSS_V}">
</head>
<body class="no-js">
<a class="skip" href="#main">Skip to content</a>

{SPRITE}

<header class="nav" id="nav">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Groods home"><img src="/assets/groods-logo.svg" alt="Groods" width="108" height="36"></a>
    <nav class="nav-links" aria-label="Main">
      <a href="/#what">What we do</a><a href="/#how">How to order</a><a href="/#reviews">Reviews</a><a href="/#about">About us</a><a href="/#faq">FAQ</a><a href="#contact">Contact</a>
    </nav>
    <div class="nav-cta">
      <a class="btn btn-call" href="tel:+919092162170" aria-label="Call 90 921 621 70"><svg><use href="#i-phone"/></svg><span class="t-long">Call</span></a>
      <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span class="t-long">Order on WhatsApp</span><span class="t-short">Order</span></a>
    </div>
  </div>
</header>

<main id="main">
{main}
</main>

{CONTACT}

<footer>
  <div class="wrap">
    <div class="foot">
      <a class="logo" href="/" aria-label="Groods home"><img src="/assets/groods-logo.svg" alt="Groods" width="108" height="36"></a>
      <nav aria-label="Footer"><a href="/#what">What we do</a><a href="/#reviews">Reviews</a><a href="/#about">About us</a><a href="/#faq">FAQ</a><a href="#contact">Contact</a></nav>
      <nav aria-label="Services"><a href="/food-delivery-tirupur/">Food delivery</a><a href="/parcel-delivery-tirupur/">Parcel delivery</a><a href="/medicine-delivery-tirupur/">Medicine delivery</a><a href="/grocery-delivery-tirupur/">Grocery delivery</a><a href="/restaurants/">Restaurants</a><a href="/blog/biryani-delivery-tirupur/">Biryani in Tirupur</a></nav>
      <span>© <span id="yr">2026</span> Groods. Tirupur.</span>
    </div>
  </div>
</footer>

{BAR}

<script src="/assets/site.js?{JS_V}"></script>
</body>
</html>
'''

def crumbs(items):
    lis = ''.join(f'<li><a href="{u}">{n}</a></li>' for n, u in items[:-1]) + f'<li aria-current="page">{items[-1][0]}</li>'
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

def crumb_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}

def faq_html(faq):
    return '\n'.join(f'      <details class="rv" name="faq"><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in faq)

def faq_ld(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def faq_section(heading, faq):
    return f'''<section class="sec" id="faq">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">FAQ</span>
      <h2>{heading}</h2>
    </div>
    <div class="faq">
{faq_html(faq)}
    </div>
  </div>
</section>'''

STEPS = '''<section class="sec steps-sec" id="how">
  <div class="wrap">
    <div class="sec-head rv">
      <span class="eyebrow">How to order</span>
      <h2>Three easy steps</h2>
      <p>No app to download and nothing to sign up for.</p>
    </div>
    <div class="steps">
      <div class="step rv"><h3>Message or call us</h3><p>Tap WhatsApp or call 90 921 621 70.</p></div>
      <div class="step rv"><h3>Tell us what you need</h3><p>Share the order, pickup and drop details. We confirm the price with you.</p></div>
      <div class="step rv"><h3>We deliver</h3><p>Our rider brings it to your door. Pay online or on delivery.</p></div>
    </div>
  </div>
</section>'''

def page(key):
    s = SERVICES[key]
    path = f'/{s["slug"]}/'; url = SITE + path
    wa = WA + quote(s['wa'])
    img, w, h, wide = s['img']
    trail = [('Home', '/'), (f'{s["name"]} in Tirupur', path)]
    lds = [
      {"@context":"https://schema.org","@type":"Service","name":f'{s["name"]} in Tirupur',"serviceType":s['name'],"description":s['desc'],"url":url,
       "areaServed":CITY,"provider":{"@type":"LocalBusiness","@id":f"{SITE}/#business","name":"Groods","telephone":"+919092162170","url":f"{SITE}/"}},
      crumb_ld(trail), faq_ld(s['faq'])]
    points = '\n'.join(f'          <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>{html.escape(b)}</b><span>{html.escape(t)}</span></div></li>' for b,t in s['points'])
    other = '\n'.join(
      f'      <a class="rv" href="/{o["slug"]}/"><b>{o["name"]}</b><span>{html.escape(o["desc"].split(". ")[0])}.</span><em>Learn more <svg><use href="#i-arrow"/></svg></em></a>'
      for k,o in SERVICES.items() if k != key)
    partners = ''; promo = ''
    if key == 'food':
        promo = '\n  <div class="wrap">\n    ' + PROMO + '\n  </div>'
        tags = '\n'.join(f'          <li><a href="{PAGE_URL[n]}">{n}</a></li>' for u,n in PARTNERS)
        partners = f'''
      <div class="svc-box rv" style="margin-top:20px">
        <h3>Order from our partner restaurants</h3>
        <ul class="tags">
{tags}
        </ul>
      </div>'''
    main = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumbs(trail)}
      <span class="eyebrow"><span class="pulse"></span>Now delivering in Tirupur</span>
      <h1>{s["h1"]}</h1>
      <p class="lead">{html.escape(s["lead"])}</p>
      <div class="cta-row" id="heroCta">
        <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Order on WhatsApp</a>
        <a class="btn btn-call btn-lg" href="tel:+919092162170"><svg><use href="#i-phone"/></svg>Call 90 921 621 70</a>
      </div>
      <a class="hero-rate" href="{REVIEWS}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">★★★★★</span><span><b>4.7</b> on Google · 91 reviews</span></a>
    </div>
    <div class="hero-art">
      <img{' class="wide"' if wide else ''} src="/assets/{img}" width="{w}" height="{h}" alt="{html.escape(s["alt"])}">
    </div>
  </div>
</section>

<section class="sec" id="about">
  <div class="wrap svc-body">
    <div class="rv">
      <span class="eyebrow">{s["name"]}</span>
      <h2>{html.escape(s["h2"])}</h2>
      {''.join(f'<p>{html.escape(p)}</p>' for p in s["body"])}
    </div>
    <div>
      <div class="svc-box rv">
        <h3>{s["box"]}</h3>
        <ul class="points">
{points}
        </ul>
      </div>{partners}
    </div>
  </div>{promo}
</section>

{STEPS}

{areas_section(s["name"].lower().replace(" delivery", "") + " delivery", TA[key])}

{faq_section(f'{s["name"]} in Tirupur: FAQs', s['faq'])}

<section class="sec" id="more" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head rv" style="margin-bottom:24px"><h2>More from Groods in Tirupur</h2></div>
    <div class="other">
{other}
    </div>
  </div>
</section>'''
    return shell(title=s['title'], desc=s['desc'], url=url, img=img, w=w, h=h, lds=lds, wa=wa, main=main)

# ---------- blog post ----------
POST = dict(
  path='/blog/biryani-delivery-tirupur/',
  title='Biryani Delivery in Tirupur: 7 Places to Order | Groods',
  desc='Biryani delivery in Tirupur from Hotel Sri Surya, Chettiar Kadai, Sasi Briyani Hotel, Junior Kuppanna and more. Order on WhatsApp with Groods.',
  h1='Biryani delivery in Tirupur: <em>7 places you can order from</em>',
  lead='Craving biryani? These are biryani spots across Tirupur that you can get delivered to your door with Groods. Just send us a WhatsApp message.',
  published='2026-11-11',
  picks=[
    ('Hotel Sri Surya', 'One of our partner restaurants in Tirupur and a favourite with our customers. Send us your biryani order on WhatsApp and we will deliver it hot.'),
    ('Chettiar Kadai', 'Tirupur Chettiar Kadai, a non-veg favourite in the city. Order your biryani along with their chicken dishes, and we will bring it all in one trip.'),
    ('Sasi Briyani Hotel', 'A dedicated biryani hotel and one of our regular partners in Tirupur. Tell us what you want and our rider will bring it to you hot.'),
    ('Dindigul Sri Alagappa Briyani', 'Dindigul-style biryani, right here in Tirupur. A good pick if you like the Dindigul way of making it.'),
    ('The Biryani Theory', 'A restaurant built around biryani. Order for yourself or for the whole family.'),
    ('Junior Kuppanna', 'A well-known name in Tamil Nadu for non-veg meals. Add biryani to your order along with your other favourites.'),
    ('Padayappa Chettinad Hotel', 'Chettinad-style food in Tirupur. Pair your biryani with their other dishes in one order.'),
  ],
  more=['Hotel New Mohan', 'Udumalai Mess', 'Hotel Maniam Classic', 'Four Monkeys', 'The Bay Grill', 'The Kitchen Drama', 'Aroma'],
  tips=[
    ('Order a little before the rush', 'Lunch and dinner peak hours are busy for restaurants. Ordering a bit earlier helps your biryani reach you sooner.'),
    ('Ordering for a group?', 'Tell us how many people you are ordering for and the restaurant. We confirm the price with you before we pick up.'),
    ('Add your extras', 'Want extra raita, gravy, an egg or a sweet? Mention it in your WhatsApp message and we will pass it on.'),
    ('Know our hours', 'We deliver every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm.'),
  ],
  faq=[
    ('Where can I order biryani for delivery in Tirupur?', 'With Groods you can order biryani from Hotel Sri Surya, Chettiar Kadai, Sasi Briyani Hotel, Dindigul Sri Alagappa Briyani, The Biryani Theory, Junior Kuppanna, Padayappa Chettinad Hotel and other restaurants across Tirupur. Message us on WhatsApp or call 90 921 621 70.'),
    ('Can I order biryani from a restaurant that is not on this list?', 'Yes. Tell us the restaurant and the dishes and we will pick it up for you from anywhere in Tirupur.'),
    ('How do I pay for my biryani order?', 'We confirm the price with you first. You can pay online or pay on delivery.'),
  ],
)

def blog():
    P = POST; url = SITE + P['path']
    wa = WA + quote('Hi Groods, I would like to order biryani.')
    trail = [('Home', '/'), ('Food delivery', '/food-delivery-tirupur/'), ('Biryani delivery in Tirupur', P['path'])]
    lds = [
      {"@context":"https://schema.org","@type":"Article","headline":re.sub('<[^>]+>','',P['h1']),"description":P['desc'],
       "url":url,"mainEntityOfPage":url,"datePublished":P['published'],"dateModified":P['published'],"inLanguage":"en-IN",
       "image":f"{SITE}/assets/rider-food.webp",
       "author":{"@type":"Organization","name":"Groods","url":f"{SITE}/"},
       "publisher":{"@type":"Organization","name":"Groods","logo":{"@type":"ImageObject","url":f"{SITE}/assets/groods-logo.svg"}},
       "about":{"@type":"Thing","name":"Biryani delivery in Tirupur"},"spatialCoverage":CITY},
      crumb_ld(trail), faq_ld(P['faq'])]
    picks = '\n'.join(f'''    <div class="pick rv">
      <span class="pick-n">{i}</span>
      <div>
        <h2><a href="{PAGE_URL[n]}">{html.escape(n)}</a></h2>
        <p>{html.escape(d)}</p>
        <a class="btn btn-wa" href="{PARTNER_URL[n]}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Order from {html.escape(n)}</a>
      </div>
    </div>''' for i,(n,d) in enumerate(P['picks'], 1))
    more = ''.join(f'<li><a href="{PAGE_URL[n]}">{n}</a></li>' for n in P['more'])
    tips = '\n'.join(f'        <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>{html.escape(b)}</b><span>{html.escape(t)}</span></div></li>' for b,t in P['tips'])
    main = f'''<section class="hero post-hero">
  <div class="wrap post">
    {crumbs(trail)}
    <span class="eyebrow">Food guide · <time datetime="{P['published']}">11 Nov 2026</time></span>
    <h1>{P["h1"]}</h1>
    <p class="lead">{html.escape(P["lead"])}</p>
    <div class="cta-row" id="heroCta">
      <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Order biryani on WhatsApp</a>
      <a class="btn btn-call btn-lg" href="tel:+919092162170"><svg><use href="#i-phone"/></svg>Call 90 921 621 70</a>
    </div>
  </div>
</section>

<article class="sec" id="about" style="padding-top:24px">
  <div class="wrap post">
{picks}

    <div class="post-block rv">
      <h2>More restaurants you can order from</h2>
      <p>Want meals, grills or something else with your biryani? Groods also delivers from these Tirupur restaurants:</p>
      <ul class="tags">{more}</ul>
      <p>Not on the list? Tell us any restaurant in Tirupur and we will pick it up. See all our <a href="/food-delivery-tirupur/">food delivery in Tirupur</a>.</p>
    </div>

    <div class="post-block rv">
      <h2>Tips for ordering biryani for delivery</h2>
      <ul class="points">
{tips}
      </ul>
    </div>
  </div>
</article>

{faq_section('Biryani delivery in Tirupur: FAQs', P['faq'])}'''
    return shell(title=P['title'], desc=P['desc'], url=url, img='rider-food.webp', w=373, h=543, lds=lds, wa=wa, main=main, og_type='article')

for k, s in SERVICES.items():
    d = os.path.join(ROOT, s['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(page(k))
    print('wrote', s['slug'])
d = os.path.join(ROOT, POST['path'].strip('/')); os.makedirs(d, exist_ok=True)
open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(blog())
print('wrote', POST['path'])

# ---------- restaurant pages ----------
ALSO = {'Sasi Briyani Hotel': 'Sasi Biryani Hotel'}  # common alternate spelling people search

def pcard(x, indent='      '):
    return (f'''{indent}<li class="pcard"><a class="p-link" href="/restaurants/{x['slug']}/"><img src="{x['img']}" width="480" height="360" alt="{x['name']}, Tirupur" loading="lazy"><h4>{x['name']}</h4></a>'''
            f'''<a class="p-cta" href="{x['wa']}" target="_blank" rel="noopener" data-label="{x['name']}" aria-label="Order from {x['name']} on WhatsApp"><svg aria-hidden="true"><use href="#i-wa"/></svg>Order now</a></li>''')

def rest_page(r):
    n = r['name']; path = f"/restaurants/{r['slug']}/"; url = SITE + path
    alt = f' (also searched as {ALSO[n]})' if n in ALSO else ''
    wa = r['wa']
    trail = [('Home', '/'), ('Restaurants', '/restaurants/'), (n, path)]
    faq = [
      (f'Does {n} deliver in Tirupur?', f'Yes. You can get {n} delivered to your home or office anywhere in Tirupur through Groods. Message us on WhatsApp or call 90 921 621 70 with your order.'),
      (f'How do I order {n} food online?', f'Tap “Order from {n}” on this page to send us a WhatsApp message, then tell us the dishes you want and your address. We confirm the price, pick up your food from {n} and deliver it.'),
      (f'What time can I order from {n}?', 'Groods delivers every day from 11:00 am to 3:30 pm and from 6:00 pm to 10:00 pm, as long as the restaurant is open.'),
      ('How much does delivery cost?', 'It depends on the distance. We confirm the full price with you before we pick up your order, and you can pay online or on delivery.'),
    ]
    same = [x for x in REST if x['group'] == r['group'] and x is not r]
    others = (same + [x for x in REST if x['group'] != r['group']])[:5]
    cards = '\n'.join(pcard(x) for x in others)
    lds = [
      {"@context":"https://schema.org","@type":"Service","name":f"{n} home delivery in Tirupur","serviceType":"Food delivery",
       "description":f"Home delivery of food from {n} in Tirupur by Groods.","url":url,"areaServed":CITY,
       "provider":{"@type":"LocalBusiness","@id":f"{SITE}/#business","name":"Groods","telephone":"+919092162170","url":f"{SITE}/"}},
      crumb_ld(trail), faq_ld(faq)]
    main = f'''<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      {crumbs(trail)}
      <span class="eyebrow"><span class="pulse"></span>{html.escape(r['group'])} · Tirupur</span>
      <h1>{n} <em>home delivery in Tirupur</em></h1>
      <p class="lead">Craving {n}{alt}? Order on WhatsApp and Groods will pick up your food from {n} and deliver it to your door anywhere in Tirupur.</p>
      <div class="cta-row" id="heroCta">
        <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener" data-label="{n}"><svg><use href="#i-wa"/></svg>Order from {n}</a>
        <a class="btn btn-call btn-lg" href="tel:+919092162170"><svg><use href="#i-phone"/></svg>Call 90 921 621 70</a>
      </div>
      <a class="hero-rate" href="{REVIEWS}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">★★★★★</span><span>Groods: <b>4.7</b> on Google · 91 reviews</span></a>
    </div>
    <div class="hero-art rest-art">
      <img src="{r['img']}" width="480" height="360" alt="{n}, Tirupur">
    </div>
  </div>
</section>

<section class="sec" id="about">
  <div class="wrap svc-body">
    <div class="rv">
      <span class="eyebrow">Partner restaurant</span>
      <h2>Order {n} without leaving home</h2>
      <p>{n} is one of Groods’ partner restaurants in Tirupur. You don’t need an app or an account: just send us your order on WhatsApp or call us, and our rider brings it to your home or office.</p>
      <p>Want something from another restaurant too? Add it to the same message. See all <a class="inline" href="/restaurants/">restaurants that deliver in Tirupur</a> or read about our <a class="inline" href="/food-delivery-tirupur/">food delivery in Tirupur</a>.</p>
    </div>
    <div class="svc-box rv">
      <h3>Why order through Groods</h3>
      <ul class="points">
        <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>Order on WhatsApp</b><span>No app, no sign-up. Just message us.</span></div></li>
        <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>Price confirmed first</b><span>We tell you the total before we pick up.</span></div></li>
        <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>Local Tirupur riders</b><span>Delivered with care, rated 4.7 on Google.</span></div></li>
        <li><span class="tick"><svg><use href="#i-check"/></svg></span><div><b>Pay online or on delivery</b><span>Whichever is easier for you.</span></div></li>
      </ul>
    </div>
  </div>
</section>

{STEPS}

{faq_section(f'{n} delivery: FAQs', faq)}

<section class="sec partners" id="more" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head rv" style="margin-bottom:24px"><h2>More restaurants in Tirupur</h2></div>
    <ul class="p-grid rv">
{cards}
    </ul>
    <p class="all-rest"><a href="/restaurants/">See all restaurants <svg><use href="#i-arrow"/></svg></a></p>
  </div>
</section>'''
    title = f'{n} Delivery in Tirupur | Groods' if len(n) > 22 else f'{n} Home Delivery in Tirupur | Groods'
    desc = f'{n}' + (f' ({ALSO[n]})' if n in ALSO else '') + ' home delivery in Tirupur. Order on WhatsApp or call 90921 62170 and Groods brings your food to your door.'
    return shell(title=title, desc=desc, url=url, img=r['img'].replace('/assets/', '', 1), w=480, h=360, lds=lds, wa=wa, main=main)

def rest_index():
    path = '/restaurants/'; url = SITE + path
    wa = WA + quote('Hi Groods, I would like to order food.')
    trail = [('Home', '/'), ('Restaurants', path)]
    groups = {}
    for r in REST: groups.setdefault(r['group'], []).append(r)
    blocks = '\n'.join(
        f'''    <div class="p-group rv">
      <h2 class="p-title">{html.escape(gname)}</h2>
      <ul class="p-grid">
''' + '\n'.join(pcard(x, '        ') for x in rs) + '''
      </ul>
    </div>''' for gname, rs in groups.items())
    names = ', '.join(r['name'] for r in REST[:4])
    short = ', '.join(r['name'] for r in REST[:3])
    lds = [
      {"@context":"https://schema.org","@type":"CollectionPage","name":"Restaurants that deliver in Tirupur","url":url,"about":{"@type":"Thing","name":"Food delivery in Tirupur"},
       "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":r['name'],"url":f"{SITE}/restaurants/{r['slug']}/"} for i,r in enumerate(REST)]}},
      crumb_ld(trail)]
    main = f'''<section class="hero post-hero">
  <div class="wrap post">
    {crumbs(trail)}
    <span class="eyebrow"><span class="pulse"></span>{len(REST)} partner restaurants</span>
    <h1>Restaurants that deliver in <em>Tirupur</em></h1>
    <p class="lead">Order from {names} and more. Tap a restaurant to see how to order, or tap “Order now” to send us your order on WhatsApp.</p>
    <div class="cta-row" id="heroCta">
      <a class="btn btn-wa btn-lg" href="{wa}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>Order on WhatsApp</a>
      <a class="btn btn-call btn-lg" href="tel:+919092162170"><svg><use href="#i-phone"/></svg>Call 90 921 621 70</a>
    </div>
  </div>
</section>

<section class="sec partners" id="about" style="padding-top:24px">
  <div class="wrap">
{blocks}
    <p class="all-rest rv">Don’t see your favourite? We pick up from any restaurant in Tirupur. <a href="/food-delivery-tirupur/">More about food delivery in Tirupur <svg><use href="#i-arrow"/></svg></a></p>
    {PROMO}
  </div>
</section>'''
    return shell(title='Restaurants That Deliver in Tirupur | Groods',
                 desc=f'Restaurants with home delivery in Tirupur (Tiruppur): {short} and more. Order on WhatsApp or call 90921 62170.',
                 url=url, img='rider-food.webp', w=373, h=543, lds=lds, wa=wa, main=main)

for r in REST:
    d = os.path.join(ROOT, 'restaurants', r['slug']); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(rest_page(r))
open(os.path.join(ROOT, 'restaurants', 'index.html'), 'w', encoding='utf-8', newline='\n').write(rest_index())
print('restaurants', len(REST), [r['slug'] for r in REST])


# ---------- optional: rebuild sitemap.xml from every index.html ----------
if '--sitemap' in sys.argv:
    import datetime, glob
    today = datetime.date.today().isoformat()
    pages = sorted(set(os.path.relpath(p, ROOT).replace(os.sep, '/')
                       for p in glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)
                       if 'tools' not in os.path.relpath(p, ROOT).split(os.sep)))
    locs = [SITE + '/' + ('' if p == 'index.html' else p[:-len('index.html')]) for p in pages]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += ''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in locs) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)
    print('sitemap', len(locs), 'urls')
