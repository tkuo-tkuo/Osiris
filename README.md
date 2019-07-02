# Jupyter_Osiris

Jupyter_Osiris (Osiris) is a tool for programmers to analyze Jupyter Notebook files before releasement. We discovered that plentiful Jupyter Notebook files pushed on GitHub cannot reproduce anticipated outputs. Alternatively, even worse, some Jupyter Notebook files can even not be executed on different end devices.

Osiris aims to eliminate this problem. One can leverage Osiris to analyze their Jupyter Notebook files before releasement to the public, which can conclude potential reasons for causing non-reproducibility. By the assistance of Osiris, programmers can properly refine their Jupyter Notebook files and enhance reproducibility of Jupyter Notebook files. 

## Getting Started

These instructions will help you complete setup, deployment, and testing. In addition, a quick tutorial for getting familiar with Osiris. 

### Prerequisites

Make sure you have conda installed on your local machine. You can access [the official website](https://www.anaconda.com/) or simply by pip. 

```
pip install conda 
```

By activating the default environment, base, in conda. Users should have both <b>nbconvert</b> and <b>nbformat</b> installed in the <b>base</b> environment. These two packages should be installed for manipulation and analyses of Jupyter Notebook files. 

```
conda activate base  
```

User can also manually install <b>nbconvert</b> and <b>nbformat</b> by pip. 

### Setup 

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

There exist a folder called <b>tests</b> in the repository for testing functionalities of Osiris. Please navigate to the <b>tests</b> directory and run the <b>test.py</b> for unit tests. Note that it only contains several essential unit tests, it is highly recommended to include more unit tests. 

```
cd tests
python3 test.py -v
```

## Deployment

Add additional notes about how to deploy this on a live system

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
