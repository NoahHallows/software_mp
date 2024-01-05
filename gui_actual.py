import PySimpleGUI as sg
import os
import cv2
import face_id_picture


radio_keys = ("-R1-", "-R2-")
# Base64 Encoded Radio Button Image of unchecked radio button
radio_unchecked = b'iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAEwElEQVR4nI1W3W9URRT/nZm7ZXdpbajdWpCAjcFEqw88+CACrgaBmFBIwI3fPPpPaJYND/wjYsxFYgwP+BV2kY9gNCIJIhEIBZSWLl3aprvde2fOOT7c3W27fNSTTO7cMzO/35wz55wZYAVRVVMuaxCGoV2qD8PQlsvlQFXNShhPAqduYEr0lrrmhmFoVbVbvWzdQxKGoS0UCgwAFy6PvySx27cQRVvY80YGZyHaIKJbPUHqvCF8k3/tlb+61z2RJAzVFgrE5QuX1q9K9x6Oouj9TCazKmUBawiAglkQO0bsPOqNejOw9qsoan62Z8eWfx9FRMsJkgnnfrv6FgXBUWOD4UzAWJsb8L3ZNFlrCQSwZ8TO6excXe/eux/UY0EcuQkXRx/t3fX6qW6iDomqGiKS87///QaM/Q7K6efXD7rBgf5AVcl7hgBQEYgqVAQEgqroZLXmb9yeTLGgKRztHtu5/XQbr0NSVDU4dAhvj703LGouBpaGXhwZ5v6nem0cO2gCB002AxGBiICZwSwIrEVtZpav3LhjneN76YxsvnDq1D0AKJVKYgBg9NgxKpVKIkpH0ulVQyPrBvxTfb02ih2ICESAdp2darJHIkIUx+jrXW03rB30PT09zzTm5UipVJLR0VECAGqb9csfV16oN3H56f60Hd20gZzzRJR4UzvAusySxBoBi8A5DyLolWvjOv1gjldnUqN7duavFYtFYyoVGACIvd2fzWZSw4P9IqKkLfBugu4GKFSSr4hSbqBfMplMaiFyBwAgn88bU60eUwCI43hbYIBsJk2e+bHAiQVL/xWiSTB4ZmQzabKG4B1vBYBqtapBoVBgVaUfz13aaI3CEBGzgAjouEuXg3bARSG6pImADJEhwLN/TlWJiDhoecOqSHYpUIJPHYclY4CqdBElZ6Otfse9otlKBRaAb5OwqjbaYSnatqKzpEXQAleFsIAlCWERBbfyR4TBwlDVRj4PBgAThqElIgVhPPaicew02R0vi6ClESWcALEkkbV0bhQ7dZ4VpONEpGEYWpPL5QgArLVnYsc0N99QAuC5nWy8JPEYvtW4PS6LfVXFfL2hznkyxv4MALlcjkwlnxcACCj4ul6fjyeqNeOZ1Xu/COoXwX0XkbDAs8B7BjPrVLVm6vVGDOXjAFCpVMSUiCQMQ/vmlpevE+nRyJOZul9jYwix84sEfrG1d94h9A5EQHW6xrEXYwhffFLYe/3dMLSlUkmS2lUsGgB4Nf/OEIleJEPDI88Ocl/vauu8b5UQdA69nS/t2mWIMDM3x+P/TFp2flKM3Tz+569T7dr1UBU+8dPZbWRS30M4s25ojVvT3xcIlNpRpCpd+cI6XZvxd6emUyrUEPW7DhbGzi6twp37mVpu27Nj65lmo7lbgDsT9+dSV2/cotqDWR/HMYt4ERHx7CWKIq7NzPrrN2/TVG0uBcVt56PdBwtjZ1sRKx3sruLaubiOnzy51tq+wy6KP0j19GSsAQwtlnrPjNgxmgvNBWvNl41m8/NPP94/seLN2E0EACd+qGxyse5runi7Zz+iLL2imLcGN1PWnhYNvv3wwM5r3ev+lzzqtdLSB926lV4rK0qxWDTlcvmx7652ZD5J/gNoDCDS80MCGwAAAABJRU5ErkJggg=='

