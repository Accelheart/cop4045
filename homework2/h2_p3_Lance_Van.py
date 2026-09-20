import csv
from testif import testif
# a
def add_user(sn: dict, username: str, fullname: str) -> bool:
    """
    This function is to add a user
    """
    try:
        if username not in sn:
            sn[username] = (fullname, [])
            return True
        else: 
            return False
    except:
        print("An error ocurred. ")
        raise

# b
def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """
    This function is to add other users as a friend
    """
    try: 
        if user1 not in sn or user2 not in sn:
            return False
        if user2 in sn[user1][1]:
            return False
        sn[user1][1].append(user2)
        sn[user2][1].append(user1)
        return True
        
    except:
        print("An error occurred while adding the user")
        raise

 # c 
def get_friends(sn: dict, user1: str, distance: int) -> list:
    """
    The get_Friends function finds all friends of the user.
    returns a list of friends found within a given distance
    """
    try:
        if user1 not in sn or distance <= 0:
            return []
        visited = {user1}
        current = [user1]
        friends_found = []
        for _ in range(distance):
            next_level = []
        for user in current:
            for friend in sn[user][1]:
                if friend not in visited:
                    visited.add(friend)
                    friends_found.append(friend)
                    next_level.append(friend)
            current = next_level
        return friends_found
        return [user for user in visited if user != user1]
    except:
        print("An error occurred while getting friends")
        raise

# d
def save_network(filename: str, sn: dict) -> None:
    """
    This function saves the social network dictionary to a CSV file
    """
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for username, info in sn.items():
                writer.writerow([username, info[0]] + info[1])
    except:
        print("An error ocurred while saving the network")
        raise

# e
def load_network(filename: str) -> dict:
    """
    Loads a social network from a CSV file and returns it as a dictionary
    """
    try: 
        network = {}
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                network[row[0]] = (row[1], row[2:])
            return network
    except Exception as e:
        print("An error ocurred while loading the network", e)
        raise

# f
def test_functions() -> None:
    """
    Tests the social network functions
    """
    try:
        sn = {    'alice': ('Alice Smith', ['maria']),
        'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
        'joe': ('Joseph Adams', ['maria', 'eve']),
        'eve': ('Evelyn Cooper', ['joe']),
        'david': ('David Benson', ['maria'])}

        print("add_user:", add_user(sn, "bob", "Bob Jones"))
        print("add_friend:", add_friend(sn, "bob", "alice"))
        print("get_friends:", get_friends(sn, "alice", 2))

        save_network("social_network.csv", sn)
        print("Network saved")

        loaded_sn = load_network("social_network.csv")
        print("Loaded network:", loaded_sn)

    except:
        print("An error occurred while testing the functions")
        raise
# extra credit
def test() -> None:
    """
    Tests the social network functions using testif.
    """
    sn = {
    'alice': ('Alice Smith', ['maria']),
    'maria': ('Maria Cortez', ['alice', 'joe', 'david']),
    'joe': ('Joseph Adams', ['maria', 'eve']),
    'eve': ('Evelyn Cooper', ['joe']),
    'david': ('David Benson', ['maria'])}

    testif(
        add_user(sn, "bob", "Bob Jones") == True,
        "add_user new user")
    testif(
        add_user(sn, "alice", "Alice Smith") == False,
        "add_user existing user")
    testif(
        add_friend(sn, "alice", "joe") == True,
        "add_friend new friendship")
    testif(
        add_friend(sn, "alice", "maria") == False,
        "add_friend existing friendship")
    testif(
        get_friends(sn, "eve", 1) == ["joe"],
        "get_friends distance 1")
    testif(
        get_friends(sn, "unknown", 1) == [],
        "get_friends invalid user")

    save_network("test_network.csv", sn)
    testif(
        True,
        "save_network")
    loaded_sn = load_network("test_network.csv")

    testif(
        loaded_sn == sn,
        "load_network")

if __name__ == "__main__":
    # test_functions()
    test()

