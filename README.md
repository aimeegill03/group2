## Overview

This dipository contains the code used for the mini-thesis for the group project of Data Science in Finance (a master's seminar at Erasmus University Rotterdam). 
The code consists of two following components:

1- DataCollection is a folder with code that collects, combines, and cleans the data. The data source includes data provided by Jensen, Kelly and Pedersen (2023) which they used for their paper: as cited below:
Jensen, T. I., Kelly, B., & Pedersen, L. H. (2023). Is there a replication crisis in finance?. The Journal of Finance, 78(5), 2465-2518.

2- Analysis is a folder that contains the analysis in this mini-thesis. This includes the code for all models, with all variations used in the paper/what we adapted for our project.

# Please note, we have provided all the code used in our project. We have created this code with all intents and purposes to recreate and extend the work from:
Choi, D., Jiang, W., & Zhang, C. (2024). Alpha go everywhere: Machine learning and international stock returns. Available at SSRN 3489679.

Much of this paper is impossible to recreate given our limited computational power. This is besides the point for the code provided here: It _can_ recreate the paper fully, but does not. To be specific, it limits the recreation in terms of:
1) Variation/Number of model specifications
2) Size of datasets used (We cut using market capitalization methods, see ME Extraction and Analysis under DataCollection -> Joseph & Aimee's Code)
3) Hyperparameter tuning ranges (detailed in the final paper)

In total, this reduced model run-throughs (total number of models created, including also within-model gridsearches) from the "millions" level to a more manageable "tens of thousands" level.

The full expansion of the gridsearches used in the paper are _not_ detailed in our code within this directory but it is very easily extrapolated from it. See our paper for more details.

# Disclaimers:
ChatGPT was used throughout this project. Its use was limited, e.g., it was used pre-code to analyze and summarize, understand methodologies, reasons for using models or certain cleaning methods. Additionally, it was used to generate code snippets throughout, explain certain errors, or clarify complicated procedures. Its use was monitored, and filtered to ensure that the code output was true to what we wanted, and that we understood every output which we were individually tasked to create.

The code provided within this directory is open to see and use/mimic. If you have questions about anything within, please contact us through the following emails:
1) aimeemgill@gmail.com
2) josephbarber2001@gmail.com
