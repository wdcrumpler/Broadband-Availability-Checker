# Broadband-Availability-Checker

A project of KC Digital Drive

<h3>Concept</h3>
Create a tool that can take a list of all addresses in the Kansas City metro and check each major ISP’s website to determine whether the provider offers internet service at that address. If the provider does offer service, the tool records what speeds and prices are offered.

<h3>Goal #1</h3>
Ensure all KC neighborhoods that lack access to high quality broadband are eligible for upcoming grant funding.

In 2024 states will undertake a major broadband grant program designed to help finance the construction of new network infrastructure in locations that currently lack access to affordable high-speed internet. An area’s eligibility to receive funding will be determined by the level of service that ISPs have reported to the FCC. If at least one ISP claims to serve an address with a broadband plan of at least 100/20 Mbps speeds, other internet providers cannot receive grant funding to serve that location. The problem is that internet providers are known to overstate their coverage. This means that there are many areas that should be eligible for broadband funding, but won’t be because of misreporting by ISPs. This tool would provide a source of ground truth that could be used to rigorously dispute any instances of overreporting, and ensure that all KC neighborhoods that do not have access to broadband have the opportunity to be served by upcoming grant programs.

<h3>Goal #2</h3>
Determine whether any neighborhoods in Kansas City are affected by price or speed discrimination by internet service providers. 

This tool would record not only whether broadband is available at an address, but also the speeds and prices available. The result will be a rich dataset that could be used to reveal evidence of price and speed discrimination by ISPs, if this should exist. Previous work has revealed that AT&T forces some neighborhoods in Kansas City to pay more for worse quality internet, but we currently lack information about whether neighborhoods experience general disparities when accounting for all internet providers that offer service in a neighborhood. 

<h3>Goal #3</h3>
Provide a high quality data source for understanding the metro’s broadband needs.

In addition to using this data to interrogate the practices of specific ISPs, the data could be useful more generally in understanding the current broadband infrastructure landscape in the metro. Speed test data is often used to provide a picture of which areas do or do not have access to high quality broadband, but speed test results can be affected by many variables unrelated to the level of service offered by ISPs. Having address-level plan data would serve as a more robust foundation for analysis, and help answer questions about fiber penetration and the level of broadband competition in the metro. 

<h3>Step #1</h3>
Compile a list of addresses in the Kansas City Metro

Status: List of addresses obtained from CostQuest. Currently seeking to gather additional supplementary datasets for comparison and cleaning.

The first step in building the tool is having a high quality list of all households in Kansas City to run against provider’s web sites. There are several sources that can be used to compile this list.

The NTIA recently contracted with the firm CostQuest to build a list of all broadband serviceable locations across the country. This list of addresses (frequently referred to as the broadband fabric) was used as the foundation for the FCC’s broadband map, and is the basis for reporting by ISPs. KC Digital Drive has successfully applied for a license to access CostQuest’s fabric data, and has generated a list of addresses in Kansas, Missouri, and the KC metro to use as inputs for the tool.

However, CostQuest’s fabric data has come under criticism by some in the broadband and digital inclusion space for leaving off a large number of households. This is an issue because internet providers cannot apply for grant funding to serve households that are not included in the map. 

For this reason, KC Digital Drive is interested in gathering additional sources of address data, including from E911 databases, tax assessments, and water utility records to compare against the fabric and identify potential missing locations. Any locations revealed as missing through this exercise will be reported to the FCC and to state broadband offices so they may be considered for upcoming grant funding. 

KC Digital Drive is currently working with the city of Kansas City, Missouri to gain access to these records. 

<h3>Step #2</h3>: Build a program that can automate a lookup process to record the price and speed of service offered by each ISP at each address in the metro

Status: KC Digital Drive, with the assistance of volunteers with Code for KC, is currently developing this tool. A prototype was successfully developed to analyze 1,162 locations in the 5th District to determine whether they were served by Google Fiber and Spectrum. 

The project aims to support lookups for five major providers in the KC metro: Google Fiber, Spectrum, Xfinity, AT&T, and Everfast. Current development is focusing on building a program that is able to navigate each provider’s website, insert a given address into the site’s lookup function, submit that address, and then record the resulting information. 

Initial testing will take place using a list of households in zip codes 64132, 64134, and 64139. Once the functionality of the tool is confirmed, the team will scale the program to be able to rapidly process all households in the KC metro. 

<h3>Step #3</h3>: Analyze collected data and use results to inform state and local decision-makers.

Status: Awaiting generation of broadband data.

The first set of outputs will be a list of addresses where actual ISP availability differs from what has been reported to the FCC. Based on the output of the tool, the team will develop a methodology for reviewing all addresses considered served by the FCC, but which do not actually have service according to ISP websites. The team will document these cases and submit any findings to the FCC and to the Kansas and Missouri offices of broadband development. 

The second set of outputs will focus on whether we found any evidence of speed or price discrimination by specific providers or in the broadband ecosystem as a whole. This may include maps and accompanying analysis of:
- The maximum speed tier available for purchase in each census block in the metro
- The minimum price to purchase a broadband plan in that block serving speeds of at least 100/20 Mbps
- The price of a 100/20 Mbps plan for each provider in blocks where they offer service
- The average price per Mbps for all plans offered in the block

The third set of outputs will focus on the broadband infrastructure landscape more generally, and may include maps and analysis of:
- A block-level map of fiber availability
- The number of competing ISPs in each block, and analysis of how the price of available plans is affected by competition
- A cross-analysis of broadband availability with speed test results to highlight areas where low speeds may be due to a lack of access to high speed plans, versus areas where low speeds may be due to affordability, equipment, or network quality issues.
