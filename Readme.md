#### Status
Currenlty breaks

### Description

##### Random Wallpaper
- Change wallpaper randomly for a given search query eg '--query cute+puppy+images' ( does not parse spaces, hence the '+' sign)
- Scraps for wallaper links for a search query
- creates a db (json list) file for that search query in the 'db' folder works as a cache so scrapping is only done once i.e if the file is not created
- gets a random links from the db
- Download and store in 'images/{search_query}/' folder
- Than set this image as wallpaper

##### Random Wikipedia Article
- Change wallpaper to a screenshot of a random wikipedia article

