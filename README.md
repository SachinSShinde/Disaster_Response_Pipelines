# Disaster Response Pipeline Project
A machine learning pipeline built to categorize emergency messages based on the needs communicated by the sender

Follwing a disaster you will get millions of messages either direct or via social media right at the time when disaster organizations have the least capacity to filter and then pull out the messages which are important. Often one in thousand messages that might be relevent and important to the disaster response professionals.So the way that disasters are typically responded to, is that different organizations will take care of different parts of the problems. So one organization will take care of water, another will care about blocked roads, medical supplies. These are the categories which data is pulled, combined and relabelled from Figure Eight. The motivation of this project is to build tool/classifier to categorize tweets/news/messages of disaster time to certain categories to facilitate identifying help needed in emergency situation.

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
