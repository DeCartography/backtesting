
# backtesting, QF v.s. Plural QF

This repository contains a Python tool for analyzing grant contributions using Quadratic Funding (QF) and a Pluralistic version of Quadratic Funding (PluralQF).

## Description

The tool performs an analysis to determine the distribution of funds to various projects based on individual contributions. compare with Quadratic Funding(QF) and Plural QF

[![Image from Gyazo](https://i.gyazo.com/e4048bfc5e4ed67e49f3ca4ab5fc96b0.png)](https://gyazo.com/e4048bfc5e4ed67e49f3ca4ab5fc96b0)

https://docs.google.com/spreadsheets/d/1BRlrpXzhKBZY2z_YDnvW30nDLhhKG9c86JWmgIBwLDw/edit?usp=sharing

## Files

- `edit_GR03_contributions.csv`: This file is an enhanced version of `GR03_contributions.csv`, originally available at [https://fddhub.io/](https://fddhub.io/) (link currently inactive). The enhancement includes the addition of project titles to the contributions data.

- `clustered.txt`: Contains clustered participant data from GR3. The data clustering was performed using the DeCartography tool, based on the crowd-workers input.

## Usage

1. Ensure that `edit_GR03_contributions.csv` and `clustered.txt` are placed in the root directory of the project.
2. Run the script with Python:

   ```shell
   python compare.py
   ```

The script will output the results of the QF and PluralQF analysis to the console.

## Requirements

- Python 3.8 or higher
- pandas
- numpy (optional for enhancements)

## Contributing

Feel free to fork this repository, and submit pull requests with any enhancements.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more information.

