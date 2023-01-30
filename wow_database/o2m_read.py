from o2m_modul import Game, Race, Class, Profession, engine
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)()

def choice_menu():
    print("~*~*~{ WOW Game Database }~*~*~")
    print("Please make tour choice: ")
    print("|1| Add new player")
    print("|2| List/search player list")
    print("|3| List all races")
    print("|4| List all classes")
    print("|5| List all professions")
    print("|6| Update player list")
    print("|7| Delete player from the list")
    print("|0| Exit")
    choice = input("Make your choice: ")
    return choice

def add_new_player():
    add_username = input("Username: ")
    add_level = input("Level: ")
    new_player = Game(username=add_username, level=add_level)

    list_all_races()
    race = session.query(Race).filter_by(id=int(input("Enter race ID: "))).one()
    race.games.append(new_player)
    list_all_classes()
    class_ = session.query(Class).filter_by(id=int(input("Enter class ID: "))).one()
    class_.games.append(new_player)
    list_all_professions()
    profession = session.query(Profession).filter_by(id=int(input("Enter profession ID: "))).one()
    profession.games.append(new_player)
    session.add(new_player)
    session.commit()
    print("~*~*~| New player added successfully! |~*~*~")

def player_list(query=session.query(Game)):
    if query and len(query.all()) > 0:
        for new_player in query.all():
            print(new_player)
    else:
        print("~*~*~| No player was found |~*~*~")

def search_player(query=session.query(Game)):
    search = input("Search for a new player or nothing to continue: ")
    if not search:
        return
    try:
        query_level = int(search)
    except ValueError:
        query = query.filter(Game.username.ilike(f"%{search}%"))
    else:
        query = query.filter(Game.level >= query_level)
    finally:
        player_list(query)
        if len(query.all()) > 0:
            search_player(query)
        else:
            search_player()

def list_all_races():
    races = session.query(Race).all()
    for race  in races:
        print(race.id, race.name, race.available, race.faction)

def list_all_classes():
    classes = session.query(Class).all()
    for class_ in classes:
        print(class_.id, class_.name, class_.party_role, class_.resources, class_.armor_type, class_.weapon)

def list_all_professions():
    professions = session.query(Profession).all()
    for profession in professions:
        print(profession.id, profession.name)

def get_player_by_id():
    player_list()
    try:
        id = int(input("Enter player ID: "))
    except ValueError:
        print("Error: ID must be a number, please try again")
    else:
        return session.query(Game).filter_by(id=id).one()

def update_player_list(player, **changes):
    for column, value in changes.items():
        if value:
            setattr(player, column, value)
    session.commit()
    print(player)

def collect_data_changes(player):
    print(player)
    print("Enter new player data or nothing to skip")
    changes = {
        "username": input("Username: "),
        "level": input("Level: "), 
    } 
    list_all_races()
    race_id = input("Race id: ")
    if race_id:
        changes["race_id"] = int(race_id)
    list_all_classes()
    class_id = input("Class id: ")
    if class_id:
        changes["class_id"] = int(class_id)
    list_all_professions()
    profession_id = input("Profession id: ")
    if profession_id:
        changes["profession_id"] = int(profession_id)
    return changes

def delete_player(player):
    print(f"Player has been successfully deleted from the list with ID {player.id}!")
    session.delete(player)
    session.commit()

while True:
    choice = choice_menu()
    if choice == "0" or choice == "":
        break
    elif choice == "1":
        add_new_player()
    elif choice == "2":
        player_list()
        search_player()
    elif choice == "3":
        list_all_races()
    elif choice == "4":
        list_all_classes()
    elif choice == "5":
        list_all_professions()
    elif choice == "6":
        player = get_player_by_id()
        update_player_list(player, **collect_data_changes(player))
    elif choice == "7":
        delete_player(get_player_by_id())
    else:
        print(f"Error: wrong choice {choice}!")