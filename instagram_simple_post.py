# Programme qui communique avec l'api d'Instagram / CARROUSSEL
import config
import json
import requests
from filestack import Client # Comment this line if you don't want filestack upload
import sys
import time

def publish_image(listImg, desc, upload):
    #######################################################################################
    #Post the media(s) on instagram with description.

    #Parameters:
    #    listImg (str): The media(s) to upload, separated with ',' if many. Local path
    #    Example : "img1.jpg" OR "img1.jpg,video.mp4,img2.png"

    #    desc (str): The description of the instagram post
    
    #######################################################################################    

    if upload: client = Client(config.filestack_api_key) #Connect to filestack
        
    # Graph api access_token
    access_token = config.ig_access_token
    ig_user_id = config.ig_user_id

    #Url to create container
    post_url = "https://graph.facebook.com/v15.0/{}/media".format(ig_user_id) 

    #Lists init
    listUrl = []
    listIdElement = []
    listFic = listImg.split(",") #Make a list of the file(s) name(s)

    #Upload each file on filestack
    if upload:
        for fic in listFic:
            imageUrl = client.upload(filepath=fic)
            listUrl.append(imageUrl.url + ";" + imageUrl.metadata()["mimetype"].split("/")[0])
        print("liste url : " + str(listUrl))
    else : listUrl = listFic

    # ONE PHOTO POST
    if len(listUrl) == 1:
        video = False
        payload = {
            "image_url": imageUrl.url,
            'caption': desc,
            'access_token': access_token
        }
        #Differents parameters for video post
        if imageUrl.metadata()["mimetype"].split("/")[0] == "video":
            video = True
            payload["media_type"] = "VIDEO"
            payload["video_url"] = payload.pop("image_url")

        #Post container
        r = requests.post(post_url, data=payload)
        print(r.text)
        print("Media uploaded successfully")
        results = json.loads(r.text)
        
        #Validate container
        if "id" in results:
            creation_id = results["id"]

            #Wait for video container instagram confirmation
            if video: waitValidationConteneur(creation_id, access_token)

            second_url = "https://graph.facebook.com/v15.0/{}/media_publish".format(ig_user_id)
            second_payload = {
                'creation_id': creation_id,
                'access_token': access_token,
            }
            r = requests.post(second_url, data=second_payload)
            print(r.text)
            print("media success publish")
        else:
            print("pas publié mdr")

    #CAROUSEL ALBUM POST
    else:
        #Create an element container for each url
        video = False
        auMoinsUneVideo = False
        for url in listUrl:
            payload = {
                "is_carousel_item": True,
                "image_url": url.split(";")[0],
                'access_token': access_token
            }
            #Differents parameters for video post
            if url.split(";")[1] == "video":
                video = True
                auMoinsUneVideo = True
                payload["media_type"] = "VIDEO"
                payload["video_url"] = payload.pop("image_url")
            #Post containers
            r = requests.post(post_url, data=payload)
            print(r.text)
            results = json.loads(r.text)
            if "id" in results: listIdElement.append(results["id"])
            if video: creation_id = results["id"]
            video = False
        print("liste id element : " + str(listIdElement))

        #Waiting for instagram container validation
        if auMoinsUneVideo: waitValidationConteneur(creation_id, access_token) 

        #Create container for carousel_album
        children = ",".join(listIdElement)
        payload = {
                "media_type": "CAROUSEL",
                "caption": desc,
                "children": children,
                'access_token': access_token
        }   
        r = requests.post(post_url, data=payload)
        print(r.text)
        print("Conteneur carousel OK")
        results = json.loads(r.text)
        print(r.text)
        if "id" in results: creation_id = results["id"]

        #Post carousel container
        second_url = "https://graph.facebook.com/v15.0/{}/media_publish".format(ig_user_id)
        second_payload = {
            'creation_id': creation_id,
            'access_token': access_token,
        }

        #Waiting for the validation of carousel container
        waitValidationConteneur(creation_id, access_token)

        r = requests.post(second_url, data=second_payload)
        print(r.text)
        print("CAROUSEL success publish")
            
def waitValidationConteneur(id, token):
    #######################################################################################
    #Wait until the container is validate by instagram.

    #Parameters:
    #    id (int): Id of the container

    #    token (str): Instagram access token
    
    #######################################################################################   
    url = "https://graph.facebook.com/{}/".format(id)
    container_ready = False
    while not container_ready:
        time.sleep(3)
        # Check status
        params = {"fields": "status_code",
                "access_token": token}
        r = requests.get(url, params=params)
        print(r.text)
        results = json.loads(r.text)
        if results['status_code'] == "FINISHED":
            container_ready = True

# Uncomment this line if you want to call the function from a .js file
#publish_image(sys.argv[1], sys.argv[2])
