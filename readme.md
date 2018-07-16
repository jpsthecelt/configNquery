This is a notebook demonstrating a prototype set of functions from from a program I created
called configNqueryCmdline.py. 

The notebook is a Jupyter (iPython) notebook which creates an R session and 
uses the R library reticulate to call python functions which query the BigFix server 
using a specified 'relevance' string ['Relevance' is the query-language used by the BigFix server
to retrieve endpoint information https://www.ibm.com/support/knowledgecenter/en/SS6MCG_9.2.0/com.ibm.tivoli.tem.doc_9.2/Platform/Relevance/c_relevance_overview.html].

PREREQUISITES:
1) On your development machine, you have to have the following properly-working setup:
- An up-to-date iPython or anaconda installation, suitable for executing the commandline 'jupyter notebook .'
- An installation of R
- An R kernel, installed within Commandline R, as per: https://www.datacamp.com/community/blog/jupyter-notebook-r

So, the configuration-file used in both in the commandline and Jupyter-Notebook scenarios is stored in a file 
called 'credentials.json'. The python program reads the specified BigFix server URL, username, and password
and returns it as a configuration-dictionary. The elements can the be used by queryViaRelevance(p1, p2).

The sample notebook file shows it's employment in a Jupyter-Notebook setting. 
A typical use might be to initially use the config file information to 'set up the connection' via
readConfig(<filename>) and then query information using queryViaRelevance(<credentials>, <relevance-string>)

Within the 'commented-out example' in the main section of the program (the __main__ 'stanza'),  the parsing 
is potentially problematic, so we use the python 'untangle' library to parse the XML using a 
list-comprehension of the '<Answer>' nodes within the XML.  

This list is used to create A Pandas dataframe, which is then passed on to R for manipulation.

As far as Relevance, Sample query strings might be phrases like 'names of bes computers' or 
'names whose (it as lowercase contains "adhay") of bes computers' [Notice that embedded quotes within
the Relevance have to be 'escaped' by using the ascii-hex string %22].

The query returns XML, which is then passed to another python function to retrieve a parsed list of
elements, suitable for creating a dataframe (An example use is included as a comment in the
code). 

The dataframe can then be used to manipulate the data using R program-constructs.

The intent is to use this as a configuration/query step in generating pretty graphs from within R & Zeppelin
notebooks, and eventually, shiny apps.

best,
jpsinger
wizard-at-large
