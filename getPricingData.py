import math
import requests
from time import sleep
from csvUtils import saveInfoToCSV
from propertyUtils import getSocietyAmenitiesFromProperty

PAGE_SIZE = 30  # page size for paginated API - increase if you're in a hurry, but don't be too greedy :)
CSV_FILE_NAME = "./output/Solapur.csv"  # the file where you want your data stored
ENDPOINT = "https://mightyzeus-mum.housing.com/api/gql/stale"  # API endpoint to get data
SOCIETY_AMENITIES_KEY = "Society Amenities" # key for society amenities - i don't know why i created a constant out of it

# request headers
headers = {
    'content-type': 'application/json; charset=UTF-8',
    'phoenix-api-name': 'SEARCH_RESULTS',
    'priority': 'u=1, i',
}

# query params
params = {
    'apiName': 'SEARCH_RESULTS',
    'emittedFrom': 'client_buy_SRP',
    'isBot': 'false',
    'platform': 'desktop',
    'source': 'web',
    'source_name': 'AudienceWeb',
}

def getJSONPayloadforPageRequest(pageNumber: int) -> dict:
    """
    This method builds JSON payload for the request. It accepts
    the page for paginated request and returns JSON payload with
    the page number and configured page size.
    """
    # copy this from the python request created from cURL copied
    # from the network tab
    rawData = {
        'query': '\n  fragment PR on Property {\n    features {\n      label\n      description\n      id\n    }\n    coverImage {\n      src\n      alt\n      videoUrl\n    }\n    polygonsHash\n    creditScore\n    currentPossessionStatus\n    hasAutoVideo\n    imageCount\n    propertyType\n    title\n    subtitle\n    isUc\n    isActiveProperty\n    isMostContacted\n    isRecentlyAdded\n    galleryTitle\n    tracking\n    price\n    displayPrice {\n      value\n      displayValue\n      description\n      unit\n      deposit\n      brokerage\n      maintenance\n      displayMaintenance\n      displayDeposit\n      displayBrokerage\n      totalRent\n      brokerageDuration\n      depositDuration\n      displayParkingCharges\n      displayPaintingCharges\n      paintingDuration\n      lockInPeriod\n    }\n    address {\n      address\n      url\n      detailedPropertyAddress {\n        url\n        val\n      }\n      distanceFromEntity\n      longAddress\n    }\n    url\n    label\n    badge\n    ownerListingBadge\n    listingId\n    postedDate\n    originalListingId\n    promotions\n    customOffers\n    suggestedOffers\n    coords\n    propertyInformation\n    tags\n    furnishingType\n    builtUpArea {\n      value\n      unit\n    }\n    sellerCount\n    meta\n    sellers {\n      ...BS\n      phone {\n        partialValue\n      }\n      isCertifiedAgent\n      isCertifiedProAgent\n      sellerTag\n      adDeficit\n      meta\n      contactPersonId\n    }\n    emi\n    brands {\n      name\n    }\n    porDetails {\n      apartmentTypeId\n      apartmentType\n      displayMinPrice\n      displayMaxPrice\n      range\n    }\n    details {\n      avgPriceValue\n      sliceViewUrl\n      images {\n        type\n        images {\n          src\n          alt\n          aspectRatio\n          isSvOrDcVerified\n          category\n          caption\n          tag\n          type\n        }\n      }\n      uniqueAmenities {\n        name\n        icon\n      }\n      config {\n        displayAreaType\n        propertyConfig {\n          key\n          label\n          propertyTypeName\n          range\n          priceOnRequest\n          data {\n            id\n            price {\n              value\n              displayValue\n              unit\n            }\n            areaConfig {\n              name\n              areaInfo {\n                value\n                unit\n                displayArea\n              }\n            }\n            projectAttributes {\n              reraIdStatus\n            }\n          }\n        }\n      }\n      propertyConfigs {\n        id\n        icon\n        label\n        description\n        meta\n        showOnMobile\n        mobileLabel\n        formattedDescription\n      }\n    }\n    minDistanceLocality {\n      distance\n      name\n    }\n    isAuctionFlat\n    photoUnderReview\n    propertyTags\n    isMyGateCertified\n    isExclusiveProperty\n    eventIds\n  }\n  fragment SR on Property {\n    ...PR\n    certifiedDetails {\n      isVerifiedProperty\n      similarPropertyKeys\n      isCertifiedProperty\n    }\n    verificationStatus\n    description {\n      overviewDescription\n      highlights\n    }\n    videoTour {\n      startDate\n      endDate\n      url\n      meetingNumber\n    }\n    highlights\n    brands {\n      name\n      image\n      theme {\n        color\n      }\n      url\n    }\n    boostedAs\n  }\n  fragment BS on User {\n    name\n    id\n    image\n    firmName\n    url\n    type\n    isPrime\n    sellerBadge\n    isPaid\n    designation\n    formattedCustomerServedCount\n    sellerOverlayColor\n    sellerOverlayTextColor\n  }\n  fragment Ad on SearchResults {\n    nearbyProperties {\n      ...SR\n      nearByPlaces {\n        establishmentType\n        name\n        distance\n        travelDistance\n        duration\n      }\n    }\n    promotedProperties {\n      type\n      properties {\n        ...PR\n        videoConnectAvailable\n        micrositeRedirectionURL\n      }\n    }\n    collections {\n      title\n      subTitle\n      image\n      propertyCount\n      url\n      key\n    }\n    sellers @include(if: $addSellersData) {\n      name\n      id\n      image\n      firmName\n      url\n      type\n      isPrime\n      sellerBadge\n      isPaid\n      designation\n      stats {\n        label\n        description\n      }\n      meta\n      description\n      sellerDescription\n      cities {\n        id\n        name\n        image\n      }\n      phone {\n        partialValue\n      }\n    }\n  }\n  query(\n    $pageInfo: PageInfoInput\n    $city: CityInput\n    $hash: String!\n    $service: String!\n    $category: String!\n    $pageTypeMajor: String\n    $meta: JSON\n    $adReq: Boolean!\n    $getStructured: Boolean!\n    $fltcnt: String\n    $isLandmarkSearchActive: Boolean\n    $addSellersData: Boolean!\n    $interestLedFilter: String\n    $isMapSearch: Boolean\n    $lat: Float\n    $lng: Float\n    $outerRadius: Float\n    $amenities: [String]\n    $amenityPageSearch: Boolean\n    $showCarouselTags: Boolean\n    $whatsChanged: Boolean\n  ) {\n    searchResults(\n      hash: $hash\n      service: $service\n      category: $category\n      city: $city\n      pageTypeMajor: $pageTypeMajor\n      pageInfo: $pageInfo\n      meta: $meta\n      fltcnt: $fltcnt\n      isLandmarkSearchActive: $isLandmarkSearchActive\n      interestLedFilter: $interestLedFilter\n      isMapSearch: $isMapSearch\n      lat: $lat\n      lng: $lng\n      outerRadius: $outerRadius\n      amenities: $amenities\n      amenityPageSearch: $amenityPageSearch\n      showCarouselTags: $showCarouselTags\n      whatsChanged: $whatsChanged\n    ) {\n      properties {\n        ...SR\n        videoConnectAvailable\n        updatedAt\n        updatedAtStr\n        verifiedAt\n        digitour {\n          url\n        }\n        nearByPlaces {\n          establishmentType\n          name\n          distance\n          travelDistance\n          duration\n        }\n        socialUrgency {\n          msg\n        }\n        socialContext {\n          msg\n        }\n        isBrokerageChargeable\n        reviewRating\n        projectReviewVideo\n        showNewLaunch\n        isTitanium\n        isLocalityChampion\n        distanceFromCoords\n        saleTag\n        entityProjectName\n        details {\n          amenities {\n            type\n            data\n          }\n          brochure {\n            pdf\n            name\n            hasBrochure\n          }\n        }\n        insights {\n          id\n          value\n        }\n        coverImageUrl\n        carouselTags\n      }\n      ...Ad @include(if: $adReq)\n      config {\n        filters\n        pageInfo {\n          totalCount\n          size\n          page\n        }\n        entities {\n          id\n          type\n          locationCoordinates\n        }\n      }\n      lastUpdatedAt\n      meta\n      structuredData @include(if: $getStructured)\n      socialProofingIndexes\n      npoPropertiesData {\n        totalCount\n        properties {\n          ...SR\n          videoConnectAvailable\n          updatedAt\n          digitour {\n            url\n          }\n          nearByPlaces {\n            establishmentType\n            name\n            distance\n            travelDistance\n            duration\n          }\n          socialUrgency {\n            msg\n          }\n          socialContext {\n            msg\n          }\n          isBrokerageChargeable\n          reviewRating\n          showNewLaunch\n          distanceFromCoords\n        }\n      }\n    }\n  }\n',
        'variables': '{"hash":"P5efs9x6b7ntxvtq5S6Y1","service":"buy","category":"residential","city":{"name":"Solapur","id":"9c063c324bb50fc74f83","cityId":"c28001a2733c14136d3d","url":"solapur_maharashtra","isTierTwo":true,"products":["buy","plots","commercial","paying_guest","rent"]},"pageTypeMajor":"SRP","pageInfo":{"page":1,"size":30},"meta":{"filterMeta":{},"url":"/in/buy/searches/P5efs9x6b7ntxvtq5S6Y1","shouldModifySearchResults":true,"pagination_flow":false,"enableExperimentalFlag":false,"isDeveloperSearch":false},"bot":false,"getStructured":true,"adReq":true,"fltcnt":"","isLandmarkSearchActive":true,"addSellersData":false,"interestLedFilter":"","isMapSearch":false,"lat":0,"lng":0,"outerRadius":0,"amenities":[],"amenityPageSearch":false,"whatsChanged":false}',
    }

    rawData["variables"] = rawData["variables"].replace(  # replace page number and size to be dynamic
        '"page":1,"size":30',
        f"\"page\":{pageNumber},\"size\":{PAGE_SIZE}"
    )

    return rawData

