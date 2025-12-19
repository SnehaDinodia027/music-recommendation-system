def get_music_links(mood):
    mood = mood.lower()

    music = {
        "happy": {
            "youtube": "https://www.youtube.com/watch?v=pIgZ7gMze7A&list=PLJNlve0_Ebae2aPbjfolLT-6LvZkP8UZA",
            "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWTwbZHrJRIgD"
        },
        "sad": {
            "youtube": "https://www.youtube.com/watch?v=Jkj36B1YuDU&list=PLZzyUfYacyoIbzbSKIzs4xCC5AsvO0-5X",
            "spotify": "https://open.spotify.com/search/sad%20music%20playlist"
        },
        "calm": {
            "youtube": "https://www.youtube.com/watch?v=tHsmufMcCqY&list=PLQ_PIlf6OzqIEvjMOCAZsD21T6xn9QUP6",
            "spotify": "https://open.spotify.com/search/calm%20music%20playlist"
        }
    }

    return music.get(mood, music["happy"])
