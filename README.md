# GearUp

**Author:** Anna Giacomello

## Introduction
GearUp is a service-oriented application that helps beginner hikers to find huts and treks, and, more importantly, to find the appropriate gear for their needs.  
The functionalities are the following. A user can:

- Search for a place as the starting point of their hike, as well as a date for the hike and a radius in kilometers for the search of the huts.
- Choose from the list of huts that get returned.
- See the details of the hike (weather, elevation profile, length of the trail) and the recommended gear. The gear is taken from a database and the parameters used to choose the appropriate items to recommend are computed based on the weather, the temperature, and the length and elevation gain of the trail.
- Set the displayed items as favourites and see all the favourite items in a dedicated page.

## Architecture of the project

### Adapter Layer
The adapter layer is responsible for sending the API calls to the external resources. There were two main external resources used for retrieving the necessary information.

#### Google
Google was used in several endpoints to perform requests to different APIs. In particular:

- **`coordinates`**: This endpoint uses Google Geocode API to retrieve the coordinates corresponding to a certain place.
- **`elevation`**: Uses Google Elevation API to get the elevation of a provided route in a given number of points (in the case of the application, once every 100 meters).
- **`huts`**: Uses Google Places API to get the huts within a certain radius from a provided set of coordinates.
- **`hutimage`**: Uses Google Places API to retrieve an image based on a specific photo reference.
- **`trails`**: Fetches the walking route between two sets of coordinates by using Google Directions API.
- **`trailimage`**: Given the encoded polyline of a trail, fetches the image of the route by resorting to Google Staticmap API.

#### Open Weather Map
Open Weather Map was used to get information about the weather conditions and temperature.

- **`weatherforecasts`**: This endpoint makes a call to Open Weather Map API to get weather information about a certain date in a place identified by a given set of coordinates.
- **`weathericon`**: This endpoint calls Open Weather Map API to fetch the weather icon corresponding to a given icon id.

### Data Layer
The data layer hosts the database, together with the models defining the tables and the endpoints managing the operations to the database. SQLite served as the database, with SQLAlchemy used as the Object-Relational Mapping framework to manage and interact with it.

#### Tables
- **Users**: This table stores information about the users, namely name, last name, and email. When a user logs in for the first time, the entry corresponding to their data is created.
- **Gear**: Gear contains information about several items useful for hiking. This table is populated as a preliminary step in the initialization of the application.
- **FavouriteGear**: FavouriteGear stores the items marked as favourites by a user. To ensure no ambiguity or conflicts, a constraint was put in place to ensure that the combination of email and gear code is unique.

#### Endpoints
The endpoints of the application are used to perform the operations on the database, namely adding new users and favourite gear items, and retrieving user information, gear items, and information about favourite gear related to a given user.

### Business Logic Layer
The Business logic layer is organized in four different services, each one running their own application.

#### Weather
Weather is responsible for retrieving and processing weather information.  
The application receives as parameters of the request a date and a location. It then makes a call to the `coordinates` endpoint in the adapter layer to retrieve the coordinates corresponding to the provided location. It then feeds the coordinates and the date (appropriately formatted) to the `weatherforecasts` endpoint in the adapter layer to retrieve weather information. This data is then processed to only return the weather, the temperature, the precipitation information, and the icon id corresponding to the weather.

#### Huts
Huts receives as parameters a location and a radius in meters. It then proceeds to fetch the coordinates corresponding to the location by calling the `coordinates` endpoint in the adapter layer. It then feeds the coordinates and the radius to the `huts` endpoint in the adapter layer. It then processes the response and returns a list of huts, each one containing information regarding the huts' id, name, rating, coordinates, and picture.

#### Trails
Trails receives as parameters the start and end location of the trails. It then retrieves the corresponding coordinates by posting a request to the `coordinates` endpoint in the adapter layer. It then uses the received coordinates to get the trail information from the `trails` endpoint in the adapter layer. The data is then used to get the elevation profile of the trail by calling the `elevation` endpoint in the adapter layer. This information is then processed and the link to the Google Maps directions, the length, the elevation profile, and the polyline is returned.

#### Gear
Gear is responsible for calculating the item parameters based on the weather (weather conditions, precipitation volume, temperature) and on the trail (length and elevation profile). These parameters are then used to retrieve the appropriate gear from the database. The list of items is then returned.

### Process-Centric Layer
The process-centric layer was implemented as a single application and is responsible for managing the user inputs by orchestrating the services in the other layers.  
Redis was employed for server-side session management.

#### Home
It is used to render the home page of the application (`index.html`). The page contains links to allow the user to log out, see their favourite items, and start the search process.

#### Login
The login page is rendered from every endpoint of the application whenever a user is not in session (either because the session has expired or because the user has logged out). The login is implemented by using Google OAuth 2.0.

#### Search and Results
The `search` endpoint displays the `search.html` page. The page allows the user to insert a location as the starting point of the hike, a radius in kilometers, a date for the hike, and a gender for the gear recommendations.  
The `results` endpoint displays the results (always in `search.html`) of the huts search, performed by calling the Huts service in the business logic layer. Moreover, weather data is retrieved by calling the Weather service in the business logic layer.

#### Results Details
By clicking on a specific hut from the results, the user can see the details of the hike (length, altitude profile, map image) and the gear recommendation. All this information gets displayed in the `results.html` page; the data is provided by the endpoint, which calls the Trails and Gear services in the business logic layer.  
Here the user can set gear items as favourites, or remove them by clicking on the heart beside each item; this will trigger a call to the `manage_favourites` endpoint.

#### Manage Favourites
This endpoint gets called each time an item has to be added or removed from the favourites. It is responsible for calling the `add_favourite_gear` and `remove_favourite_gear` endpoints in the data layer respectively.

#### Display Favourites
From anywhere in the application, the user can see the items set as favourites. These are retrieved from the data layer by calling the `get_favourite_gear` endpoint, and subsequently the `get_gear` endpoint to get the details of each piece of equipment.  
The user can decide to remove an item from the favourites by pressing the appropriate button.

#### Error
The `error.html` page gets displayed whenever an exception is raised or the HTTP call does not return a successful status code. The error is reported in the page for clarity to the user.
