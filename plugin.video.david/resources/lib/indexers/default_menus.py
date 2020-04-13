
class DefaultMenus:
    
    def RootList(self):
        return [

            {
                "iconImage": "movies.png", 
                "mode": "navigator.main",
                "action": "MovieList",
                "name": "Movies", 
                "foldername": "Movies",
            }, 

            {
                "iconImage": "tvshows.png", 
                "mode": "navigator.main",
                "action": "TVShowList",
                "name": "TV Shows", 
                "foldername": "TV Shows",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "navigator.main", 
                "action": "MovieListTrakt",
                "name": "My Movies (Trakt)", 
                "foldername": "My Movies Trakt",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "navigator.main", 
                "action": "TVShowListTrakt",
                "name": "My TV Shows (Trakt)", 
                "foldername": "My TV Shows Trakt",
            }, 

#             {
#                 "iconImage": "trakt.png", 
#                 "mode": "navigator.my_trakt_content", 
#                 "name": "My Lists & Widgets (Trakt)", 
#                 "foldername": "My Lists Trakt",
#             }, 

            {
                "iconImage": "trakt.png", 
                "mode": "build_next_episode", 
                "name": "New Episodes", 
                "foldername": "New Episodes",
            }, 

            {
                "iconImage": "search.png", 
                "mode": "navigator.search", 
                "name": "Search", 
                "foldername": "Search",
            }, 

            {
                "iconImage": "tools.png", 
                "mode": "navigator.tools", 
                "name": "Tools", 
                "foldername": "Tools",
            } 

        ]


    def MovieList(self):
        return [

            {
                "name": "In Theaters", 
                "iconImage": "in-theaters.png", 
                "foldername": "In Theaters", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_in_theaters",
            }, 

            {
                "action": "tmdb_movies_premieres", 
                "iconImage": "latest-movies.png", 
                "mode": "build_movie_list", 
                "name": "Premieres", 
                "foldername": "Movies Premiering",
            }, 

            {
                "name": "Latest Releases", 
                "iconImage": "latest-movies.png", 
                "foldername": "Latest Releases", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_latest_releases",
            }, 

            {
                "name": "Most Popular", 
                "iconImage": "most-popular.png", 
                "foldername": "Most Popular", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_popular",
            }, 

            {
                "name": "Trending", 
                "iconImage": "featured.png", 
                "foldername": "Trending", 
                "mode": "build_movie_list", 
                "action": "trakt_movies_trending",
            }, 

            {
                "name": "Genres", 
                "menu_type": "movie", 
                "iconImage": "genres.png", 
                "foldername": "Genres", 
                "mode": "navigator.genres",
            }, 

            {
                "action": "trakt_movies_top10_boxoffice", 
                "iconImage": "box-office.png", 
                "mode": "build_movie_list", 
                "name": "Top 10 Box Office", 
                "foldername": "Movies Box Office",
            }, 

            {
                "name": "Blockbusters", 
                "iconImage": "most-voted.png", 
                "foldername": "Blockbusters", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_blockbusters",
            }, 

            {
                "name": "Top Rated", 
                "iconImage": "highly-rated.png", 
                "foldername": "Top Rated", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_top_rated",
            }, 

            {
                "name": "Up Coming", 
                "iconImage": "userlists.png", 
                "foldername": "Up Coming", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_upcoming",
            }, 

            {
                "name": "Anticipated", 
                "iconImage": "latest-movies.png", 
                "foldername": "Anticipated", 
                "mode": "build_movie_list", 
                "action": "trakt_movies_anticipated",
            }, 

            {
                "name": "Oscar Winners", 
                "iconImage": "oscar-winners.png", 
                "foldername": "Oscar Winners", 
                "mode": "build_movie_list", 
                "action": "imdb_movies_oscar_winners",
            }, 

            {
                "name": "Mosts", 
                "menu_type": "movie", 
                "iconImage": "trakt.png", 
                "foldername": "Mosts", 
                "mode": "navigator.trakt_mosts",
            }, 

            {
                "name": "Languages", 
                "menu_type": "movie", 
                "iconImage": "languages.png", 
                "foldername": "Movie Languages", 
                "mode": "navigator.languages", 
            }, 

            {
                "name": "Years", 
                "menu_type": "movie", 
                "iconImage": "years.png", 
                "foldername": "Movie Years", 
                "mode": "navigator.years", 
            }, 

            {
                "name": "Certifications", 
                "menu_type": "movie", 
                "iconImage": "certificates.png", 
                "foldername": "Certifications", 
                "mode": "navigator.certifications",
            }, 

            {
                "name": "Because You Watched", 
                "iconImage": "library_update.png", 
                "foldername": "Because You Watched", 
                "mode": "navigator.because_you_watched", 
                "menu_type": "movie",
            }, 

            {
                "name": "Popular People", 
                "iconImage": "people.png", 
                "foldername": "Popular People", 
                "mode": "build_movie_list", 
                "action": "tmdb_popular_people",
            }, 

            {
                "name": "Favourites", 
                "iconImage": "userlists.png", 
                "foldername": "Movie Favourites", 
                "mode": "build_movie_list", 
                "action": "favourites_movies",
            }, 

            {
                "name": "Subscriptions", 
                "iconImage": "library_update.png", 
                "foldername": "Subscriptions", 
                "mode": "build_movie_list", 
                "action": "subscriptions_movies",
            }, 

            {
                "name": "Kodi Library", 
                "iconImage": "library_update.png", 
                "foldername": "Kodi Library", 
                "mode": "build_movie_list", 
                "action": "kodi_library_movies",
            }, 

            {
                "name": "Kodi Library - Recently Added", 
                "iconImage": "library_update.png", 
                "foldername": "Recently Added to Kodi Library", 
                "mode": "build_kodi_library_recently_added", 
                "db_type": "movies",
            }, 

            {
                "iconImage": "trakt.png", 
                "action": "MovieListTrakt",
                "name": "My Movies (Trakt)", 
                "foldername": "My Movies Trakt",
            }, 

            {
                "name": "Search", 
                "iconImage": "search.png", 
                "foldername": "Movie Search", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_search", 
                "query": "NA",
            }, 

            {
                "name": "People Search", 
                "iconImage": "people-search.png", 
                "foldername": "People Movie Search", 
                "mode": "people_search.search", 
            }, 

            {
                "foldername": "Movie Search History", 
                "iconImage": "search.png", 
                "mode": "search_history", 
                "action": "movie",
                "name": "Search History",
            }

        ]


    def MovieListTrakt(self):
        return [

            {
                "name": "Trakt Collection", 
                "iconImage": "trakt.png", 
                "foldername": "Trakt Collection", 
                "mode": "build_movie_list", 
                "action": "trakt_collection",
            }, 

            {
                "name": "Trakt Watchlist", 
                "iconImage": "trakt.png", 
                "foldername": "Trakt Watchlist", 
                "mode": "build_movie_list", 
                "action": "trakt_watchlist",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.get_trakt_my_lists", 
                "name": "Trakt My Lists", 
                "foldername": "Trakt My Personal Lists",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.get_trakt_liked_lists", 
                "name": "Trakt Liked Lists", 
                "foldername": "Trakt Liked Lists",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.search_trakt_lists", 
                "name": "Trakt Search User Lists", 
                "foldername": "Trakt Search Lists",
            }, 

            {
                "name": "Trakt Recommendations", 
                "iconImage": "trakt.png", 
                "foldername": "Trakt Recommendations", 
                "mode": "build_movie_list", 
                "action": "trakt_recommendations",
            }, 

            {
                "foldername": "Watched Movies", 
                "iconImage": "trakt.png", 
                "mode": "build_movie_list",  
                "action": "watched_movies", 
                "name": "Watched Movies",
            }, 

            {
                "foldername": "In Progress Movies", 
                "iconImage": "trakt.png", 
                "mode": "build_movie_list",  
                "action": "in_progress_movies", 
                "name": "In Progress Movies",
            }

        ]
    

    def TVShowList(self):
        return [

            {
                "action": "tmdb_tv_popular", 
                "iconImage": "most-popular.png", 
                "mode": "build_tvshow_list", 
                "name": "Most Popular", 
                "foldername": "TV Most Popular",
            }, 

            {
                "action": "trakt_tv_trending", 
                "iconImage": "featured.png", 
                "mode": "build_tvshow_list", 
                "name": "Trending", 
                "foldername": "TV Trending",
            }, 

            {
                "action": "tmdb_tv_premieres", 
                "iconImage": "new-tvshows.png", 
                "mode": "build_tvshow_list", 
                "name": "Premieres", 
                "foldername": "TV Premiering",
            }, 

            {
                "action": "tmdb_tv_top_rated", 
                "iconImage": "highly-rated.png", 
                "mode": "build_tvshow_list", 
                "name": "Top Rated", 
                "foldername": "TV Top Rated",
            }, 

            {
                "menu_type": "tvshow", 
                "iconImage": "genres.png", 
                "mode": "navigator.genres", 
                "name": "Genres", 
                "foldername": "TV Genres",
            }, 

            {
                "menu_type": "tvshow", 
                "iconImage": "networks.png", 
                "mode": "navigator.networks", 
                "name": "Networks", 
                "foldername": "TV Networks",
            }, 

            {
                "action": "tmdb_tv_airing_today", 
                "iconImage": "airing-today.png", 
                "mode": "build_tvshow_list", 
                "name": "Airing Today",
            }, 

            {
                "action": "tmdb_tv_on_the_air", 
                "iconImage": "airing-today.png", 
                "mode": "build_tvshow_list", 
                "name": "On the Air", 
                "foldername": "TV On the Air",
            }, 

            {
                "name": "Up Coming", 
                "iconImage": "userlists.png", 
                "foldername": "Up Coming", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_tv_upcoming",
            }, 

            {
                "action": "trakt_tv_anticipated", 
                "iconImage": "latest-episodes.png", 
                "mode": "build_tvshow_list", 
                "name": "Anticipated",
            }, 

            {
                "menu_type": "tvshow", 
                "iconImage": "trakt.png", 
                "mode": "navigator.trakt_mosts", 
                "name": "Mosts", 
                "foldername": "TV Trakt Mosts",
            }, 

            {
                "menu_type": "tvshow", 
                "iconImage": "languages.png", 
                "mode": "navigator.languages", 
                "name": "Languages", 
                "foldername": "TV Show Languages",
            }, 

            {
                "name": "Years", 
                "menu_type": "tvshow", 
                "iconImage": "years.png", 
                "foldername": "TV Show Years", 
                "mode": "navigator.years", 
            }, 

            {
                "menu_type": "tvshow", 
                "iconImage": "certificates.png", 
                "mode": "navigator.certifications", 
                "name": "Certifications", 
                "foldername": "TV Show Certifications",
            }, 

            {
                "name": "Because You Watched", 
                "iconImage": "library_update.png", 
                "foldername": "Because You Watched", 
                "mode": "navigator.because_you_watched", 
                "menu_type": "tvshow",
            }, 

            {
                "name": "Popular People", 
                "iconImage": "people-boxsets.png", 
                "foldername": "Popular People", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_popular_people",
            }, 

            {
                "action": "favourites_tvshows", 
                "iconImage": "userlists.png", 
                "mode": "build_tvshow_list", 
                "name": "Favourites", 
                "foldername": "TV Show It Favourites",
            }, 

            {
                "action": "subscriptions_tvshows", 
                "iconImage": "library_update.png", 
                "mode": "build_tvshow_list", 
                "name": "Subscriptions", 
                "foldername": "Subscriptions",
            }, 

            {
                "action": "kodi_library_tvshows", 
                "iconImage": "library_update.png", 
                "mode": "build_tvshow_list", 
                "name": "Kodi Library", 
                "foldername": "Kodi Library",
            }, 

            {
                "name": "Kodi Library - Recently Added", 
                "iconImage": "library_update.png", 
                "foldername": "Recently Added to Kodi Library", 
                "mode": "build_kodi_library_recently_added", 
                "db_type": "episodes",
            }, 

            {
                "iconImage": "trakt.png", 
                "action": "TVShowListTrakt",
                "name": "My TV Shows (Trakt)", 
                "foldername": "My TV Shows Trakt",
            }, 

            {
                "name": "Search", 
                "iconImage": "search.png", 
                "foldername": "TV Show Search", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_tv_search", 
                "query": "NA",
            }, 

            {
                "name": "People Search", 
                "iconImage": "people-search.png", 
                "foldername": "People TV Show Search", 
                "mode": "people_search.search", 
                "query": "NA",
            }, 

            {
                "iconImage": "search.png", 
                "mode": "search_history", 
                "action": "tvshow",
                "name": "Search History", 
                "foldername": "TV Show Search History",
            }

        ]


    def TVShowListTrakt(self):
        return [

            {
                "iconImage": "trakt.png", 
                "mode": "build_next_episode", 
                "name": "Trakt Progress", 
                "foldername": "Trakt Progress",
            },

            {
                "action": "trakt_collection", 
                "iconImage": "trakt.png", 
                "mode": "build_tvshow_list", 
                "name": "Trakt Collection", 
                "foldername": "Trakt TV Collection",
            }, 

            {
                "action": "trakt_watchlist", 
                "iconImage": "trakt.png", 
                "mode": "build_tvshow_list", 
                "name": "Trakt Watchlist", 
                "foldername": "Trakt TV Watchlist",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.get_trakt_my_lists", 
                "name": "Trakt My Lists", 
                "foldername": "Trakt My Personal Lists",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.get_trakt_liked_lists", 
                "name": "Trakt Liked Lists", 
                "foldername": "Trakt Liked Lists",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "trakt.search_trakt_lists", 
                "name": "Trakt Search User Lists", 
                "foldername": "Trakt Search Lists",
            }, 

            {
                "name": "Trakt TV Show Calendar", 
                "iconImage": "trakt.png", 
                "foldername": "Trakt TV Show Calendar",  
                "mode": "trakt.get_trakt_my_calendar", 
            }, 

            {
                "name": "Trakt Recommendations", 
                "iconImage": "trakt.png", 
                "foldername": "Trakt Recommendations", 
                "mode": "build_tvshow_list", 
                "action": "trakt_recommendations",
            }, 

            {
                "foldername": "Watched TV Shows", 
                "iconImage": "trakt.png", 
                "mode": "build_tvshow_list",  
                "action": "watched_tvshows", 
                "name": "Watched TV Shows",
            }, 

            {
                "action": "in_progress_tvshows", 
                "iconImage": "trakt.png", 
                "mode": "build_tvshow_list", 
                "name": "In Progress TV Shows", 
                "foldername": "In Progress TV Shows",
            }, 

            {
                "iconImage": "trakt.png", 
                "mode": "build_in_progress_episode", 
                "name": "In Progress Episodes", 
                "foldername": "In Progress Episodes",
            } 


        ]


    def DefaultMenuItems(self):
        return ['RootList', 'MovieList', 'MovieListTrakt', 'TVShowList', 'TVShowListTrakt']

