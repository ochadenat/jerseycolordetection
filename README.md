# [FootShirt.com](https://www.footshirt.com)
![alt text](https://www.footshirt.com/assets/logo/footshirtlogo-small.png "FootShirt.com")

[FootShirt.com](https://www.footshirt.com) is the site for soccer fans that enjoy collecting jerseys and/or are passionate by the history and values communicated by soccer shirts. 

Managing your jerseys collection can not be easier. Easily add your jerseys to your digital closet. Browse through the available jerseys or add your own. 
Add the jerseys you plan to buy or receive as a gift to your Wishlist that you can share with friends and family. 

Read our blog that features articles about soccer shirts. Do you think you know everything about soccer jerseys? Try our quizzes and compete with other 
fans around the world to be on the top of the leaderboard.

# Introduction

The goal of this notebook is to demonstrate the use of data visualization techniques and libraries while using hopefully a fun dataset. We will focus on Soccer Jersey Dominant Color in this notebook and create many 3D scatter plots.

# Dataset

## Home, Away and Third Jerseys
For a very long time, soccer teams had only two jerseys referenced as Home and Away. These two jersey types had very distinct colors in case two teams having the same main color were playing against each other (think Manchester United versus Liverpool Red Jerseys). It's worth mentioning that many teams have still an Away jersey with white as the dominant color, likely a heritage from the black and white TV era.

Third Jerseys started appearing 20 years ago. Teams are using them if both their first-choice and away colors are deemed too similar to those of an opponent. It's also believed to be a way for kit suppliers to increase sales by offering designs that appeal to younger generations (bright colors, etc…). Recently, Third Jerseys have been mainly used for the Away games in the European Cups.

## Records
The dataset has around 3,200 records (i.e. jerseys) covering 156 teams (104 Clubs and 52 National Teams). Some teams might have only 1 jersey in the dataset while other popular teams such as Manchester United will have 104 jerseys. In addition, the recent period is more represented compared to other periods: 2,034 jerseys for 2005–2019 vs 1,198 jerseys for the period pre-2005.

This will introduce a bias toward popular teams, the recent past, the Home jersey in some analysis. Goalkeeper jerseys have been excluded in most analyses and visualizations.

## Fields Description
| Field                 | Description   | Example/Value
| --------------------- | --- | ---
| **id**                | jersey unique id                                    | 1, 2, 3
| **team_id**           | team unique id                                      | 1, 2, 3
| **teamname**          | team name                                           | Boca Juniors
| **teamtype**          | team type                                           | Club, National   
| **teamcountry**       | team country                                        | Argentina
| **homeawaythird**     | jersey type                                         | Home, Away, Third, Goalkeeper  
| **season**            | season                                              | 2018-2019
| **image_caption**     | concatenation of team name, season, and jersey type | Boca Juniors 2018-2019 Home
| **image_color**       | jersey dominant color                               | rgb(50,72,81)
| **image_r**           | jersey dominant color red component                 | Number between 0 and 255, e.g. 50  
| **image_g**           | jersey dominant color green component               | Number between 0 and 255, e.g. 72
| **image_b**           | jersey dominant color blue component                | Number between 0 and 255, e.g. 81
| **image_content_url** | Jersey image URL                                    | https://
| **brand_id**          | kit supplier unique id                              | 1, 2, 3
| **brandname**         | kit supplier                                        | Adidas, Nike, Puma

Each jersey is assigned one (and only one) dominant color. We will use the RGB Color model in which each parameter (Red, Green, and Blue) defines the intensity of the color as an integer between 0 and 255.A future analysis will handle several dominant colors to take into account shirts such as Juventus Turin jerseys where both black and white can be considered as dominant colors.