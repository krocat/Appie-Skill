# Alexa Appie Skill

Manage your Albert Heijn "Appie" shopping list with Alexa through the use of an unofficial API

### THIS SKILL IS FOR PERSONAL USE ONLY AND IS NOT ENDORSED BY ALBERT HEIJN OR AMAZON - DO NOT SUBMIT THIS TO AMAZON FOR CERTIFICATION AS IT WON'T PASS!

This skill is based on the mijahlib library made by Costas Tyfoxylos

https://github.com/costastf/mijnahlib

You will need to set-up a developer account and an AWS account with Amazon. Instructions are below. When the installation is complete, you will be manage what's on your Appie list through Alexa by asking for example:

"Alexa ask Appie to add milk to my list"


#Installation Instructions.

## Setup

This step-by-step instruction is based on this instruction by tartanguru:

https://github.com/tartanguru/alexa-google-search/blob/master/README.md

To run the skill you need to do three things:-

1. download the files from github
2. deploy the example code in lambda
2. configure the Alexa skill to use Lambda.

### Download code from github

1. Click on the green "Clone or download" button
2. Click download ZIP
3. Unzip the file to a known place on your hard-drive


### AWS Lambda Setup

1. Go to http://aws.amazon.com/lambda/ . You will need to set-up an AWS account (the basic one will do fine) if you don't have one already ** Make sure you use the same Amazon account that your Echo device is registered to** Note - you will need a credit or debit card to set up an AWS account - there is no way around this. If you are just using this skill then you are highly unlikely to be charged unless you are making at least a million requests a month!
2. Go to the AWS Console and click on the Lambda link. Go to the drop down "Location" menu and ensure you select US-East(N. Virginia) if you are based in the US or EU(Ireland) if you are based in the UK or Germany. This is important as only these two regions support Alexa. NOTE: the choice of either US or EU is important as it will affect the results that you get. The EU node will provide answers in metric and will be much more UK focused, whilst the US node will be imperial and more US focused.
3. Click on the Create a Lambda Function or Get Started Now button.
4. Skip the Select Blueprint Tab and just click on the "Configure Triggers" Option on the left hand side
5. On the Cofigure Triggers tab Click the dotted box and select "Alexa Skills Kit". Click Next  
6. Name the Lambda Function "Appie".
7. Select the Python 2.7 as the runtime.
9. Select Code entry type as "Upload a .ZIP file". Go to the folder where you unzipped the files you downloaded from Github. Open the src folder, Select Appie.zip and click open.  **Do not upload the zip file you downloaded from github - only the Appie.zip contained within it**
10. Make sure lambda_function.lambda_handler is set in the Handler field (this refers to the main py file in the zip).
11. Create a basic execution role by slecting "Create new role from template(s)" in the Role box, then name the role "lambda_basic_execution” in the role name box and click create.
12. Under Advanced settings change the Timeout to 10 seconds
13. Click "Next" and review the settings then click "Create Function". This will upload the Appie.zip file to Lambda. **This may take a number of minutes depending on your connection speed**
14. Copy the ARN from the top right to be used later in the Alexa Skill Setup (it's the text after ARN - it won't be in bold and will look a bit like this arn:aws:lambda:eu-west-1:XXXXXXX:function:Appie). Hint - Paste it into notepad or similar

### Alexa Skill Setup

