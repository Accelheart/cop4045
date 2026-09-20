import csv
# a
def display_top_collaborations(
    rated_filename: str,
    casts_filename: str,
    limit: int = None
) -> None:
    """
    Displays director and actor collaboration
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
        if limit is not None:
            sorted_collaborations = sorted_collaborations[:limit]
        for pair, count in sorted_collaborations:
            print((pair[0], pair[1], count))

# b 
def display_top_actors(
    grossing_filename: str,
    cast_filename: str,
    limit: int = None
) -> None:
    """
    Shows actors from top grossing movies ranked by the total box office money
    """
    grossing = {}
    with open(grossing_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            title = row[1]
            year = row[2]
            money = int(row[3])
            grossing[(title, year)] = money

    actor_totals = {}
    with open(cast_filename, "r", encoding ="utf-8") as file:
        reader=csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            title = row[0]
            year = row[1]
            actors = row[3:]

            if (title, year) in grossing:
                money = grossing[(title, year)]

                for actor in actors:
                    if actor in actor_totals:
                        actor_totals[actor] += money
                    else:
                        actor_totals[actor] = money
        sorted_actors = sorted(
        actor_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )

    if limit is not None:
        sorted_actors = sorted_actors[:limit]

    for actor, money in sorted_actors:
        print((actor, money))

# c
def main() -> None:
    """
    Tests the functions 
    """
    print("Top Collaborations:")
    display_top_collaborations(
        "imdb-top-rated.csv",
        "imdb-top-casts.csv",
        10
    )

    print("\nTop Actors:")
    display_top_actors(
        "imdb-top-grossing.csv",
        "imdb-top-casts.csv",
        10
    )
if __name__ == "__main__":
    main()