# Data Logger and Visualizer for 4G Router (ZLT_P11X)

This is a simple data logger application for 4g routers to monitor the performace over time

1. Install the requirements with pipenv Pipfile.
2. Run the Data Logger with
```
  python data_logger.py
```
3. Run the visualizer (Using Dash)
```
  python data_visualizer.py
```  
4. Optionally you can run device notifier which will notify new device connections and device going offline. The notifier is set to Telegram, you will need to create a Telegram bot and provide its Token and your user I.
```
python notifier,py
```



