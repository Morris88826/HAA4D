import mysql.connector
import json
import glob


def getValue(filename):

    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)

    action_classes = sorted([f.split(
        '/')[-1] for f in glob.glob("../../../dataset/normalized_skeletons_3d/*")])

    action_dict = {}
    class_id = 1
    for c in data["class_20"]:
        action_dict[c] = class_id
        class_id += 1
    for c in data["class_2"]:
        action_dict[c] = class_id
        class_id += 1
    vals = []

    for i, action_class in enumerate(action_classes):
        vals.append((action_dict[action_class], action_class))

        if i == 49:
            break
    # class_id = 1
    # for c in data["class_20"]:
    #     if c in action_classes:
    #         vals.append((action_dict[c], c))

    # for c in data["class_2"]:
    #     if c in action_classes:
    #         vals.append((action_dict[c], c))

    return vals


if __name__ == "__main__":
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="root",
    #     database="HAA4D"
    # )

    mydb = mysql.connector.connect(
        host="us-cdbr-east-05.cleardb.net",
        user="be1d55c228f455",
        passwd="892a86aa",
        database="heroku_4d2256cc291b81a"
    )

    print(mydb)
    mycursor = mydb.cursor()

    sql = "INSERT INTO action_classes (id, name) VALUES (%s, %s)"

    filename = "../../src/assets/all_classes.json"
    vals = getValue(filename)\

    mycursor.executemany(sql, vals)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")
