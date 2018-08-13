import untangle
import pandas

# Sample lambda function to parse returned XML & extract computer-names (note it has 1 parameter &
        #        returns a dataframe
        #        previously: ResponseDataframe = pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf1 = lambda x: pd.DataFrame([i.cdata for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf2 = lambda x: pd.DataFrame([i.cdata.split(">") for i in untangle.parse(x).BESAPI.Query.Result.Answer])
computersLf3 = lambda x: pd.DataFrame([i.cdata.split(",") for i in untangle.parse(x).BESAPI.Query.Result.Answer])
