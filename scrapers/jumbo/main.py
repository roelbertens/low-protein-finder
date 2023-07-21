from json import dumps
from pathlib import Path

from requests import post
from tqdm import tqdm

QUERY = "query SearchProducts($input: ProductSearchInput!) {\n  searchProducts(input: $input) {\n    redirectUrl\n    removeAllAction {\n      friendlyUrl\n      __typename\n    }\n    pageHeader {\n      headerText\n      count\n      __typename\n    }\n    start\n    count\n    sortOptions {\n      text\n      friendlyUrl\n      selected\n      __typename\n    }\n    categoryTiles {\n      count\n      catId\n      name\n      friendlyUrl\n      imageLink\n      displayOrder\n      __typename\n    }\n    facets {\n      key\n      displayName\n      multiSelect\n      values {\n        ...FacetDetails\n        children {\n          ...FacetDetails\n          children {\n            ...FacetDetails\n            children {\n              ...FacetDetails\n              children {\n                ...FacetDetails\n                children {\n                  ...FacetDetails\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products {\n      ...ProductDetails\n      crossSells {\n        sku\n        __typename\n      }\n      retailSetProducts {\n        ...ProductDetails\n        __typename\n      }\n      __typename\n    }\n    textMessage {\n      header\n      linkText\n      longBody\n      messageType\n      shortBody\n      targetUrl\n      __typename\n    }\n    socialLists {\n      author\n      authorVerified\n      followers\n      id\n      labels\n      productImages\n      thumbnail\n      title\n      __typename\n    }\n    selectedFacets {\n      values {\n        name\n        count\n        friendlyUrl\n        __typename\n      }\n      __typename\n    }\n    breadcrumbs {\n      text\n      friendlyUrl\n      __typename\n    }\n    seo {\n      title\n      description\n      canonicalLink\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductDetails on Product {\n  id: sku\n  brand\n  category: rootCategory\n  subtitle: packSizeDisplay\n  title\n  image\n  inAssortment\n  availability {\n    availability\n    isAvailable\n    label\n    __typename\n  }\n  sponsored\n  link\n  retailSet\n  prices: price {\n    price\n    promoPrice\n    pricePerUnit {\n      price\n      unit\n      __typename\n    }\n    __typename\n  }\n  quantityDetails {\n    maxAmount\n    minAmount\n    stepAmount\n    defaultAmount\n    __typename\n  }\n  primaryBadge: primaryBadges {\n    alt\n    image\n    __typename\n  }\n  secondaryBadges {\n    alt\n    image\n    __typename\n  }\n  badgeDescription\n  promotions {\n    id\n    group\n    isKiesAndMix\n    image\n    tags {\n      text\n      inverse\n      __typename\n    }\n    start {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    end {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    attachments {\n      type\n      path\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FacetDetails on Facet {\n  id\n  count\n  name\n  parent\n  friendlyUrl\n  selected\n  __typename\n}\n"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Sec-Fetch-Site": "same-origin",
    "Accept-Language": "en-GB,en;q=0.9",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Sec-Fetch-Mode": "cors",
    "Host": "www.jumbo.com",
    "Origin": "https://www.jumbo.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15",
    "Referer": "https://www.jumbo.com/producten/brood-en-gebak",
    # 'Content-Length': '2824',
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "apollographql-client-name": "basket-app-apollo-client",
}


def search_request(category: str | None = "", offset: int = 0) -> dict:
    """Create a search request.

    A request takes a category and an offset. A category looks like:
     "zuivel,-eieren,-boter/?searchType=category", and the offset
    is the distance from the start of the search results. Typically
    24 results are returned.

    Searching for an empty category results in _all products_.
    """
    input_variables = dict(
        searchType="category",
        searchTerms="producten",
        friendlyUrl=category,
        offSet=offset,
        bloomreachCookieId="",
    )
    payload = dict(
        operationName="SearchProducts",
        variables=dict(input=input_variables),
        query=QUERY,
    )
    result = post(
        url="https://www.jumbo.com/api/graphql",
        json=payload,
        # cookies=cookies,
        headers=HEADERS,
    )
    return result.json()["data"]["searchProducts"]


if __name__ == "__main__":
    results = []
    data = search_request()
    categories = data.get("categoryTiles", [])
    for category in categories:
        print("Category", category["friendlyUrl"])
        data = search_request(category=category["friendlyUrl"], offset=0)
        with tqdm(total=data["count"]) as t:
            while True:
                offset = data["start"]
                t.update(len(data["products"]))
                results += data["products"]
                if data["count"] <= offset or len(data["products"]) == 0:
                    break
                data = search_request(
                    category=category["friendlyUrl"],
                    offset=offset + len(data["products"]),
                )
        print()
    Path("jumbo_products.json").write_text(dumps(results))