# Base64 Encoded Radio Button Image of checked radio button
radio_checked = b'iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAF40lEQVR4nI2Wf2yWVxXHv+fe+7y/3xbYWvpzhbGRCOkMLoRsjr21A2dI2BalTeaYxsyQ6GT+YTQuQRsy4zRGtmg2gzGNf+jinoK6sY2ZbNK3JQuSuWmiWx3ggBQKfTta+v58nueee/zjfQusMPD88yT3ued87sk593sPcCMTUblDYgZ80R9b90XnDomBiLphjOsEp8WBNQEiohUt2uuLhsji1Ut2zR8Dvq9HBgcZAPqPzK+ZD81DxWpwt2XucYIURCqa6FQmHnuryeBPY31N79dhvkbD77qQAV/0yCBx7tBMV0knn5oPooczyVR8Rcyi0zAS5FBhYDLQ+DDUKJWrtaxRf0hF87uObL3lzIL/J0IWNmx8c7Z/zsR/b7Rp25qex7aOuL09ayhhiECAs4xSyPLBxVD2T4bmQLkZURRNZaLi9nce7P4rfNG4AnQZIqJA5O4Zu5Cbk+TrHVRL/Hi1ie5cnjBgosAyWAAnAnEOEIcYCbRjOXy+an94XHlTHK8tcZUvvP1AR34h3mXIUL1DNm2eaTsXxN5t96R1uNdw15KkrgQMAqAgEAAiAuccnHOI2MFah4wWHJ+t8OMTWp8L9fn2uKwbP9JyHgCwm5wCgIG1IOwmdyH0no4lkq0/uQ22qzmhyzWGIUARINfqEBF4GrBaY83NKb2rJ7Amnlg+U+GnsZvcwNoRqmfSSOu+sYurT1Xdv7a3Oj10R5bKoZAhwAlAtBBTLmViLcMoQhBZfH84j7vXduLhDT3yvX+U5Y8fJXlVMlo7trX7GIZEqdwoFADMMn0pm057X2w3zjkQpH76mFFwTi4BRASWHYxWYCfY+dwb+M3L7+Bn/lHMViN6YDlcOpnwpgO1DQByfVAqXxgRACgHduMKz2JVxlBgHTxNIABnZopIJQwsuwaAYTTBOYcdzx7Ei2MT6O5Yih999bOA1rglAer2IpQZ9wBAvjAiCoODLCJkWXo6TIS4EoqsAwB899dv4q4nfouxf55GNh1HLYhgVD2zHc++jn2HP0D7sjR++c1+3PfpbhSrIZIa1KZCWJYVIkIYHOQF3dFOJJWAA4mAnQOzxdRHRZwtFPGVn76MN94+gZuWphBGFjueOYiR8f+gY1kGzz++CZ+7owuFi5X6nRBBHAxxkhodhQYA04AwQSoVJkTMcE7BMjD8nS0gIuwbn8BjP38Nz+3cjJH8BF7MT6Dz5gye37kJud5OFObKUASwc4gco+o8CFDp6wPXIb6viYhXv3rh5GSkP1UKQ1EaCEJG3NPY++374UTw0lvH8PU9B1GuRWi/KYNffWsz+no7MT1XgSLUa+YcSiHLmcgTD+FJIhL4vla5lgECgFQM4ycDQ8fmI/EgcCKoBhEIgr1PfB4P3nUbpueqaE7HsbeRwfRcGYoEzK7eEMI4XmSZjGKU8PQYAORaBsjkR+EAoNmofadL5d37zrLpbYoktEQeESq1EDFP4xff6Ec26WHL+pVXANAAOITWIUaRvFrQqlyphh0x3g8A+VE4ulIYe18pDLtE+mt72gt2Q0vCzIYCTwHOCYgIqbhBEFlUamG9kA15qVlGRjkcLQR21/kuo2rl4ROPdD+GAV9jZJA/pl259dOtU2LebTW27Zlbq7yyKabnQqnfTAiY619qACzX9SujGP+9GPCTp5bogjXnsiZc996/V0wvaNdVKvyZA2c2zqv0X1pRSz7ZVYnWL9UmFKKABdbVayUigGMYOChn5egM2z3nmr2CJCtZW73/vUd6Dl+twgvWeAfW/fn0vSXd9DttdHe/nsaWFmdXJkEJJUQQROxQDllOlEVeK2gzatvAbE+ng+L29x9dNf7J70nDFupz5/6T7dVY9qli6L6ciMWSXSZAOwWIE6PKhLM2jknroVwNqxmPXlgSXPjB3x9dM7UYcE1IPaPLb/WGA9O3zzM9VAr5XhvZlQ6SIaGSUfRh0jP5ZRS+9Ldt3ccW+/1/JkJYNK0oAg6JmKtmIN+/7rRyYxuqz12LgfD9+tw1dOO563+8H1VJkK2keQAAAABJRU5ErkJggg=='


#Section for selecting the image containing face to search for
select_target_face = [
    [
        sg.Text("Select the image containing the face to search for (ensure only one face is in the image)"),
        sg.In(size=(25, 1), enable_events=True, key="-TARGET_FACE_LOCATION-"),
        sg.FileBrowse(),
    ],
    [
        sg.Image(key="-TARGET_FACE_DISPLAY-"),
    ]
]

