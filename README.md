
#  Lifeline: Accident Data Analysis for Karnataka State Police Hackathon

# Problem Statement
Traditional methods of accident data analysis often lack insights into patterns and contributing factors, limiting the effectiveness of preventive measures. Despite the vast volume of data collected by the police relating to accidents, this data is often underutilized for analysis and prediction purposes. Our challenge is to develop an advanced data analysis system, named Lifeline, which can identify accident patterns, high-risk locations, and contributing factors such as weather, road conditions, and driver behavior. By doing so, we aim to inform targeted safety interventions and infrastructure improvements to reduce the occurrence and severity of accidents.

# Approach
After critically assessing the problem statement and reviewing relevant research papers, we devised a comprehensive approach to address the challenge. Our analysis encompasses various variables including the time of accident, driver demographics, vehicle characteristics, location, and weather conditions. By examining these factors, we aim to identify patterns and correlations that can help predict future occurrences of accidents and understand their root causes.

# Key Features
Comprehensive Data Analysis: Lifeline analyzes accident data to determine the causes of accidents and identify contributing factors, whether related to driver behavior or road infrastructure. \
Spatial and Temporal Distribution: By recognizing spatial and temporal distributions of accidents, Lifeline helps in planning interventions and targeting safety measures effectively. \
Severity Classification: Accidents are categorized into fatal, serious injury, or light injury cases, enabling policymakers to develop appropriate prevention strategies and enhance emergency response protocols. \
Prediction Model: Lifeline utilizes a hybrid model consisting of K-Means clustering and Random Forest classification to predict the severity of road traffic accidents. This approach improves accuracy compared to traditional algorithms.
# Impact
The Lifeline project aims to make a significant impact on road safety by providing Karnataka State Police with actionable insights derived from accident data analysis. By identifying patterns, high-risk locations, and contributing factors, Lifeline empowers authorities to implement targeted interventions and infrastructure improvements, ultimately saving lives and reducing the number of accidents on Karnataka's roads.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Get Involved
We welcome collaboration and contributions to the Lifeline project. Whether you're a data scientist, policymaker, or road safety advocate, your expertise and insights can help make our roads safer for everyone. Reach out to us to learn more about how you can get involved in this important initiative.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Contributors

Yash Patle \
Nikhil Dhande \
Vinay Kamdi  \
Vaidhehi Thool 







<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Tech Used


**Python Libraries:** Streamlit,Flask,Follium,Plotlib,sklearn,keplergl,google.generativeai

**Server** Cloud Application,gemini_api






<p align="right">(<a href="#readme-top">back to top</a>)</p>
## Installation 
To install the requirements of project python should be installed  optional 3.11.9

## Optional
You can use the venv or u can either run it in the console 

```bash
   python -m venv venv
   venv/Scripts/activate
```
## Dependances
```bash
  pip install -r requirements.txt
```



## Deployment

To deploy this project run

```bash
    streamlit homepage.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>





# ScreenShots



## Main Dashboard  District,Year slicer
<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242522963732070483/Screenshot_2024-05-21_011357.png?ex=664e252f&is=664cd3af&hm=892c0dc7691002e42ea3e114b36418c5a2681581f9811eef7f5f9671e2442b74&">





## Pridiction of Black Spot with respect to distrcts
<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242525350286856284/image.png?ex=664e2768&is=664cd5e8&hm=d463b5df64da44f1d07344785d1639d019f139117694db45eaa6986a34679d18&">

## Pridiction of Grey zones with respects to distrcts
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242531837944008794/Screenshot_183.png?ex=665027b3&is=664ed633&hm=746116bc0d3cddf2afc54773315dcafaac6811785a095fba809849f8543b0c69&=&format=webp&quality=lossless&width=1193&height=671">

## Cluster based Heatmap
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242529600236683274/Screenshot_181.png?ex=6650259d&is=664ed41d&hm=f2c6d80f182575f12837538f0ad6e95e87902eb7cfd9ed3f412babbbbb54e32c&=&format=webp&quality=lossless&width=1193&height=671">
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242529600236683274/Screenshot_181.png?ex=664e2b5d&is=664cd9dd&hm=42dfdd61fddbd8b561cc8588259da7e5fa69d89ccfd0c65c8b36cd1e3ad8702d&=&format=webp&quality=lossless&width=1193&height=671">

## Suggestion Models Ai Recomdation
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242529536256770259/updated_black.png?ex=6650258e&is=664ed40e&hm=5cb6623d737c6e3fe9881dda7e4a60825765c9f560ffb8b1c2a6c5db2c893a4a&=&format=webp&quality=lossless&width=1398&height=671">
 # AI output
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242529535895801936/suggestion_ai.png?ex=6650258e&is=664ed40e&hm=064c4732f64fbfbbe3465f939754d51a8eb011257b25a7b5de62d3d384554ce3&=&format=webp&quality=lossless&width=1440&height=553">


## Suggestion Models Most Impactful factor
<img src="https://media.discordapp.net/attachments/1217137981337370805/1242522964109295698/Screenshot_2024-05-21_203201.png?ex=664e252f&is=664cd3af&hm=c759b2f2f230ce5dde096f07a87f7fa779367e712a89573303864282a987b2bd&=&format=webp&quality=lossless&width=1440&height=668">
## Suggestion Models Most Impactful factor AI suggestions
<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242529535895801936/suggestion_ai.png?ex=664e2b4e&is=664cd9ce&hm=1a57b8a80fe4c69c5e031fc2d0c182a32617c9180d6f0bf22dc900ede828aed7&">
## Suggestion Models Most Impactful factor options
<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242529690410025071/options.png?ex=664e2b73&is=664cd9f3&hm=081997027b78c4733651ef3265873654cd8800cd097f08c1bc02d756acc584bc&">

## open 360  road View


<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242532645972217866/image.png?ex=664e2e33&is=664cdcb3&hm=ad81204a3f8b3d3f9bbfe164b0e877803f8a582d6589ff92000f9ef36a6dcd91">

<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242532472462245969/image.png?ex=664e2e0a&is=664cdc8a&hm=6f40694209d01d829baeeb2e1a0b6317d8941d21252de5f91f2f0d53bbd7d4b1">
## Power bi reports

<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242522965871034369/Screenshot_2024-05-21_202352.png?ex=664e2530&is=664cd3b0&hm=b1b231cd13556535a34de317387ab223af8fd50bfc36ef3b7ed43e69c77a4997">

<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242522966567288983/Screenshot_2024-05-21_201703.png?ex=664e2530&is=664cd3b0&hm=1ba6800515071f0238d442e632fc16fc128a7ad906395f148332dae86fd1a367">

<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242522967271800933/Screenshot_2024-05-21_200913.png?ex=664e2530&is=664cd3b0&hm=8dfd86efaf2acf26ecf051626637191eadbca8b19cdf829863d376a9b5ff0809">

<img src="https://cdn.discordapp.com/attachments/1217137981337370805/1242522966206709920/Screenshot_2024-05-21_201800.png?ex=664e2530&is=664cd3b0&hm=2775d1948c68fbe3e1b65f7b840d5546cc030e6faade4b2bf809921ad05943c2">





