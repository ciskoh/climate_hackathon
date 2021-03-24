React Frontend Organization
------------

    ├── README.md            <- The frontend README for developers using this project.
    ├── data
    │   ├── index.html       
    │   ├── manifest.json              
    │   └── robots.txt            
    │
    ├── package.json         <- Install all dependecies (yarn install)
    └── src                  <- Source code for use in this project.
        │
        ├── assets           <- images used in the project.
        │  
        ├── components                        
        │   ├── landProBase  <- material about landpro and the basic publication
        │   ├── mapComponent <- leaflet map component
        │   ├── navi         <- navi component for all the different pages
        │   └── teamMembers  <- team members basic info and card component
        │  
        ├── pages                        
        │   ├── about        <- about page about our group
        │   ├── home         <- home page with the background, inspiration and other details
        │   └── map          <- the interactive map page
        │  
        ├── routes           <- router file with the different routes
        │ 
        └── store            <- a preparation infrastructure to import and export needed data                        
            ├── actions      <- 
            ├── reducers     <- 
            ├── constants    <- 
            └── index.js     <- the store file
            
 after installing the dependencies, to start the website locally just run the command yarn start if used yarn install or npm start if used npm install
