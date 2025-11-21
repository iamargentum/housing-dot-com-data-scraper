# housing.com city-wise data extractor

## what is this?

this is a small script that can be used to extract data from [housing.com](housing.com) and save it to a CSV file.
housing.com uses `graphql` as their API interface. although i don't really know how to write gql queries and we don't have the gql schema that housing.com uses, we can just tap the API request that is made in the browser and recycle it by changing parameters and making it our own. hehe.

## why is this?

a researcher friend needs help with extracting data from housing.com for research purposes and this is DEFINITELY NOT INTENDED FOR ANY USE OTHER THAN ACADEMIC PURPOSES.

## how do i use this?

all of the packages used in this project are inbuilt python packages, so you don't need to set up virtual environments or install any dependencies.

follow these instructions to use this script -
- download this code <insert image here>
    - if you know `git` and have it set up on your machine, you can just clone this repo
    - if you do not know `git`, click on the green `code` button on the top right and click on "Download as zip" and unpack it
- go into the folder where the project is unpacked or cloned
- open a terminal in the folder where the project is unpacked (if you don't know what it means, follow the steps below) <insert images here>
    - for Windows
        - once you are in the folder where the projects are unpacked and you can see the file `getData.py`, `csvUtils.py`, etc. hit ctrl+shift+right mouse click
        - from the list in the menu, select "Open powershell here"
    - for Linux
        - right click in the folder
        - Open terminal here
    - for Mac
        - i don't know
- open your favourite browser
- log on to [housing.com](housing.com)
- copy the request as CURL
    - open developer tools (hit F12)
    - select a city in the dropdown right before search and hit search <insert image here>
    - select "Date added" in the sorting dropdown
    - in the developer tools, select "Network"
    - right click on the lastes entry in the list that looks like <insert api endpoint and query params here>
    - inside the "Copy" submenu, click on copy as cURL
- log on to <insert curl to python request tool url>
- paste what you've copied into the text box on the top
- copy the `json_data` part of the code that gets displayed below
- paste it in the `rawData` variable in `getJSONPayloadforPageRequest`
- change the output file if you want by updating the value of `CSV_FILE_NAME` in the `getData.py` script.
- run the script using `python3` and voila! your data will be shortly (or after some time, based on number of projects in the city you've selected) visible in the output CSV file.
    - 
