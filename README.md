# Watch out for homicides :oncoming_police_car::ambulance:(Dashboard for Homicide Cases in America) 

**Heroku**: [https://dash-app-murder.herokuapp.com](https://dash-app-murder.herokuapp.com)

## Welcome!

First and foremost, Welcome! :tada::balloon::balloon::balloon:         
             
Thank you for visiting the `Watch out for homicides` app project repository.          

This document (README file) is a hub to provide you with some information about the project. Jump directly to one of the sections below, or scroll straight down to find out more.

* [Who are we?](#Group-information)
* [What is our ideal project?](#Initial-Ideas)
* [What are we doing?](#Introduction)
* [What does our package include?](#Package-Structure)
* [How to use our project?](#How-to-use)
* [How can you get involved?](#How-to-Contribute)
* [Get in touch](#Contact-us)

## Group information
- **Group members: Yuxin Chen :wink: & Siyue Gao :blush: & Xinyu Dong :grin: & Matthew Yau :smirk:** 

## Initial Ideas

There will be four tabs in total to depict the homicide cases data in America: geographical distribution,  Rose chart breaking down by season and month, the direction of crimes among different race and gender groups with a Sankey graph, and the trend line graph by gender over time.  

The first tab is designed to mainly demonstrate the geographical distribution of homicide over America, with a date selection component, a drop-down menu to filter weapon categories and a bar chart to summarize race and gender aggregation. By using this tab the user can easily filter out the interested subset and observe how those cases are distributed geographically.

![](https://github.com/KingOfOrikid/DATA551_proj/blob/Xinyu/sketch/Tab1.png)

The second tab is to show the frequency of homicide is regulated by season or month. By changing the drop-down menu, users can select the cases given specific relationship, weapon, crime type and state.

![](https://github.com/KingOfOrikid/DATA551_proj/blob/Xinyu/sketch/Tab2.png)

The third tab aims to show specific *crime corridors* between different race and gender groups. The area sitting on the left and right side means the percentage of that group as perpetrator or Victim. The width of the line connecting each group indicates the count of cases. 

![](https://github.com/KingOfOrikid/DATA551_proj/blob/Xinyu/sketch/Tab3.png)

## Introduction
Homicides in the United States is an important topic to think about. Compared to other high-income countries, the US contains greater homicide rates (e.g. gun homicides, https://pubmed.ncbi.nlm.nih.gov/30817955/). Because homicides can cause significant negative effects (e.g. loss of life), it may be important to investigate ways to reduce the negative effects of homicides.                   
                               
One way to address the negative effects of homicides in the US may be to provide general education about homicides. General education can be helpful in at least two ways: 1) For everyday citizens, awareness about homicides (e.g. what types of crimes are likely to be committed, in which regions), may increase citizens’ abilities to prepare and defend themselves against attacks. 2) For people working in crime-related areas (e.g. law enforcement), information about homicides may increase their ability to pinpoint and reduce criminal activity.                                     
                  
Therefore, the aim of the current project is to create tools that could provide education about homicides in the US. Specifically, we will create an interactive dashboard investigating homicide-related data from the 2010’s to 2014s. This dashboard could be used to provide insights into relevant questions, such as examining how homicide-related activity is distributed geographically across the US.                

## Package Structure

```
project/
├── data/  
│   └── database.csv
│
├── src/             
│   └── app.py
│
├── reports/
├── doc/
│   ├── sketch/
│   ├── main_submission_proposal.md
│   ├── reflection-milestone2.md
│   ├── demo.gif
│   └── team-contract.md
│
├── requirements.txt
├── README.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── LICENSE.md
```

## How to use

```
$ pip install -r requirements.txt
$ python src/app.py
```

Open the link displayed on the terminal.                     
                      
![demo.gif](https://github.com/KingOfOrikid/DATA551_proj/blob/main/doc/demo.gif)

## How to Contribute
Please note that this project is released with a [Contributor Code of Conduct](https://github.com/KingOfOrikid/DATA551_proj/blob/main/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.              
         
If you think you can help in any of these areas or in many areas we haven't thought of yet, then please take a look at our [Contributors' guidelines](https://github.com/KingOfOrikid/DATA551_proj/blob/main/CONTRIBUTING.md).          
           
## Contact us
If you want to report a problem or suggest an enhancement we'd love for you to [open an issue](../../issues) at this github repository because then we can get right on it. But you can also contact [Yuki(Yuxin)](https://github.com/KingOfOrikid) by email yuxin.yuki.chen@gmail.com.