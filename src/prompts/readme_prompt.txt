You receive a Python dictionary that describes the functionality of a software \
project. The project was mainly developed in the language {programming_language}.
The keys in the dictionary consist of file paths, with the root directory \
being the root directory of the project. This allows you to implicitly learn \
the package structure of the software project from the keys.
The values ​​are lists in which the classes that appear in the respective file \
are stored. You will also find the entry "global" in the lists, which \
describes the logic of global functions in the file. Both are stored as a \
nested dictionary. In these nested dictionaries you can finally find textual \
descriptions of the functions that are in the respective class or that have \
been defined globally.

--- Minimalist example ---
####
{{
    "project_root_dir/main.py": [
        {{
            "Main": {{
                "__init__": "This docstring is documenting the __init__ method in the Main function.",
                "Main": "This docstring is documenting the Main class itself."
            }}
        }},
        {{
            "global": {{
                "global_function": "This docstring is documenting the global function global_function."
            }}
        }}
    ],
    "project_root_dir/__init__.py": [
        "This file is empty."
    ],
}}
####

--- Data sructure containing project information ---
####
{project_information}
####

Your task is to create a readme file (in markdown code) for the software \
project using such a data structure.
Here is a sample readme file. Learn the pattern and use it as a template. Fill \
the template with relevant information you learned from the data structure.
If you are missing information to complete certain sections in the template, \
leave the sections out.

--- Readme sample ---
####
# Project Title

A brief description of what this project does and who it's for


## Table of Contents

