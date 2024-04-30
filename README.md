
<img src='man/figures/eLTER-IMAGE-validiraptor.svg' width = '150px' style = 'display:block; margin-top:5em; clear:both !important' />

<br/>

# Validiraptor

![](https://img.shields.io/badge/license-EUPL--1.2-blue)
![](https://img.shields.io/badge/R-v4.3.3-blue)

## Description

**Validiraptor is an R package which provides a browser based UI to
validate data for conformance with a schema.** Instances are provided by
the user as flat CSV tables, schemas are retrieved from remote in JSON
schema notation.

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

### Installation from GitHub

This **R** package ist available from GitHub only. Use
{[remotes](https://cran.r-project.org/web/packages/remotes/index.html)}
or {[pacman](https://cran.r-project.org/web/packages/pacman/index.html)}
to install from the GitHub source:

      ## install {remotes} if necessary:
      if(!require("remotes")) install.packages("remotes")
      ## fetch and install {validiraptor}:
      remotes::install_github("eLTER-RI/validiraptor")

> On Windows, you need to download and install
> [Rtools](https://cran.r-project.org/bin/windows/Rtools/rtools43/rtools.html)
> to compile the source files retrieved from GitHub. Make sure to
> install the Rtools compatible with your R version (e. g. `RTools4.3`
> for R version 4.3).

After installation of the package, execute `validiraptor::run_app()` to
launch the web app.

### Getting help

#### For users

In the running app (hosted or launched locally with
`validiraptor::run_app()`), switch to the “demo” tab in the left sidebar
for a choice of sample data to validate.

#### For users and developers

Visit <https://elter-ri.github.io/validiraptor/> or execute
`validiraptor::run_site()` to browse the documentation

#### For developers

Consult inline comments for internal functions which are not exported
for use with `help()`

## Contributing

### Dependencies

- Dependencies on other R packages are declared in `DESCRIPTION` and
  resolved upon installation.
- Javascript dependencies are declared and included in `inst/app/www/js`

*To modify the javascript part of the validation functionality, change
the source `validate.src.js` first, then
[`browserify`](https://www.npmjs.com/package/browserify) the source to
get the bundled `validate.js`*

- R code is tested with {[testthat](https://testthat.r-lib.org/)}. The
  test scripts go into `tests/testthat/`.

### Coding standards

To maintain the quality and readability of our code, we follow certain
coding standards. Contributors are expected to adhere to these
guidelines when writing code for this project:

#### Style

- Our R code adheres to the [tidyverse style
  guide](https://style.tidyverse.org/). Key points include:
  - Name variables and functions in `snake_case` (except `camelCase` for
    IDs of Shiny UI elements)
  - Place spaces around all binary operators (=, +, -, \<-, etc.),
    except in function arguments.
  - Always assign `<-`, not `=`

#### Paradigm

- Please stick to R’s [functional
  approach](https://adv-r.hadley.nz/fp.html) and make liberal use of the
  native pipe operator `|>` to prevent scope mess and increase
  readability.

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
