import mysql.connector
import numpy as np

class_dict = {
    "abseiling": 3,
}

def getValue(filename):
    skeletons_3d = np.load(filename)

    class_id = class_dict[filename.split('/')[-1].split('.')[0][:-4]]
    video_id = int(filename.split('/')[-1].split('.')[0][-3:])
    print(class_id, video_id)

    vals = []
    for frame_id in range(skeletons_3d.shape[0]):
        
        skeleton = skeletons_3d[frame_id]
        val = [class_id, video_id, frame_id]
        for joint_id in range(skeleton.shape[0]):
            x, y, z = list(skeleton[joint_id])
            d = "{:.4f},{:.4f},{:.4f}".format(x, y, z)
            val.append(d)

        vals.append(tuple(val))

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

    joints = ["lower_spine",
              "right_hip",
              "right_knee",
              "right_ankle",
              "left_hip",
              "left_knee",
              "left_ankle",
              "mid_spine",
              "upper_spine",
              "neck",
              "nose",
              "left_shoulder",
              "left_elbow",
              "left_hand",
              "right_shoulder",
              "right_elbow",
              "right_hand"]

    input_name = "class_id, video_id, frame_id, "
    for i, joint in enumerate(joints):
        input_name += joint
        if(i != len(joints)-1):
            input_name += ', '

    input_field = ""
    for i in range(len(joints)+3):
        input_field += "%s"
        if(i != len(joints)+2):
            input_field += ","

    sql = "INSERT INTO skeletons_3d ({}) VALUES ({})".format(
        input_name, input_field)

    class_name = "abseiling"
    video_id = 1

    filename = "../../../dataset/normalized_skeletons_3d/{}/{}_{:03d}.npy".format(
        class_name, class_name, video_id)
    vals = getValue(filename)

    mycursor.executemany(sql, vals)

    mydb.commit()

    print(mycursor.rowcount, "was inserted.")
