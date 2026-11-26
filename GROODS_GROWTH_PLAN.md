# Groods website growth plan

Prepared 25 November 2026. This is a planning document; no website, account, campaign, or server setting was changed.

## Goal

Increase qualified traffic to Groods in Tirupur, turn more visits into completed orders, and give customers reasons to return. The main customer action today is ordering through WhatsApp or by phone.

## What the website already does well

- Clear local positioning for Tirupur, with food, parcel, medicine, and grocery delivery pages.
- A restaurant directory and individual restaurant pages, including Sandwich 99.
- Visible WhatsApp and phone actions, service hours, areas served, customer reviews, canonical tags, structured data, `robots.txt`, and `sitemap.xml`.
- GA4 code that records WhatsApp and call clicks. These clicks show intent, but they are not completed orders.

## Important checks before promotion

1. **Biryani guide URL:** The repository links to `/biryani-delivery-tirupur/`, while a search result showed `/blog/biryani-delivery-tirupur/`. The old-path redirect is only a commented example in `tools/nginx-redirects.conf`. Check the live HTTP status, canonical, internal links, and Search Console for both URLs. Keep one URL and redirect the other if both exist. The web tool could not confirm the live HTTP status of those paths.
2. **Sandwich 99 publication/indexing:** The local `restaurants/sandwich-99-tirupur/index.html` already contains a location, six popular items, and item-specific WhatsApp links. A crawled search view showed an older, shorter page. Check what the live server actually serves and request indexing after any genuine update. Do not assume the search snippet reflects the latest page.
3. **Measurement:** Confirm that GA4 receives `whatsapp_click` and `call_click`, then connect enquiries to actual orders in a simple order log. Without that, traffic and click growth cannot be judged against sales.
4. **Live technical audit:** Use Search Console and PageSpeed Insights to check indexing, mobile Core Web Vitals, and errors. This review did not have access to private analytics or Search Console reports, so it does not establish current traffic, rankings, speed scores, or conversion rates.

## Priority plan for sales and SEO

| Priority | Action | Why it matters | Measure |
| --- | --- | --- | --- |
| 1 | Explain delivery pricing with a truthful starting fee or example distance bands, and state that the final total is confirmed before pickup. | Customers currently have to start a chat to learn the likely cost. | Enquiry-to-order rate |
| 2 | Make restaurant pages useful with verified menus or popular items, current prices where available, original photos, location, restaurant hours, and clear item ordering. | Customers can decide what to buy before messaging. | Restaurant page visits to completed orders |
| 3 | Resolve the biryani URL and confirm the live version of updated pages. | Prevent broken promotion links and competing URLs. | Search Console indexing and page traffic |
| 4 | Keep Groods' Google Business Profile accurate: category, services, hours, service area, photos, website, and review replies. | Local search is central for a city delivery business. | Profile interactions and orders attributed to Maps |
| 5 | Publish helpful, specific Tirupur content tied to ordering: lunch options, family biryani, office snacks, cake delivery, and neighbourhood guides. | These answer real customer searches and create entry points beyond the homepage. | Search impressions, qualified visits, orders |
| 6 | Build partner links and distribution: restaurant social profiles, QR cards, bags, and local collaborations. | Partners can send customers who already want their food. | Orders per partner source |

### SEO implementation notes

- Keep one primary search intent per page: general delivery, each service, each restaurant, and each genuinely distinct guide. Avoid creating many near-identical neighbourhood pages.
- Verify the title, description, heading, canonical URL, internal links, and indexability for each important page. The repository already has many of these elements; the work is to validate their live state and improve page usefulness.
- Use local names naturally, including Tirupur/Tiruppur where helpful. Include Tamil information when it serves customers; avoid repetitive keyword blocks.
- Keep restaurant facts current and confirmed with the partner. A menu, price, opening time, or partnership claim that is wrong can lose orders and trust.
- Generate sitemap `lastmod` dates from meaningful page changes. The generator currently stamps all URLs with the generation date, which may not reflect when each page was actually updated.
- Keep FAQs for customer help, but do not rely on FAQ schema for Google rich results; Google limits those results mainly to authoritative government and health sites.
- Test the key mobile pages for loading speed and usability. Improve problems found in actual measurements instead of chasing a perfect score.

## Marketing ideas

### Partner distribution

- Give each restaurant its own Groods ordering link and QR card for the counter, menu, and takeaway bags, with the restaurant's agreement.
- Ask partners to share the link in their Instagram bio or stories and, where appropriate, their business listing.
- Feature one partner or a specific dish at a time with an original photo and a clear ordering link.

### Local campaigns

- Test short Tamil and English posts showing real dishes and delivery use cases. Link each post to the relevant restaurant or service page.
- Try small, geographically focused campaigns only after the landing page clearly shows the offer and how to order. Set a spending cap and assess **cost per completed order** and margin.
- Test a weekday lunch, office snack, or family meal offer only with verified availability and an agreed commercial arrangement.
- Ask satisfied customers for genuine Google reviews after delivery, without requiring a positive rating. Reply to reviews.
- Test a repeat-order benefit if unit economics support it, then compare repeat purchase rate and margin.

## Interactive features to add to the site

