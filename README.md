# SmarterRingV2
Ring but cooler V2.0

This is an expiremental hack using an unnoficial ring api. When someone is at the door, and this program is running, You will be notified who it is.
For you to use this with your own ring, follow the following simple steps

Create Environment variables USERNAME and PASSWORD, and set them to your ring account password

run (Multiple times):
**$python submit_face.py NAME**
Where NAME is the name of the person whos images you would like to enter.
Stand outside with lighting similar to that of your ring's view.
Record 3-5 images per person 
Account for different lighting conditions and different times of day
Press the space bar once run to submit a face 

Then run:
**$python main.py**
This will start the program. First, it will ask you for a 2FA code. Make sure you have two-factor authentication enabled for your ring account. 
If you have it set up, you will see an email with the code you must enter into cmd.
It will instantly download and predict on the last time the doorbell was rung, then, it will wait until the doorbell is ring
once more, and predict on that.

This is very expiremental, using Google's Facenet model for clustering, such that the prediction in real time procces is very fast. 
Fine tuning is in development and will be implemented shortly

