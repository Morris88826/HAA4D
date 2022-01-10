import mysql.connector
import json

class_dict = {
    "abseiling": 3,
}


def getValue(filename):
    
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
        
    
    vals = []
    
    class_id = 1
    for c in data["class_20"]:
        vals.append((class_id, 20, c))
        class_id += 1
    
    for c in data["class_2"]:
        vals.append((class_id, 2, c))
        class_id += 1

    return vals


if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="HAA4D"
    )

    print(mydb)
    mycursor = mydb.cursor()

    sql = "INSERT INTO action_classes (id, num_examples, name) VALUES (%s, %s, %s)"

    class_name = "abseiling"
    video_id = 1

    filename = "../../src/assets/all_classes.json"
    vals = getValue(filename)

    mycursor.executemany(sql, vals)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")
