import csv
def display_top_collaborations(rated_filename: str, casts_filename: str) -> None:
    """
    Displays director and actor collaborations 
    """
    top_rated = set()
    with open(rated_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            title = row[1]
            year = row[2]
            top_rated.add((title, year))

    collaborations = {}
    with open(casts_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            title = row[0]
            year = row[1]
            director = row[2]
            actors = row[3:]
            if(title, year) in top_rated:
                for actor in actors:
                    pair = (director, actor)
                    if pair in collaborations:
                        collaborations[pair] += 1
                    else:
                        collaborations[pair] = 1
        sorted_collaborations = sorted(
            collaborations.items(),
            key=lambda x: x[1],
            reverse = True
        )                
        for pair, count in sorted_collaborations:
            print((pair[0], pair[1]. count))
            
