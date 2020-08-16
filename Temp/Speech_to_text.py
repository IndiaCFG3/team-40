import speech_recognition as sr
import pyttsx3
import json
import pandas as pd
import xlwt
r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

DATA = []
# Collecting voice to Text Element vice
# This code will verify the entry after every Element by Reading the entry
# TO END THE DATA SAY SAVE
while (1):
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            if (MyText == "yes"):
                break
            DATA.append(MyText)

            SpeakText(MyText)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occured")

# Asuming {NAME:,FIELD,PHONE NUMBER ,NEXT}
# Cleaning Data
# Clean the phone number
# DATA=["danish","electrnoics","756",'7598',"752","mayank","chemical","564","35","34567"]
num = [str(x) for x in range(10)]
error = 0
new_data = []

for x in DATA:
    # print(x[0],x[0] in num)`
    if (x[0] in num and error):
        # continues Number
        new_data[-1] = new_data[-1] + x
        error = 1
    elif (x[0] in num and error == 0):
        # start entering number
        new_data.append(x)
        error = 1
    else:
        error = 0
        new_data.append(x)
if((len(new_data))%3==2):
    new_data.append("NULL")
elif((len(new_data))%3==1):
    new_data.append("NULL")
    new_data.append("NULL")
# New_data has data after cleaning
df = pd.DataFrame()
df["Name"] = new_data[0::3]
df["Branch"] = new_data[1::3]
df["Number"] = new_data[2::3]
df.to_excel("Result.xls", index=False)
json.dumps({'DATA': DATA})


