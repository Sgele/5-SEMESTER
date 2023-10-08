from pymongo import MongoClient, ASCENDING
import Artist
import Albums
from bson.code import Code

client = MongoClient("mongodb://localhost:27017")
db = client.spotify

artists = db.artist
albums = db.album

def dropCollections():
    for collection in db.list_collection_names():
        db[collection].drop()

def insertDataToMongo():
    artists.insert_many(Artist.artists)
    albums.insert_many(Albums.albums)

def displayAllCollections():
    print("Displaying inserted collections:")
    print(db.list_collection_names())
    print("")


def displayEverythingAboutAlbums():
    print("\nDisplaying everything about the albums (sorted by album's title):")
    for i in albums.find().sort("Album's_Title", ASCENDING):
        print(i)
    print("\n")


def aggregation():
    pipeline = [
        {"$unwind": "$Tracks"},
        {"$group": {"_id": "$Album_Title",
                    "Album_duration": {"$sum": "$Tracks.Duration"}}}
    ]
    result = albums.aggregate(pipeline)
    print("Total album durations in seconds using aggregate:")
    print(list(result))
    print("")

def mapReduce():
    map = Code("""
                function(){
                    for(i in this.Tracks) {
                        emit(this.Album_Title, this.Tracks[i].Duration);
                    }
                }
                """)
    reduce = Code("""
                    function(keyTitle, valTotalDuration){
                        return Array.sum(valTotalDuration);
                    }
                    """)
    map_red = albums.map_reduce(map, reduce, "albumDuration")
    result = []
    for i in map_red.find():
        result.append(i)
    print("Total album durations in seconds using map-reduce:")
    print(result)

def main():
    dropCollections()
    insertDataToMongo()
    displayAllCollections()
    displayEverythingAboutAlbums()
    aggregation()
    mapReduce()

if __name__ == "__main__":
    main()