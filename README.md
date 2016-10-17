## Airbag

I've been on a big Maltego kick lately, and scoured the web for more sources of information I could start incorporating into Maltego. I found a site a few months ago that has been helpful in identifying certain individuals actual vehicles, VIN numbers, and addresses, and thought this would be a good set of transforms to build. The site is called [vin.place](http://vin.place/) and is pretty basic, you put in a name or VIN and it gets you associated details for the person or vehicle.

For instance, we search on "John Doe" and get a large number of results back:

![http://i.imgur.com/bfWOQBH.png](http://i.imgur.com/bfWOQBH.png)

Clicking on one of the results above, will give us some interesting data back:

![http://i.imgur.com/1YMrCD2.png](http://i.imgur.com/1YMrCD2.png)

While there isn't an API for this available, and plenty of other limitations described below, I thought this data could be a good source for attempting to identify potential addresses or vehicles for a person of interest. To build these transforms, I chose to use BeautifulSoup to help parse the returned HTML and pick up the items of interest. In total, there are three transforms available to use to get more data, "Airbag - Get Addresses", "Airbag - Get Vehicles", and "Airbag - Get VINs". 

The first transform will need a person entity on the map to get started. Let's use our John Doe example again...

![http://i.imgur.com/9cSjYK4.png](http://i.imgur.com/9cSjYK4.png)

Running the "Airbag - Get Addresses" transform returns 12 entities (I'm still using the commercial license, can someone spare some change to get a license? :( ). Running this transform will return "Home" entities which is the residence of the person who bought that vehicle at time of purchase.

There's no other way to filter the searches down to state or anything, so the returned entities will be from all across the country. Another item to note, only a subset of the entire result set is returned, with only 26 vehicles being presented to the user. There's no way to go through pages of results in the site, or through the way I'm doing it (since I'm just going through the site as well). This is a huge limitation of the tool, so, hopefully the person you are looking up has an un-common name, so the result set is not that large.

You can either select one or all the address entities on the graph, and then run the "Airbag - Get Vehicles" transform.

Running this transform will go through each result and scrape the original result page and then print the vehicle information for each result. A "Car" entity will then get returned for each address, looking like this:

![http://i.imgur.com/1BtEEDm.png](http://i.imgur.com/1BtEEDm.png)

You can see in the new car entity, it returns the year, make and model for the vehicle. The last thing we can do with this data set is to get the related VIN numbers for each vehicle. Right-click on the vehicle and run "Airbag - Get VIN". 

The transform will run the results again and pull out the VIN number related with that vehicle.

![http://i.imgur.com/Ol45soU.png](http://i.imgur.com/Ol45soU.png)

### Limitations

There are a number of limitations, some I mentioned previously, however, I'll go over all of them again here.

- Only returns a max of 26 vehicles for a given name, with no way to retrieve more.
- Takes an incredibly long time to return results. I'm not sure if this can be fixed with threading the requests, however, if someone wants to check into that and submit a PR, I'd appreciate it!
- The information isn't high-confidence. While some of the results I've checked out have been valid, there are also a large number of results that are missing, or incorrect. Please take these results with a grain of salt and only think of this as a starting-point and not matter of fact.
- Like above, it's not guaranteed or even probable that you will find who you are looking for in this dataset, I'm not sure where this site got their original data, however, I'm not sure how many total records there are. 
- One thing to note is that there is a "complete list" of data on their site, [http://vin.place/complete.php](http://vin.place/complete.php), which is all the records they have. I'm sure this could be taken and thrown into a database somewhere, and then turned into a remote transform, however, that's not something I was interested in messing with right now.

### Installation

I've covered how to configure local transforms like this in the past, and you can find how to install these in my latest blog post [AlienVault OTX Maltego Transforms](https://nullsecure.org/alienvault-otx-maltego-transforms/). Basically it boils down to installing the .mtz file along with updating the Python interpreter you use, along with where you saved the transforms on your machine. Find all the required files [here](

If you have any questions about this, or bugs (which I'm sure there will be), please create an issue on the GitHub page, or contact me through email or Twitter.