1. Go to the Alexa Console (https://developer.amazon.com/edw/home.html and select Alexa on the top menu)
2. Click "Get Started" under Alexa Skills Kit
3. Click the "Add a New Skill" yellow box.
4. You will now be on the "Skill Information" page. 
5. Set "Custom Interaction Model" as the Skill type
6. Select the language as English (US).
7. Set "Appie" as the skill name and "Appie" as the invocation name, this is what is used to activate your skill. For example you would say: "Alexa, Ask Appie what's on my list."
8. Leave the "Audio Player" setting to "No"
9. Click Next.
10. You will now be on the "Inovation Model" page. 
11. Click "Launch Skill Builder (BETA)".
12. Go to "Code Editor"
13. On the top it says "Drag and drop your .json file", browse to the intent folder in the zip file you downloaded from Github and drag the intent.json file onto this box in your browser. In the editor you see some lines of code added to what you had already.
14. Click "Save Model", wait until it saves and then click "Build Model".
15. When the model has been built, go to "Configuration" on the top-right bar.
17. You will now be on the "Configuration" page.
18. Select "AWS Lambda ARN (Amazon Resource Name)" for the skill Endpoint Type.
19. Then pick the most appropriate geographical region (either US or EU as appropriate) and paste the ARN you copied in step 13 from the AWS Lambda setup. 
20. Select no for Account Linking
21. Click Next.
22. Create a new folder somewhere on your harddrive and extract the contents of the zip file you uploaded in step 9 of the AWS Lambda Setup into it.
22. Now, go back to the skill Information tab and copy the appId. Open the settings.py file in the directory you just created and paste the appId into the settings.py file for the variable ApplicationID (IMPORTANT make sure it is in quotes).
23. In the settings.py file also change the values for username and password to match the username and password that you use to log-in on the AH.nl webpage. Save the settings.py file.
24. Create a new zip file to upload. Open the folder you created in step 22 and select all the files and folders in that folder. Create a new zip file called Appie.zip with these files. **Make sure the zip file is not just the src directory itself**, otherwise Lambda function will not work.

The contents of the zip file should be as follows:

    ```
    
        beautifulsoup4-4.6.0.dist-info ( the folder and its contents )
        bs4 ( the folder and its contents )
        bs4-0.0.1-py2.7.egg-info ( the folder and its contents )
        mijnahlib ( the folder and its contents )
        mijnahlib.egg-info ( the folder and its contents )
        requests ( the folder and its contents )
        requests-2.13.0.dist-info ( the folder and its contents )
        settings.py
        lambda_function.py
    
    ``` 
Then update the lambda source zip file with this change and upload to lambda again, this step makes sure the lambda function only serves request from authorized source.

25. Go back to the Skill Setup page and select the "Test" step. Here you can test if your new Appie skill is working by using the Ask Appie button.

**NOTE: if you get a lambda response saying : "The remote endpoint could not be called, or the response it returned was invalid." It is likely that you have zipped the src folder and not it's contents**

### Fault Finding  


1. It works in the simulator but not on my device.
Make sure that the Echo device and AWS/Developer accounts are setup on the **SAME** Amazon account. If you use multiple users accounts on your echo device then make sure it is not switched to someone else's profile. Also make sure that the language of the skill (EN-GB or EN-US) is the same as the setting on your device

2. I am getting this error message: "The remote endpoint could not be called, or the response it returned was invalid"
Sometimes AWS doesn't like the zip. Try uploading it again.

If it is successful then you should see this output:-

    ```
    
    {
     "version": "1.0",
     "response": {
       "outputSpeech": {
         "type": "PlainText",
         "text": "milk was added to your shopping list."
       },
       "card": {
         "content": "milk was added to your shopping list.",
         "title": "Appie - Shopping list",
         "type": "Simple"
       },
       "reprompt": {
         "outputSpeech": {
           "type": "PlainText",
           "text": ""
         }
       },
       "shouldEndSession": true
     },
     "sessionAttributes": {}
    }
    
    ```
This means that the basics of the skill are functioning.


3. I am getting this error message:-

    ```
    Task timed out after 3.00 seconds
    ```
You have missed one of the steps. To fix this, go to the Configuration Tab in the Lambda Console, click on Advanced settings and in the Timeout box, increase the time to 10 seconds. Then click on Save.

4. My upload to lambda takes ages and then I get a "signature expired".

Your PC/Mac's clock is wrong. Turn on the automatically set time option in your control panel


5. Other errors.
Try uploading the zip file again, and wait a minutes or so before testing in the simulator or on a real device. This sorts out most things.
