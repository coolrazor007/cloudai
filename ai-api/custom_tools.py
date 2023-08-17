# from langchain.llms import OpenAI
# from langchain.agents import initialize_agent, load_tools, Tool
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# #from langchain.tools import DuckDuckGoSearchRun
# import subprocess

from langchain.tools import BaseTool
from langchain.tools import DuckDuckGoSearchRun
import subprocess


##########################################
# Git Section                            #
##########################################
# def git_status(return_info = False):
#     info = {"name": "git_status", "description": "Git status is a command used in Git, a version control system, to display the state of the working directory and the staging area. It lists out all the files that have been modified, deleted, or newly created, but not yet committed to the repository. Additionally, it shows which changes are staged for the next commit and which are not, providing a clear overview of your project's current state."}
#     if return_info: return info

#     # very helpful link: https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
#     # print("test running a command", "\n")
#     # result = subprocess.run(['ls', '-l'], capture_output=True, text=True).stdout
#     # print(result)

#     #Passing args INTO the command
#     # print("test passing in arguement:", "\n")
#     # cmd = ['cat', '>>', 'text.txt']
#     # text = "Hello world"
#     # result2 = subprocess.run(cmd, stdout=subprocess.PIPE, input=text)
#     # print(result2)


#     print("Running git_status", "\n")
#     cmd = ['git', 'status']

#     result3 = subprocess.run(cmd, stdout=subprocess.PIPE)
#     print(result3)


##########################################
# Search Section                         #
##########################################

class DuckDuckGoSearchTool(BaseTool):
    name = "DuckDuckGo Web Search"
    description = "use this tool when you need to search or browse the internet"
    single_input = True
    return_intermediate_steps = True

    def _run(self, query):
        search = DuckDuckGoSearchRun()
        # search.run(query)
        #query.run()
        search.run(query)
        print('\n','########')
        print('Here is the values in the search variable: ', search)
        print('########','\n')
        return f"Results for query {query}"

    def _arun(self, query):
        raise NotImplementedError("This tool does not support async")

    @property
    def is_single_input(self):
        return self.single_input




# class CircumferenceTool(BaseTool):
#     name = "Circumference calculator"
#     description = "use this tool when you need to calculate a circumference using the radius of a circle"

#     def _run(self, radius: Union[int, float]):
#         return float(radius)*2.0*pi

#     def _arun(self, radius: Union[int, float]):
#         raise NotImplementedError("This tool does not support async")
