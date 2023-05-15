---
title: "The vaccination campaign in Tunisia: a blameless crime ?"
subtitle: ""
excerpt: "
Assigning responsibilities in the case of the mismanagements of a public health crisis
is nothing but a basic expectation from democratically elected officials.
But what if citizens are the culprits ? So we are told.
In this short exploration, I go through one aspect of the efforts against the 
COVID-19 pandemic in Tunisia: the registration for vaccinations.
"
date: 2021-07-21T12:17:41+01:00
author: "Iyed Ghedamsi"
draft: false
series:
tags: ["COVID-19", "Tunisia"]
categories:
layout: single # single or single-sidebar
---

> **Disclaimer I**: The data used throughout this piece
> has been scraped from the *'open data'* section of [EVAX](https://evax.tn).
> It is very possible that I made a mistake collecting / interpreting
> the data given that It was collected in non-traditional ways. The code I used
> is available in the end of the article, [please check it for yourself](https://github.com/iyedg/iyedg.github.io/blob/develop/content/blog/vaccination_campaign_tunisia/notebook/scraping.ipynb) .


> **Disclaimer II**: This is an opinion article despite it having
> graphs and numbers. It should not be taken as nothing more than a
> random stranger's opinion on the internet.

## Introduction

Assigning responsibilities in the case of the mismanagements of a public health crisis
is nothing but a basic expectation from democratically elected officials.
But what if citizens are the culprits ? So we are told.
In this short exploration, I go through one aspect of the efforts against the 
COVID-19 pandemic in Tunisia: the registration for vaccinations.

## Citizen awareness: the tale of a scapegoat


{{< figure src="images/cum_line_plot.png" title="" >}}

Looking at the two plots above outlining the number of registrations
on the official platform **EVAX**, an upwards trend in the population and
across all age groups is clear.
Although some groups have higher registration rates such as ages *50-60*
and *60-70*, the other groups do show an accelerated registration rate
starting from June, most notably the *18-30* group. Based solely on these
observations one might be tempted to question the dominant narrative
that *Tunisians do not want to get vaccinated*. Yet a rephrasing of the of this blame
pushes us to further analysis: *Are Tunisians registering fast enough ?*

### Enter: The dip

{{< figure src="images/stream_plot.png" title="" >}}

 A first observation to make from the graph above is the peculiar dip in the number
 of registrations for the vaccinations by the end of January. Yet looking at
 how the trend is reversed right after the beginning of the vaccination campaign,
 it seems to me that an explanation, and an answer, arise. With 52 days between the
 launch of EVAX and the first day of the vaccination campaign, registration efforts were bound
 to fizzle out with no immediate or foreseeable outcome in sight. More importantly,
 a variety of phenomena can explain the registration rate of Tunisians following the
 beginning of the vaccination campaign. Firstly, the economic crisis and the inconsistent
 signals provided by the government regarding their ability to purchase the necessary
 vaccine quantities are certainly a hindrance for any effort to onboard people on EVAX.
 Secondly, a notable failure of the COVID-19 national strategy 
 was the lack of communication on the safety of the vaccines. The void left by this 
 absence left room for a variety of rumors and misinformation / disinformation to plague
 the public discourse about vaccines.


### The crestfallen bunch

Right before Eid al-Adha, a Facebook post on the Health ministry's page announced 
[*Vaccination Open Days*](https://www.facebook.com/santetunisie.rns.tn/posts/4322448191127585) 
on the 19<sup>th</sup> of July, at 3:21 PM, for anyone older than 18.
The announcement caused a lot of confusion and excitement. A registration frenzy ensued: 45 566
people between the ages 18 and 30 registered on the 19<sup>th</sup>. That's 17 211 more registrations
than the next day with the most registrations for that age group. The interest of the young groups,
however, precedes this event. The graph below shows that the *30-40* had climbed two positions to become
the second most registering age group by the 12<sup>th</sup> of July. As well as the *18-30* group that 
became the highest ranking group on the 16<sup>th</sup> of July. Thus dispelling the last
drop of doubt that Tunisians are *'unaware'* of the importance of vaccinations. Instead, what Tunisians
needed was .. vaccines.


 > ***Crestfallen*** : disappointed and sad because of having failed unexpectedly.
 > -- <cite>Cambridge Dictionary</cite>


{{< figure src="images/bump_plot.png" title="" >}}

The disappointment followed the Eid al-Adha's episode is one to be remembered, hopefully long enough
to punish those responsible. A simple look at the data readily available on EVAX would have made is sufficiently
clear that calling upon *every Tunisian old enough to be vaccinated* within two days was an exercise in stupidity and tomfoolery.
With the absence of common sense that is.

## The road ahead:
{{< figure src="images/comp_plot.png" title="" >}}

It goes without saying that engaging in an honest an thorough analysis
of the bottlenecks slowing down the vaccination process is a must. 
Between the over-worked and understaffed health workers and the saturation of the
whole health system of the country, clear measures must be taken to firstly
curb the spread of the virus and to efficiently vaccinate the remainder of the population.

Relying on the *'citizen's awareness'* has become a meme that simultaneously denigrates
any civilised behaviour from Tunisians and branding them as *de facto* savages until
they prove otherwise, and a representation of a weak political class that can do nothing but serve the
rich and blame the poor. I say, citizens are aware, as aware as their material conditions allow them to be.

