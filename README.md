
# Validactylus

## Description

**Validactylus** is a Python command line tool to validate structure and format
of CSV data. The validation rules are specified in JSON Schema and
retrieved from a central repository.

## Table of Contents

- [Installation and usage](#installation-and-usage)
  <!---   [Data standards](#data-standards)
  -   [File naming nomenclature](#file-naming-nomenclature)
  -   [Reproducibility](#reproducibility)
  -->
- [Contributing](#contributing)
- [Authors](#authors)
- [License](#license)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)

## Installation and usage

### Installation from GitHub:

```
pip install git+https://github.com/eLTER-RI/validactylus.git
```

### Usage

run from command line

Windows:
```
> py -m validate_elter
```

Linux:
```
$ python path/to/validate_elter.py
```


#### Examples
`> py -m validate_elter testdata.csv -r data_mapping`


*trying to validate with a schema that won't be found in eLTER's central
shema store*:
```
> py -m validate_elter testdata.csv -r inexistent_schema

```
> `elter_validate: error: argument -r/--rules: invalid choice: 'this_schema_doesnt_exist' (choose from 'data_mapping', 'data_observation', 'event', 'license', 'mapping', 'method', 'reference', 'sample', 'station')`


### Getting help

#### For users
run `validate_elter.py` with the `-h` flag

#### For developers
see `/docs` or visit [GitHub page](https://elter-ri.github.io/validactylus/)

## Contributing

### Dependencies


### Coding standards

To maintain the quality and readability of our code, we follow certain
coding standards. Contributors are expected to adhere to these
guidelines when writing code for this project:

#### Style


#### Paradigm


<!-- general advice for contributors, include in README ?
&#10;### Tools for enforcing style
&#10;-   R packages to support styling (and other code checks) are
    [`lintr`](https://lintr.r-lib.org/) or
    [`styler`](https://styler.r-lib.org/). RStudio and other
    popular code editors also offer R-specific linting modes/plugins.
&#10;## Data standards
&#10;This project adheres to eLTER data standards. Please ensure all data
complies with these standards (*e. g. by using this package*)
    and is deposited appropriately in
[Zenodo](https://zenodo.org/communities/elter) or
[B2SHARE](https://b2share.eudat.eu/communities/LTER) repositories as per
eLTER community guidelines.
&#10;
&#10;## File naming nomenclature
&#10;To ensure clarity and ease of access for all contributors, please adhere
to the following file naming conventions:
&#10;-   Use descriptive names that reflect the content or purpose of the
    file.
-   Use underscores (\_) to separate different elements of R source file names
    (`awesome_function.R`) as well as to denote spaces within
    an element (`my_important_dataframe`)
-   Keep file names concise, avoiding unnecessary abbreviations while
    maintaining sufficient detail. 
    [Here's how to name R source files](https://r-pkgs.org/code.html#sec-code-organising)
&#10;
## Reproducibility
&#10;Ensure the reproducibility of your work by:
&#10;-   Providing detailed descriptions of methods and protocols in the
    documentation.
-   Including version-controlled source code for all scripts and
    analysis workflows.
-   Specifying versions and sources of external libraries and tools
    used.
-   Sharing raw data and processed results in accessible, referenced
    data repositories with clear metadata.
-   Documenting any deviations from the expected protocols.
&#10;## Contributing
&#10;The repository should have clear instructions on how to contribute to
the project. This should include different files with clear
instructions. To do so, add a folder named `.github` on the project
root. In this folder you should add the following files:
&#10;-   `CONTRIBUTING.md`
-   `CODE_OF_CONDUCT.md`
-   `PULL_REQUEST_TEMPLATE.md`
-   `ISSUE_TEMPLATE.md`
-   `BUG_REPORT.md`
-   `FEATURE_REQUEST.md`
&#10;
end general dev advice  -->

## Authors

|     Author      |                       Affiliation                       |                            ORCID                             |            e-mail            |
|:---------------:|:-------------------------------------------------------:|:------------------------------------------------------------:|:----------------------------:|
| Ivo Offenthaler | [Environment Agency Austria](https://ror.org/013vyke20) | [0000-0001-5793-6641](https://orcid.org/0000-0001-5793-6641) | <validiraptor-dev@proton.me> |

## License

- This project is licensed under the [EUPL License](https://eupl.eu/) -
  see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Development & maintenance funded through:

<p align="center">
<a href="https://elter-ri.eu/elter-ppp">
<img src="man/figures/eLTER-IMAGE-PPP_logo-v01.svg" alt="eLTER PLUS Logo" width="175" height="auto"/>
</a> <a href="https://elter-ri.eu/elter-plus">
<img src="man/figures/eLTER-IMAGE-PLUS_logo-v01.svg" width="175" height="auto"/>
</a> <a href="https://elter-ri.eu/elter-enrich">
<img src="man/figures/eLTER-IMAGE-EnRich_logo-v01.svg" alt="eLTER EnRich Logo" width="175" height="auto"/>
</a>
</p>
