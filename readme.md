This is a notebook demonstrating a prototype set of functions from from a program I created
called configNqueryCmdline.py. 

The notebook is a Jupyter (iPython) notebook which creates an R session and 
uses the R library reticulate to call python functions which query the BigFix server 
using a specified 'relevance' string ['Relevance' is the query-language used by the BigFix server
to retrieve endpoint information https://www.ibm.com/support/knowledgecenter/en/SS6MCG_9.2.0/com.ibm.tivoli.tem.doc_9.2/Platform/Relevance/c_relevance_overview.html].

The configuration-file used in both in commandline and Jupyter-Notebook is stored in a file called 
'credentials.json'. The python program reads the specified BigFix server URL, sername, and password.

The sample notebook file shows it's use in a Jupyter-Notebook setting. 
A typical use might be to initually use the config file information to 'set up the connection' with
readConfig(<filename>) and then query information using queryViaRelevance(<credentials>, <relevance-string>)

Sample query strings might be phrases like 'names of bes servers' or 
'names whose (it as lowercase contains "adhay") of bes computers'.

The query returns XML, which is then passed to another python function to retrieve a parsed list of
elements, suitable for creating a dataframe (An example use is included as a comment in the
code). 

The dataframe can then be used to manipulate the data using R program-constructs.

The intent is to use this as a configuration/query step in generating pretty graphs from within R & Zeppelin
notebooks, and eventually, shiny apps.

best,
jpsinger
wizard-at-large
