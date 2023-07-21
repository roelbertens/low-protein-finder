from json import dumps, loads
from typing import Any, Dict, Optional, Iterable, Union

from scrapy import Request, Spider
from scrapy.responsetypes import Response

from scrapers.items import Product

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


class JumboSpider(Spider):
    name = "jumbo"
    allowed_domains = ["jumbo.com"]
    query: str = "query SearchProducts($input: ProductSearchInput!) {\n  searchProducts(input: $input) {\n    redirectUrl\n    removeAllAction {\n      friendlyUrl\n      __typename\n    }\n    pageHeader {\n      headerText\n      count\n      __typename\n    }\n    start\n    count\n    sortOptions {\n      text\n      friendlyUrl\n      selected\n      __typename\n    }\n    categoryTiles {\n      count\n      catId\n      name\n      friendlyUrl\n      imageLink\n      displayOrder\n      __typename\n    }\n    facets {\n      key\n      displayName\n      multiSelect\n      values {\n        ...FacetDetails\n        children {\n          ...FacetDetails\n          children {\n            ...FacetDetails\n            children {\n              ...FacetDetails\n              children {\n                ...FacetDetails\n                children {\n                  ...FacetDetails\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    products {\n      ...ProductDetails\n      crossSells {\n        sku\n        __typename\n      }\n      retailSetProducts {\n        ...ProductDetails\n        __typename\n      }\n      __typename\n    }\n    textMessage {\n      header\n      linkText\n      longBody\n      messageType\n      shortBody\n      targetUrl\n      __typename\n    }\n    socialLists {\n      author\n      authorVerified\n      followers\n      id\n      labels\n      productImages\n      thumbnail\n      title\n      __typename\n    }\n    selectedFacets {\n      values {\n        name\n        count\n        friendlyUrl\n        __typename\n      }\n      __typename\n    }\n    breadcrumbs {\n      text\n      friendlyUrl\n      __typename\n    }\n    seo {\n      title\n      description\n      canonicalLink\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ProductDetails on Product {\n  id: sku\n  brand\n  category: rootCategory\n  subtitle: packSizeDisplay\n  title\n  image\n  inAssortment\n  availability {\n    availability\n    isAvailable\n    label\n    __typename\n  }\n  sponsored\n  link\n  retailSet\n  prices: price {\n    price\n    promoPrice\n    pricePerUnit {\n      price\n      unit\n      __typename\n    }\n    __typename\n  }\n  quantityDetails {\n    maxAmount\n    minAmount\n    stepAmount\n    defaultAmount\n    __typename\n  }\n  primaryBadge: primaryBadges {\n    alt\n    image\n    __typename\n  }\n  secondaryBadges {\n    alt\n    image\n    __typename\n  }\n  badgeDescription\n  promotions {\n    id\n    group\n    isKiesAndMix\n    image\n    tags {\n      text\n      inverse\n      __typename\n    }\n    start {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    end {\n      dayShort\n      date\n      monthShort\n      __typename\n    }\n    attachments {\n      type\n      path\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FacetDetails on Facet {\n  id\n  count\n  name\n  parent\n  friendlyUrl\n  selected\n  __typename\n}\n"

    def start_requests(self) -> Iterable[Request]:
        yield self.search_request()

    def parse(self, response: Response, **kwargs) -> Iterable[Union[Request, Product]]:
        data: Dict[str, Any] = loads(response.text)["data"]["searchProducts"]
        categories = data.get("categoryTiles", [])
        if len(data["breadcrumbs"]) == 0:  # This is the main category
            for category in categories:
                yield self.search_request(
                    category=category["friendlyUrl"],
                )
        else:
            for product in data["products"]:
                yield Request(
                    url=response.urljoin(product["link"]),
                    callback=self.parse_product,
                )
            max_index = data["start"] + len(data["products"])
            if data["count"] > max_index:
                yield self.search_request(
                    category=data["breadcrumbs"][-1]["friendlyUrl"],
                    offset=max_index,
                )

    def parse_product(self, response: Response):
        """

        @url https://www.jumbo.com/producten/jumbo-wit-tijgerbrood-300153STK
        @returns item 1
        """
        table = response.xpath(
            "//table[@data-testid='nutritional-values-table-content']"
        )
        nutrition = {
            row.xpath("./td[1]/text()")
            .extract_first(): row.xpath("./td[2]/text()")
            .extract_first()
            for row in table.xpath(".//tr")
        }
        return Product(
            name=response.xpath(
                "//strong[@data-testid='product-title']/text()"
            ).extract_first(),
            nutrition=nutrition,
        )

    def search_request(self, category: Optional[str] = "", offset: int = 0) -> Request:
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
            query=self.query,
        )
        return Request(
            url="https://www.jumbo.com/api/graphql",
            method="POST",
            body=dumps(payload),
            headers={"Content-Type": "application/json", "Accept-Encoding": "gzip"},
            priority=offset,
        )
