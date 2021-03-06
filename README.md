# SmarterRingV2

![Project Image](MEDIA/Cover.png)

> This is an aplied deep learning project that will literally tell you who is at your door, once the doorbell is rung.

---

### Table of Contents
Medium Blog: https://dude123studios.medium.com/face-recognition-at-your-doorbell-1e6f250f2ee9

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [Author Info](#author-info)

---

## Description

_Face Recognition_ is **huge**. With the ability to automatically classify someone, many useful prducts have been created. For example, to unlock the new _IPhones_ all you need is to display your face. This single handedly shows how strong our technology has come. Millions rely on a deep clustering model to protect all of their private information and other smart phone data. With the new _Amazon Ring_, I was disapointed that it didn't have this common feature. So I decided to create it myself! Read my medium blog on the subject. This repository can be used on your own _Amazon Ring_ in just a couple of steps!
![Diagram](MEDIA/Diagram.png)

---

#### Technologies

- Deep Learning
- Ring API
- Computer Vision 
- Face Recognition  

If you are interested in _FaceNet_ the model used in this repository, the following diagram illustrates it:
![Architecture](MEDIA/Architecture.png)

[Back To The Top](#SmarterRingV2)

---

#### Installation

```venv
  $git clone https://github.com/dude123studios/SmarterRingV2
  $pip install requirements.txt
```
##### How To Use

**Prerequisites** 
Set environment variables, _USERNAME_ and _PASSWORD_, and equate them to your _Amazon Ring_ acount's username and password

**Gather Data**
In order to submit the faces of your family members, or those who you would like to have regonized, you have two options. 
(name = name of person to enter)
- run:
```venv
  $python submit_face.py name False
```
- or:
```venv
  $python submit_face.py name True
```
In the first case, a popup will show on your screen using your webcam. Hit the space bar when ready to record an image of "name". Do so multiple times from different angles. Once done, hit the escape button to close the program. 
In the second case, data will be grabbed directly from your ring doorbell."name" is the name of the person who was at your doorbell last when it was rung. This method will reach higher accuracy.  

**Encode Data**  
Once all the images are in, run:
```venv
  $python create_encodings.py
```
This will simply encode your data.  
**Run**  
Finally, to run the program, run main.py. Leave it running. Once anyone rings your doorbell, you will have a loud Text-To-Speech played automatically on your device informing you who it is. 
```venv
  $python main.py
```
  
**Test**(Optional)  
run: 
```venv
  $python test.py
```  
A window will pop up showing your webcam detecting your face. Use incase you run into any issues or want to test the capabilities of the program  

[Back To The Top](#SmarterRingV2)

--- 

## References

- https://github.com/tchellomello/python-ring-doorbell
- https://arxiv.org/abs/1503.03832
- https://gtts.readthedocs.io/en/latest/module.html
- https://pypi.org/project/playsound/
- https://pypi.org/project/mtcnn/  
[Back To The Top](#SmarterRingV2)
--- 

## Author Info

- Name: Atharv N.
- Location: California USA
- Age: 13
- Hobbies: Math, Programming, Minecraft 
- Email: dude123studios@gmail.com 

  
[Back To The Top](#SmarterRingV2)



