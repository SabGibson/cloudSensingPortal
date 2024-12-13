
# IOT Cloud Sense

A project that uses software based sensors to extract, process and transform information. Such that it can be digeted by a client application and deliver insights.

## Background 
The code component for the IOT project, that shows the creation of MVP for an application. That tracks the Fx values of and the price of amazon best seller baskets. Displayed in a dashboard.


## Features 
- Data analysis
- Database Connection 
- Web Client Interface for Data Viewing


## Technology 
- Python: Core programming language used for development, offering robust libraries for data processing and analysis

- Streamlit: Open-source framework for rapidly building and sharing data applications, used for creating the interactive dashboard interface.

- Pandas: Data manipulation library for Python, used for efficient handling and analysis of structured data.

- Black: Python code formatter that automatically formats code to conform to PEP 8 style guide, ensuring consistent code style.

- Pymongo: Python distribution containing tools for working with MongoDB, enabling database interactions.

- Azure: Microsoft's cloud computing platform, used for hosting and deploying the application.

- Docker: Containerization platform used to package the application and its dependencies, ensuring consistent deployment across different environments.

## Deployment
This application was deplyed on the cloud and is avaliable to view [here](https://iotdashboard--hdhsim2.icyplant-7192f703.australiaeast.azurecontainerapps.io/)

To run the dashboard client for this application

```bash
  docker build -t iot-dashboard
  docker run -p 8501:8501 iot-dashboard
```



## Bugs
Not Applicable 

## Licence(s)
MIT License

