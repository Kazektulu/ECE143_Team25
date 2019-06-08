# __ECE143_Team25__

Steven Sharp - ...2191 <br/>
Tanaya Kolankari - ...5700 <br/>
Yifei Wu - ...2438 <br/>
<br/><br/>

# __Discretionary Income__<br/>

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
__Gathering the Data__:<br/>
*Datasets distributed and scraped, collected, cleaned and consolidated: Tax Datasets *(FICA, Federal, State, Local County)*, CoL Dataset (Numbeo)*<br/>
  * __Issue arisen__: Numbeo Dataset inconsistent and user-entry based. Alternative dataset discovered under ideal framework as [__'LivingWage'__ data](http://livingwage.mit.edu/). Living Wage dataset includes
    1. $base qty, 
    1. Average Medical costs
    1. utility fees
    1. local sales taxes 
  * Tax datasets not easily pre-structured as expected, significant manual data cleaning required before application.
  * Skill gap in web-scraping and cleaning required heavy
* Consolidating the data requires some conventional standards between data types before processing mathematically.<br/><br/>

## Stage 3: Updates
*__Data changes before processing applied__:<br/> Results from gathered, cleaned and scrubbed data yeilded need for minor changes.*<br/>
  * __Data skipped__ due to manual cleaning complexity and complexity to resolving county<->city for different dataset sources: _County-based Tax Data_</br>   __Overall impact__: resolution of results increase to state, few data points for states dependant on county tax rather than a state rate will hold higher approximation error.
  * __Data added__: *Quality of Life Data* from *LivingWage Dataset* added to resolve questions/concerns regarding purely cost-based insights that may shift by urban vs rural environment, and add further analysis insight into which conditions may yeild a better target condition: whether QoL follows Population Density, CoL, or DI itself.
  * __Data Source Resolution__: Numbeo was already scraped, cleaned and added to appropriate frames, so will __continue to use Numbeo for CoL Data__. *LivingWage Data* may be applicable later if program/analysis needs to be taken to next version level for increased precision of calculations/qualifying data.<br/><br/>

## Stage 4
__Processing the Data__:<br/>
*The ideal Data Format will be processed in regard to user input variable as Salary, and process base calculations as defined by Discretionary Income:*<br/>
  * __Discretionary Income = [Salary] * (1 - [FICA Tax] - [Federal Tax] - [State Tax] - [~~Local Tax~~]) - [Cost of Living]__<br/>
  * To target interesting data analysis for presentation however, the user entry tool will be forgone to include other metrics to bring about insightful conclusions: 
     1. Firstly, *Salaries by job offer differ by region*. Thus, we will weigh the calculated DI against an Industry based regional basis as a value normalizing feature, and see if something interesting can be observed through the US. 
     1. Secondly, by evaluating purely monetary cost metrics by region affected heavily by CoL may ignore some key potential trends wherein *assuming high tax rates, and high cost of living provide high Quality of Life*, a Quality of Life rating of regions such as Metropolitan Hubs (where most high paying jobs would correlate) may be a worthy tradeoff for a lower DI, so a comparison will be performed here.
     1. Since the local tax data was (currently) too complicated to resolve between high volume collection, cleaning, and resolving hundreds of thousands of Cities and Counties to match data points - A dramatic loss of Resolution for precision observations will be expected as we will be left with *State Level* contrast. Surface Level observations will still be obtainable, but primary questions regarding Metropolitan vs Rural regions will be left inconclusive.
     1. To make up for lack of local data resolution, we will probe if there is something worth performing further analysis regarding *population density* by sampling a few state cases and pick a notable high, medium, and low population city and compare/ contrast data to see if a notable trend emerges, and give some insight into whether DI correlates well to natural economic responses or other data.<br/><br/>
     
## Stage 5: 
__Presentation and Consolidation of Data__:<br/> *Notes*
  * Interactive plots, graphs, and heatmaps have been produced and included within the presentation with overall descriptions; in a ppt format.
  * Embedding interactability within the presentation has proven tricky, but a .ppt embedding as a link within a local-only .ppt file as an embedded webpage over a member's PC installed with necessary supporting extension was able to work.
  * Included into conclusion some challenges, difficulties and ideal *next iterations* necessary to implement the best case version of our initial target data tool, under the notion that time and expertise are not delimiting factors.
  * Notably: Some state data points had *very few data points for CoL* (such as Washington, with one data point providing false impressions of positivity. or none from South Dakota): This was a huge red flag for overall quality of data distributed throughout the dataset as far as qualifying reliable, dependable, or scientifically sound results. This was a drawback of using __Numbeo__, which collects it's data through a voluntary user-data entry. *Overall trends will remain valid*, but again emphasising that the analysis touches on only *surface level observations*, without qualifying factors in data sources and high resolution data points.<br/><br/>

## Overall Observations:
  1. __Discretionary Income Correlates directly to Quality of Life__
  1. Cost of Living or Tax Rates __do not Correlate__ to Quality of Life
  1. __Population Density vs DI__ held two divergent trends with not enough data to produce conclusions. Highlighting it being worth investigating further for local resolution data.<br/> Speculation is that the source of CoL reductions roots differently by state policy: with CA having overall high costs and Tax across the state and NY costs being centered around NY City/ the High Population Density region by market forces.
  1. Trends among industry specific DI, by state distribution displayed observable trends for West vs East Coast analysis:<br/> Notably, Technology, Science, Medical trends hold higher DI (likely attributed specifically by Salary) held better yield in the West Coast, while Managerial and Administrative yeilded better DI in the East Coast - speculating to show the stereotypical coastal cultures in business styles hold divergent as progressive and more adaptable practices occur in the west vs the more traditional and structured practices in the East Coast states.
  1. One stark observation stands out for the Administrative Industry (support staffers) that correlates a negative DI calculated in CA, NY - wherein some of the highest population density metropolitan cities, and high CoL exist. This stands to tell of support staffers opperating on mostly nominal wages (yet usually above minimum wage) that speculates a struggle to maintain basic living standards under such high cost environments, irregardless of full time gainful employment.<br/> This trend does not follow to the other less population dense states however; So would require further analysis into more normalized and qualified datasets, and inclusion of local resolution data to draw any substantial conclusions.

