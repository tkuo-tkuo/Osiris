# Jupyter_Osiris

Jupyter_Osiris (Osiris) is a tool for programmers to analyze Jupyter Notebook files before releasement. We discovered that plentiful Jupyter Notebook files pushed on GitHub cannot reproduce anticipated outputs. Alternatively, even worse, some Jupyter Notebook files can even not be executed on different end devices.

Osiris aims to eliminate this problem. One can leverage Osiris to analyze their Jupyter Notebook files before releasement to the public, which can conclude potential reasons for causing non-reproducibility. By the assistance of Osiris, programmers can properly refine their Jupyter Notebook files and enhance reproducibility of Jupyter Notebook files. 

## Getting Started

These instructions will go through execution environments setup, usage, and unit tests for users to check functionalities of Osiris. 

### Prerequisites

Make sure both Conda and Pip installed. Install Conda via [the official website](https://www.anaconda.com/) or by pip. 

```
pip install conda 
```

### Setup 

Before the usage of Osiris, to cope with various python version and package requirements for Jupyter Notebook files. A setup.sh needs to be executed to deploy several Conda environments with several combinations between different versions python and ten selected packages. 

```
cd envs 
source ./setup.sh
```

Press yes during Conda environments installation if any. 
After executing setup.sh, Conda environments with 'Osiris_' prefix should be installed.
Execute the following command for verification. 

```
conda env list
```

display an image as a little demonstration 

### Running unit tests for Osiris 

There exist a folder called <b>tests</b> in the repository for testing functionalities of Osiris. Please navigate to the <b>tests</b> directory and run the <b>test.py</b> for unit tests. These unit tests will verify whether Osiris functions properly in various scenarios. 

```
cd tests
python3 test.py -v
```

## Usage 

intro for this section 

```
conda activate Osiris_default 
```

### Parameters 

description for parameters 

### Examples 

example 1 

```
source ./runOsiris ...
```

example 2

```
source ./runOsiris ...
```

and more 

```
source ./runOsiris ...
```

## Contributing

Skip
<!-- Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us. -->

## Versioning

Skip
<!-- We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). -->

## Authors

* **KUO, Tzu-yang** - *Implementation* - [GitHub page](https://github.com/KuoTzu-yang)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Why it's called Osiris? <br/>
Osiris is the god of the afterlife, the underworld, and rebirth in ancient Egyptian religion. Our tool aims to enable Jupyter Notebook files to be executable, more reproducible, giving these files rebirth on different machines. That is the inspiration why I would like to name our tool as Jupyter Osiris. 
* Hat tip to anyone whose code was used
* Inspiration
* etc

## Reference 

Skip
