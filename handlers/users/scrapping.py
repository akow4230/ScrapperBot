import requests


def get_product_details(soup):
    products = []

    product_list = soup.select('.a-section.a-spacing-base')

    for product in product_list:
        # Extract title
        title_element = product.select_one('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 a')
        if title_element:
            title = title_element.get_text(strip=True)
        else:
            continue  # Skip this product if title is not found

        # Extract new price
        price_element = product.select_one('.s-price-instructions-style .a-price .a-offscreen')
        if price_element:
            new_price = price_element.get_text(strip=True)
        else:
            continue  # Skip this product if new price is not found

        # Extract old price and discount amount
        price_section = product.select_one('.s-price-instructions-style')
        if price_section:
            old_price_element = price_section.select_one('.a-price.a-text-price .a-offscreen')
            if old_price_element:
                old_price = old_price_element.get_text(strip=True)
            else:
                continue  # Skip this product if old price is not found

            discount_text = price_section.get_text(strip=True)
            discount_start = discount_text.find('(')
            discount_end = discount_text.find(')')
            discount = discount_text[
                       discount_start + 1:discount_end] if discount_start != -1 and discount_end != -1 else None
        else:
            continue  # Skip this product if price section is not found

        # Extract URL
        url_element = product.select_one('a.a-link-normal.s-no-outline')
        if url_element:
            url = url_element.get('href')
            if url:
                try:
                    base_url = f"https://www.amazon.in{url}"
                    url_parts = url.split('/dp/')
                    if len(url_parts) > 1:
                        url = base_url.split('/dp/')[0] + '/dp/' + url_parts[1].split('/')[
                            0] + '?&linkCode=ll1&tag=gauravbisht20-21'
                    else:
                        continue  # Skip this product if URL is malformed
                except IndexError:
                    continue  # Skip this product if an IndexError occurs
            else:
                continue  # Skip this product if URL is not found
        else:
            continue  # Skip this product if URL element is not found

        # Add product to list if all data is available
        products.append({
            'title': title,
            'new_price': new_price,
            'old_price': old_price,
            'discount': discount if discount else "No discount found",
            'url': url,
        })



    return products


def get_main(url, page_limit=400):
    headers = {
        'authority': 'www.amazon.in',
        'method': 'GET',
        'path': '/s?bbn=976392031&rh=n%3A976392031%2Cp_n_pct-off-with-tax%3A2665400031&dc&qid=1723088612&rnid=2665398031&ref=lp_976393031_nr_p_n_pct-off-with-tax_1',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en,ru;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'cookie': 'session-id=261-4182904-4995521; i18n-prefs=INR; ubid-acbin=262-8264721-2298530; session-id-time=2082787201l; session-token=IGnTEUY1x45h/AQ9/2T160UBIT7Pz3oc4BGje35TfEikgq5/WZY1idZIdLv3fwzlrdjtHJhDO1na8vjy8iEjAsueYl76MMsy8phg0SOLRzIZ5QqajaWNqUrrtkzxt1VX0OwFdf9Rz97lIjGnpTP13BD24gJMt2xl1l2NxmasxgS5bSoYDvMDm3PdjWtJfq00d0lf3MxC3GB1tLKnCleGQPA9pDIDNfcsJK6IRKLfxa8rtbf9ORfQEKH2E7VndKjvbZYFksDGhwXVVlmvj14ljNPnVN0O02MfFitIKDE1vy7vPbKZrxl8VNpG9wqprkek1Qqs/lgV1mjPpYnmJ3bpD99GvUH6hqjN; csm-hit=tb:DEXPTR54M661C4DGEFKM+s-XK45BRDTRSPJ2MZZYTDC|1723088624209&t:1723088624209&adb:adblk_no',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1.25',
        'ect': '4g',
        'priority': 'u=0, i',
        'referer': 'https://www.amazon.in/',
        'rtt': '200',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.25',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-ch-viewport-width': '1488',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'viewport-width': '1488',
    }

    current_page = 1
    all_products = []

    while current_page <= page_limit:
        print(f"Fetching page {current_page}")
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = get_product_details(soup)
            all_products.extend(products)

            print(f"Page {current_page} processed.")

            # Find the URL for the "Next" page
            next_page = soup.find('a', {'class': 's-pagination-next'})
            if next_page and 'href' in next_page.attrs:
                next_url = "https://www.amazon.in" + next_page['href']
                print(next_url)
                url = next_url
                current_page += 1
            else:
                print("No more pages found.")
                break
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            break