- [Contribution](#contribution)
- [Keywords](#keywords)
- [Technologies](#technologies)
- [Installation](#Installation)
- [Introduction](#introduction)
- [Data Acquisition](#dataacquisition)
- [Result Analysis](#resultanalysis)
- [Real-life applications of the project](#Real-lifeapplicationsoftheproject)
- [License](#license)
- [References](#references)
## Contribution 

Define the contributers name, email id and contibution(roles in the project) in the following manner.

Example:

Shafait Azam - s.azam@reply.de - Data Acquisition, Programmer, Automation etc.

## Keywords
Define the Keywords of the corresponding project, so that it can be easier for the user to search through.


## Technologies

Define the Technologies which have been used to develop the corresponding project and also add the icon of the technologies. Select the correct icon from the following examples. If more than one technologies are used, then generate icon for all of them.

1. For "Programming languages":

If "python" is used then use the following code to generate Python Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/></code>
</div>
"""

If "java" is used then use the following code to generate java Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/117201156-9a724800-adec-11eb-9a9d-3cd0f67da4bc.png" alt="Java" title="Java"/></code>
</div>

"""

If "Android" is used then use the following code to generate android Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/117269608-b7dcfb80-ae58-11eb-8e66-6cc8753553f0.png" alt="Android" title="Android"/></code>
</div>

"""

If "C++" is used then use the following code to generate C++ Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/192106073-90fffafe-3562-4ff9-a37e-c77a2da0ff58.png" alt="C++" title="C++"/></code>
</div>

"""

If "C#"  is used then use the following code to generate C# Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/121405384-444d7300-c95d-11eb-959f-913020d3bf90.png" alt="C#" title="C#"/></code>
</div>

"""

If "HTML" is used then use the following code to generate HTML Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/192158954-f88b5814-d510-4564-b285-dff7d6400dad.png" alt="HTML" title="HTML"/></code>
</div>

"""

If "CSS" is used then use the following code to generate CSS Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183898674-75a4a1b1-f960-4ea9-abcb-637170a00a75.png" alt="CSS" title="CSS"/></code>
</div>

"""

If "php" is used then use the following code to generate php Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183570228-6a040b9f-3ddf-47a2-a201-743121dac664.png" alt="php" title="php"/></code>
</div>

"""


2. For "Tools" which are used as an IDE:

If "Visual Studio Code" is used then us the following code to generate VS code Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/192108891-d86b6220-e232-423a-bf5f-90903e6887c3.png" alt="Visual Studio Code" title="Visual Studio Code"/></code>
</div>

"""

If "Jupyter Notebook" is used then us the following code to generate Jupyter Notebook Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183914128-3fc88b4a-4ac1-40e6-9443-9a30182379b7.png" alt="Jupyter Notebook" title="Jupyter Notebook"/></code>
</div>

"""

3. For "Database" which are used to store Data:

If "Oracle" is used then us the following code to generate oracle Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/117208736-bdedc080-adf5-11eb-912f-61c7d43705f6.png" alt="Oracle" title="Oracle"/></code>
</div>

"""

If "MySQL" is used then us the following code to generate MySQL Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183896128-ec99105a-ec1a-4d85-b08b-1aa1620b2046.png" alt="MySQL" title="MySQL"/></code>
</div>

"""

If "mongoDB" is used then us the following code to generate mongoDB Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/182884177-d48a8579-2cd0-447a-b9a6-ffc7cb02560e.png" alt="mongoDB" title="mongoDB"/></code>
</div>

"""

4.  For "DevOps" which are used for development and deployment:


If "Docker" is used then us the following code to generate Docker Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png" alt="Docker" title="Docker"/></code>
</div>

"""

If "kubernetes" is used then us the following code to generate kubernetes Icon:


"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/182534006-037f08b5-8e7b-4e5f-96b6-5d2a5558fa85.png" alt="Kubernetes" title="Kubernetes"/></code>
</div>

"""

5. For "Cloud" which is used as a Cloud platform:

If "Microsoft Azure" is used then us the following code to generate Microsoft Azure Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183911544-95ad6ba7-09bf-4040-ac44-0adafedb9616.png" alt="Microsoft Azure" title="Microsoft Azure"/></code>
</div>

"""

If "AWS" is used then us the following code to generate AWS Icon:

"""

<div align="center">
	<code><img width="30" src="https://user-images.githubusercontent.com/25181517/183896132-54262f2e-6d98-41e3-8888-e40ab5a17326.png" alt="AWS" title="AWS"/></code>
</div>

"""

## Installation

Instructions on how to install and set up the project. For example:


1. Clone the repository

```sh
git clone https://github.com/yourusername/project-name.git
```

2. Navigate to the project directory
```sh
cd project-name
```
3. Install Dependencies from requirements.txt file
```sh
pip install -r requirements.txt
```

## Introduction
Brief Introduction about the project, what's it about, unique features regarding the project and define those unique features brifely.


## Data Acquisition

Define project's goal and which project repositories has been used as the input data.(project's gitbhub link)
## Result Analysis

Define different kind of metrics to evaluate the performance of the project, if exists. such as BLEU score, accuracy, recall, precision etc.

## License
This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details. Add the License with the follwoing link.

Example link addition:

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/ddobric/htmdotnet/blob/master/LICENSE)

## Real-life applications of the project
Define the real life use cases about the project and for more info refer to the Documentation folder and if necesseary refer specific documents. 

_For more examples, please refer to the [Documentation](https://github.com/your_github/IIRA)_
## References
Add specific references or biblography in the precise context. check for the referenceson the documents and add them here as a following manner.

Example:

[1]	J. Clerk Maxwell, A Treatise on Electricity and Magnetism, 3rd ed., vol. 2. Oxford: Clarendon, 1892, pp.68–73.

[2]	I. S. Jacobs and C. P. Bean, “Fine particles, thin films and exchange anisotropy,” in Magnetism, vol. III, G. T. Rado and H. Suhl, Eds. New York: Academic, 1963, pp. 271–350. 

etc...
####

To summarize your tasks again:
1. Learn the semantics of the project using the data structure.
2. Learn the patterns used in the Readme template.
3. Create a readme file using what you learned in 1. and 2.
4. Return the Markdown code of the readme file and nothing else. In \
particular, do not return any formatting information or other metadata.