def makeRequest(pageNumber: int) -> requests.Response:
    """
    This method makes the actual HTTP request and returns the
    response. Since this is a paginated request, it accepts page
    number as an argument.
    """
    return requests.post(
        ENDPOINT,
        params=params,
        headers=headers,
def pushResponseToCSV(city: str, jsonResponse: dict) -> None:
    """
    This method accepts the JSON response of the api, massages
    the data, structures it to fit in a CSV format and saves it
    in the configured CSV file.
    It takes care of creating the CSV file if it does not already
    exist.
    If the CSV file already exists, it just appends data to the
    file.
    """
    propertyInfos = []
    for property in jsonResponse["data"]["searchResults"]["properties"]:
        # built-up area
        builtUpAreaUnit = "NA"
        builtUpAreaValue = "NA"

        if property["builtUpArea"]:
            builtUpAreaUnit = property["builtUpArea"]["unit"]
            builtUpAreaValue = property["builtUpArea"]["value"]

        builtUpArea = "NA" if builtUpAreaValue == "NA" else f"{builtUpAreaValue} {builtUpAreaUnit}"

        # number of bedrooms and bathrooms and parking
        numParking = "NA"
        numBedrooms = "NA"
        numBathrooms = "NA"
        propertyInfoArea = "NA"

        if property["propertyInformation"]:
            numParking = property["propertyInformation"].get("parking") if property["propertyInformation"].get("parking") != None else "NA"
            numBedrooms = property["propertyInformation"].get("bedrooms") if property["propertyInformation"].get("bedrooms") != None else "NA"
            numBathrooms = property["propertyInformation"].get("bathrooms") if property["propertyInformation"].get("bathrooms") != None else "NA"
            propertyInfoArea = property["propertyInformation"].get("area") if property["propertyInformation"].get("area") != None else "NA"

        # list of data to be appended to the CSV
        propertyInfos.append({
            "Property type": property["propertyType"],
            "Project name": property["entityProjectName"],
            "Price": property["price"],
            "Address": property["address"]["address"],
            "URL": property["url"],
            "Listing ID": property["listingId"],
            "Original listing ID": property["originalListingId"],
            "Built-up area": builtUpArea,
            "# of bedrooms": numBedrooms,
            "# of bathrooms": numBathrooms,
            "# of parking": numParking,
            "Area": propertyInfoArea,
            "RERA verified": "YES" if "rera_verified" in property["tags"] else "NO",
            "Amenities": getSocietyAmenitiesFromProperty(property=property)
        })
    # put property infos into a csv
    saveInfoToCSV(propertyInfos=propertyInfos, csvFileName=CSV_FILE_NAME)

def getData() -> None:
    """
    The main function that makes the API call, extracts and
    structures the data and saves it to the configured CSV file.
    """
    # initialize with 1
    startingPage = 1
    totalNumberOfPages = 1

    # request for first page
    response = makeRequest(startingPage)
    jsonResponse = response.json()
    pushResponseToCSV(jsonResponse=jsonResponse)
    
    # jsonResponse.searchResults.config.pageInfo.page
    totalNumberOfPages = math.ceil(jsonResponse["data"]["searchResults"]["config"]["pageInfo"]["totalCount"]/PAGE_SIZE)

    for pageNumber in range(startingPage + 1, totalNumberOfPages):
        response = makeRequest(pageNumber=pageNumber)
        jsonResponse = response.json()
        pushResponseToCSV(jsonResponse)
        sleep(2)

if __name__ == "__main__":
    getData()