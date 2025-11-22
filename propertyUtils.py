SOCIETY_AMENITIES_KEY = "Society Amenities" # key for society amenities - i don't know why i created a constant out of it

def getSocietyAmenitiesFromProperty(property: dict) -> str:
    """
    This method takes in a single property, extracts the list of
    amenities and returns all amenities as a comma separated str.
    """
    societyAmenities = 'NA'
    if (
        not property
    ) or (
        not property["details"]
    ) or (
        not property["details"]["amenities"]
    ) or len(property["details"]["amenities"]) == 0: return societyAmenities # which is NA at this point

    societyAmenitiesList = []

    for amenity in property["details"]["amenities"]:
        # found amenities of the type society amenities
        if amenity["type"] == SOCIETY_AMENITIES_KEY:
            societyAmenitiesList = amenity["data"]
            break
    
    # no society amenities found
    if len(societyAmenitiesList) == 0: return societyAmenities # which is NA at this point

    return ", ".join(societyAmenitiesList)
