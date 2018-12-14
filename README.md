# Effect Estimator By Incident Interval Count(EEBIIC)

## Requirements

* Python3
* Libraries (automatically installed with pip)
    * Numpy
    * Pandas
    * Tabulate
    * Pystan

## How to use

### Install

```bash
git clone https://github.com/metagen/EEBIIC.git
cd EEBIIC
pip install .
```

It will take a while as stan models are compiled to C++.

### Pre-calculation

Before using eebiic, you have to calculate the event interval. See test files in /eebiic/tests/data/test_c2i.
These counts file can be converted and summarized to a single stacking table by

```bash
eebiic_c2i <Interval_path> <Count_path> <Testfood_path> <Placebo_path>
```

### Estimation

Estimate effect with interval count file by

```bash
eebiic_estimate <Output_path> <Interval_path>
```

In default, model number 5 will run. If you want to change your idea of the effect, please change the model by `-m` option.
We have candidates shown below.

| No. | Scale parameter | Shape parameter | Placebo effect | Test food effect | Prior distribution       |
|-----|-----------------|-----------------|----------------|------------------|--------------------------|
| 1   | individual      | shared          | individual     | individual       | -                        |
| 2   | individual      | shared          | shared         | shared           | -                        |
| 3   | shared          | shared          | shared         | shared           | -                        |
| 4   | individual      | individual      | individual     | individual       | -                        |
| 5   | individual      | individual      | individual     | individual       | half-normal distribution |
| 6   | individual      | individual      | shared         | shared           | half-normal distribution |
| 7   | individual      | individual      | individual     | shared           | half-normal distribution |
| 8   | individual      | individual      | shared         | individual       | half-normal distribution |
| 9   | individual      | individual      | shared         | -                | half-normal distribution |
| 10  | individual      | individual      | -              | shared           | half-normal distribution |


## Notice

* After estimated, please check whether Rhat become lower than 1.1. If not, MCMC sampling didn't convergent
* We recommend you to check n_eff is greater than 100.
* If you want to compare models, please use WAIC which will be printed after sampling.

## Citation

Nakamura Y., Suzuki S., Murakami S., Higashi K., Watarai N., Nishimoto Y., Umetsu J., Suzuki S., Ishii C., Ito Y., Mori Y., Kohno M., Yamada T., Fukuda S., Multi-omics analysis identified fecal biomarkers for bowel movement responders with enteric seamless capsules containing Bifidobacterium longum: a randomized controlled trial, submitting

## License

BSD 3-Clause
