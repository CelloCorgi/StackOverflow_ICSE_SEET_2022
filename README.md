# Debugging with Stack Overflow: ICSE SEET, 2022

This is the GitHub repository associated with the 2022 [ICSE SEET](https://conf.researchr.org/track/icse-2022/icse-2022-seet#event-overview) paper, _Debugging with Stack Overflow: Web Search Behavior in Novice and Expert Programmers_

## Abstract

Debugging can be challenging for novice and expert programmers alike. Programmers routinely turn to online resources such as Stack Overflow for help, but understanding of debugging search practices, as well as tool support to find debugging resources, remains limited. Existing tools that mine online help forums are generally not aimed at novices, and programmers face varying levels of success when looking for online resources. Furthermore, training online code search skills is pedagogically challenging, as we have little understanding of how expertise impacts programmers' web search behavior while debugging code.

We help fill these knowledge gaps with the results of a study of 40 programmers investigating differences in Stack Overflow search behavior at three levels of expertise: novices, experienced programmers who are novices in Python (the language we use in our study), and experienced Python programmers. We observe significant differences between all three levels in their ability to find posts helpful for debugging a given error, with both general and language-specific expertise facilitating Stack Overflow search efficacy and debugging success. We also conduct an exploratory investigation of factors that correlate with this difference, such as the display rank of the selected link and the number of links checked per search query. We conclude with an analysis of how online search behavior and results vary by Python error type. Our findings can inform online code search pedagogy, as well as inform the development of future automated tools.

## Authors

* [Annie Li](https://www.linkedin.com/in/annieli21/): <annieli@umich.edu>
* [Madeline Endres](http://www-personal.umich.edu/~endremad/): <endremad@umich.edu>
* [Westley Weimer](https://web.eecs.umich.edu/~weimerw/): <weimerw@umich.edu>

## Paper Link

The paper pdf can be found [here](http://www-personal.umich.edu/~endremad/papers/SODebug2022.pdf)

## Repository Contents

* [Stimuli](https://github.com/CelloCorgi/StackOverflow_ICSE_SEET_2022/tree/main/Stimuli): Contains images of the programming bugs used as stimuli in our experiment (text versions of the stimuli are in the Survey Instrument if needed)
* [Analysis](https://github.com/CelloCorgi/StackOverflow_ICSE_SEET_2022/tree/main/Analysis): Includes both details regarding the manual annotation process and our analysis scripts. We note that our spread sheet for "ground truth" annotations was originally done on google drive, and is thus more readable on that platform. The google drive version can be found [here](https://docs.google.com/spreadsheets/d/1BZy1nMYC4jgJclLBDBjeOGK26oRYcPItZQZlSQWFIh8/edit?usp=sharing).
* [Survey Instrument](https://github.com/CelloCorgi/StackOverflow_ICSE_SEET_2022/tree/main/SurveyInstrument): Contains word and qualtrics versions of the survey instrument used to show the stimuli to participants
* [Recruitment](https://github.com/CelloCorgi/StackOverflow_ICSE_SEET_2022/tree/main/Recruitment): Contains our consent form and prescreening survey

## Paper Citation
```
@inproceedings{Li2022DebuggingWith,
  author    = {Annie Li and
               Madeline Endres and
               Westley Weimer},
  title     = {Debugging with Stack Overflow: Web Search Behavior in Novice and Expert Programmers},
  booktitle = {To appear in the 44nd International Conference on Software Engineering: Software Engineering Education and Training (ICSE-SEET '22)},
  publisher = {{ACM}},
  year      = {2022},
  url       = {https://doi.org/10.1145/3510456.3514147},
  doi       = {10.1145/3510456.3514147}
}
```
