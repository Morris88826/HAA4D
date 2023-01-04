import glob
import json

if __name__ == "__main__":
    
    with open('./dataset/info.json', 'rb') as jsonfile:
        info = json.load(jsonfile)
    primary_classes = info["primary_classes"]
    additional_classes = info["additional_classes"]


    print("For Primary Classes:")
    i = 0
    for pc in primary_classes:
        if(len(glob.glob('./dataset/skeletons_3d/{}/*'.format(pc)))!=20):
            print("{} MISSING".format(pc))
        else:
            i += 1
    print("  complete: {}/{}".format(i, len(primary_classes)))

    print("--------------------------")
    print("For Additional Classes:")
    i = 0
    for ac in additional_classes:
        if(len(glob.glob('./dataset/skeletons_3d/{}/*'.format(ac)))<2):
            print("{} MISSING".format(ac))
        else:
            i+=1
    print("  complete: {}/{}".format(i, len(additional_classes)))