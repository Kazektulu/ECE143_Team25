# __ECE143_Team25__

Steven Sharp - .....2191 <br/>
Tanaya Kolankari -  <br/>
Yifei Wu -  <br/>
<br/><br/>

# __Discretionary Income Checker__<br/>

## Introduction
 This project is for a class assignment in accordance with UCSD and ECE 143 guidelines. The objective is to probe and build abilities in data analysis utilizing real world datasets to perform a realistic and interesting objective. Rather than a singular task for the sake of novelty, we chose to build a toolset that is something each of us see as useful and important for not only us, but the other students and working professionals alike.<br/><br/>

## Stage 1
__Planning and Framing the program__<br/>
*As of now, we have framed out objective and listed a number of expectations for meeting our goal. We have hashed out a number of dependancies and ideal inclusions for a better implementation.<br/> Since we are also learning how to implement these functionalities and skills from scratch, there is a chance that the project could be more ambitious or simpler than we may expect. Under the case that the objective is simple, we have also discussed possible added features to make this program more robust and useful for the most likely purposes of use.*<br/><br/>
 * __Expected use Cases:__
   * A tool for students and professionals to assess a more realistic comparison of a job salary expectation in a given higher or lower cost of living area.
   * A tool for use to gauge reasonable pay for negotiation with employers or employees
   * General Purpose Budgeting insights<br/>
 * __Expected target Audience:__ 
   * Students
   * Young Entry level Professionals
   * Industry professionals looking to move to a new area or weighing a new job offer
   * Individuals wanting to frame job outlook based on Quality of Life obtainable<br/><br/>

## Stage 2
__Gathering the Data__<br/>
* Datasets distributed and scraped, collected, cleaned and consolidated: Tax Datasets *(FICA, Federal, State, Local County)*, CoL Dataset (Numbeo)*
  * __Issue arisen__: Numbeo Dataset inconsistent and user-entry based. Alternative dataset discovered under ideal framework as [__'LivingWage'__ data](livingwage.mit.edu). Living Wage dataset includes
    i. $base qty, 
    i. Average Medical costs
    i. utility fees
    i. local sales taxes 
  * Tax datasets not easily pre-structured as expected, significant manual data cleaning required before application.
  * Skill gap in web-scraping and cleaning required heavy
* Consolidating the data requires some conventional standards between data types before processing mathematically.

## Stage 3
*Consolidating some basic python function definitions, methods, framing flow and validations.*