| Feature | How it would work | Priority / dependency |
| --- | --- | --- |
| Quick order builder | Customer chooses food, parcel, medicine, or grocery delivery; fills only relevant fields; the site prepares a complete WhatsApp message. | **First**. Keep it short and mobile friendly. |
| Restaurant search and filters | Search by restaurant or dish; filter for meals, biryani, sandwiches, pizza, and desserts. | **First**. Makes the existing directory easier to use. |
| Delivery fee estimator | Select pickup and drop areas to see an estimate and a clear final-price confirmation note. | Next. Requires agreed pricing rules and maintenance. |
| Open-now display | Show Groods' status and next delivery window in Tirupur time; show restaurant hours separately if verified. | Next. Avoid implying a restaurant is open because Groods is open. |
| Repeat order | Save an order summary on the customer's device and prepare the same WhatsApp message next time. | Later. Confirm current menu availability and prices. |
| Order status page | Show confirmed, picked up, and delivered states through a customer link. | Later. Only useful if operations can update it reliably. |

## Features that make the site worth revisiting

- **What should I eat? picker:** Ask for craving, budget, and meal type, then suggest a few relevant Tirupur restaurants with ordering links. Keep recommendations based on available, verified items.
- **Today's picks:** Show a small set of dishes or restaurants with real photos and current information. Assign an owner to refresh it regularly.
- **Group ordering:** Let an office or family collect items through one shared link, then send a consolidated order to Groods. Start with a simple flow before adding accounts or payments.
- **Local food guides:** Create genuinely useful guides with restaurant choices, location context, and direct ordering links.
- **Customer stories:** Show permission-based photos and short accounts of deliveries such as cakes, gifts, or office lunches.

The best initial combination is the quick order builder, restaurant search, and the food picker. These fit the existing WhatsApp workflow. Today's picks should follow only when the team can maintain it.

## Focus plan: Sandwich 99

**Objective:** Bring customers looking for sandwiches, pasta, shakes, and Sandwich 99 delivery to the Groods page, then convert that interest into completed orders.

### Page and SEO

1. Confirm the enriched local Sandwich 99 page is the version served live. It already has six popular dishes and item-specific WhatsApp links in the repository.
2. Verify each dish, the restaurant location, and current availability with Sandwich 99. Add current prices and original dish photos if the restaurant agrees and can keep them updated.
3. Make the restaurant's opening hours distinct from Groods' delivery hours. Show the delivery area and realistic pricing information.
4. Keep the page focused on Sandwich 99 delivery in Tirupur. Link to it from the restaurant directory, food delivery page, and relevant guides.
5. Check its indexing and search queries in Search Console after the live page is confirmed.

### Traffic campaign

1. Get Sandwich 99's agreement to share its Groods page in its Instagram bio/stories, on a counter QR card, and in takeaway bags.
2. Promote a specific dish or agreed combo with a real photo, clear price, delivery terms, and a direct item-order link. Do not advertise a discount without partner agreement.
3. Test a small local campaign around the areas Groods can reliably serve. Use one landing page and distinct tracked links or WhatsApp message labels by channel.
4. Record source, enquiry, completed order, order value, delivery cost, and contribution margin. Continue a channel only if it produces profitable orders or a justified repeat-customer value.

### Suggested two-week test

| Period | Work | Decision point |
| --- | --- | --- |
| Days 1–3 | Verify live page, dishes, prices, hours, photos, and tracking. | Page is accurate and ready for visitors. |
| Days 4–7 | Partner shares the link; place QR material; publish a few dish-focused posts. | Identify which source brings enquiries. |
| Days 8–14 | Run a capped local paid test if the page and fulfilment are ready. | Compare completed orders and margin by source. |

## Measurement dashboard

Review weekly: organic search impressions and clicks; Google Business Profile interactions; landing page visits; WhatsApp and call enquiries; completed orders; enquiry-to-order rate; average order value; contribution margin; repeat orders; and orders by restaurant and campaign. Keep a simple order sheet if there is no integrated ordering system yet.

## Suggested sequence

1. **Week 1:** Verify live URLs and indexing, confirm analytics, start the order-source log, and agree on pricing language.
2. **Weeks 2–3:** Improve the highest-traffic restaurant and service pages; launch the Sandwich 99 partner test.
3. **Weeks 3–5:** Add the quick order builder and restaurant search; publish one or two useful local guides.
4. **After baseline data exists:** Test the food picker, fee estimator, offers, and paid traffic in small increments. Prioritize what produces completed orders and healthy margin.

## Sources and limits

- Site reviewed: [Groods homepage](https://groods.in/), [restaurant directory](https://groods.in/restaurants/), [Sandwich 99 page](https://groods.in/restaurants/sandwich-99-tirupur/), and files in this repository.
- [Google Business Profile local ranking guidance](https://support.google.com/business/answer/7091): complete business information, photos, and reviews support local visibility.
- [Google Search Central on FAQ rich results](https://developers.google.com/search/blog/2023/08/howto-faq-changes): FAQ rich results have limited eligibility.
- [Google Search Central on sitemap `lastmod`](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping): the date should reflect a significant page change.
- [Google Search Central on page experience](https://developers.google.com/search/docs/appearance/page-experience): use performance data as one part of the overall user experience.

This plan is based on a read-only review of public pages and repository files. Private Search Console, GA4, Google Business Profile, order records, partner agreements, and ad account data were unavailable. Numerical targets and campaign budgets should be set after a baseline is measured.