#Section for selecting the directory to search
select_image_dir = [
    [
        sg.Text("Select the directory containing the images to search and edit"),
        sg.In(size=(25, 1), enable_events=True, key="-IMAGE_DIRECTORY-"),
        sg.FolderBrowse(),
    ],
]

#List images in selected dir
image_list = [
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-LIST_IMAGES-"
        )
    ],
]

#select overlay
overlay_select = [
    [
        sg.Text("Slect image to replace matching faces with"),
        sg.In(size=(25, 1), enable_events=True, disabled=True, key='OVERLAY_LOCATION'),
        sg.FileBrowse(key="OVERLAY_BROWSER", disabled=True)
    ]
]

#View images in selected dir
selected_img_viewer = [
    [sg.Text(size=(70, 1), key="-TOUT-")],
    [sg.Image(key="-SELECTED_IMAGE-")],
]

# Section for options
options = [
    [sg.Text("If an image is found to contain the searched for face should the program:")],
    [sg.Image(radio_checked, enable_events=True, key='-R1-', metadata=True), sg.Text('blur face', enable_events=True, key='-TTT1-')],
    [sg.Image(radio_unchecked, enable_events=True, key='-R2-', metadata=False), sg.Text('replace face', enable_events=True, key='-TTT2-')],
]


# Layout
layout = [
    select_target_face,
    select_image_dir,
    [
        sg.Column(image_list),
        sg.VSeparator(),
        sg.Column(selected_img_viewer)
    ],
    options,
    overlay_select,
    [sg.Button('Start', size=(5, 2), button_color=('white', 'springgreen4'), key='SUBMIT')],
]

window = sg.Window("Face removal tool", layout)

def check_radio(key):
    for k in radio_keys:
        window[k].update(radio_unchecked)
        window[k].metadata = False
    window[key].update(radio_checked)
    window[key].metadata = True

#Declare action and overlay_location variable so if the radio button isn't clicked it still has a value
action = 1
overlay_location = ''

#list what elements to disable
key_list = 'OVERLAY_LOCATION', 'OVERLAY_BROWSER'

while True:
    event, values = window.Read()
    #Exit
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    #Get target face image location
    if event == "-TARGET_FACE_LOCATION-":
        target_face_location = values["-TARGET_FACE_LOCATION-"]
        image = cv2.imread(target_face_location)
        # Get the dimensions of the image (height, width, number_of_channels)
        height, width, channels = image.shape
        scale_factor = (100/height)
        new_width = int(round(scale_factor*width, 0))
        resized_image = cv2.resize(image, (new_width, 100), interpolation=cv2.INTER_AREA)
        imgbytes = cv2.imencode(".png", resized_image)[1].tobytes()
        window["-TARGET_FACE_DISPLAY-"].update(data=imgbytes, size=(100, new_width))

    #Get location of images to search
    if event == "-IMAGE_DIRECTORY-":
        folder = values["-IMAGE_DIRECTORY-"]

        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", '.jpg'))
        ]

        window["-LIST_IMAGES-"].update(fnames)

    #Display image if clicked on from list
    elif event == "-LIST_IMAGES-":  # A file was chosen from the listbox

        try:
            filename = os.path.join(

                values["-IMAGE_DIRECTORY-"], values["-LIST_IMAGES-"][0]

            )
            image = cv2.imread(filename)
            # Get the dimensions of the image (height, width, number_of_channels)
            height, width, channels = image.shape
            scale_factor = 200/height
            new_width = int(round(scale_factor*width, 0))
            resized_image = cv2.resize(image, (new_width, 200), interpolation=cv2.INTER_AREA)
            imgbytes = cv2.imencode(".png", resized_image)[1].tobytes()
            window["-SELECTED_IMAGE-"].update(data=imgbytes, size=(new_width, 200))
            window["-TOUT-"].update(filename)
        except:
            pass

    #Get what to do to matching faces
    if event in radio_keys:
        check_radio(event)
    elif event.startswith('-TTT'):        # If text element clicked, change it into a radio button key
        check_radio(event.replace('TTT', 'R'))
    if event == "-R1-":
        action = 1
        for key in key_list:
            window[key].update(disabled=True)
    if event == "-R2-":
        action = 2
        for key in key_list:
            window[key].update(disabled=False)
    
    #Logic for overlay selection
    if event == "OVERLAY_LOCATION":
        overlay_location = values["OVERLAY_LOCATION"]
    
    #Logic for start button
    if event == "SUBMIT":
        print(f"action = {action}")
        print(f"target face location = {target_face_location}")
        print(f"Images to search directory = {folder}")
        results = face_id_picture.__init__(folder, target_face_location, action, overlay_location)
        print(results)


window.Close()