# Effect Estimator By Incident Interval Count(EEBIIC)

EEBIIC(pronounced by eɪ-bi-si) is an effect estimator by inident inteval counts, using bayesian weibull regression based on GLM.

## Requirements

* Python3 (≥ 3.4, checked by 3.6.5)
* Libraries (automatically installed with pip)
    * Numpy
    * Pandas
    * Tabulate
    * Pystan (≤2.17.1 because of index style modification)

## How to use

### Install

```bash
git clone https://github.com/metagen/EEBIIC.git
cd EEBIIC
pip install .
```

It will take a while as stan models are compiled to C++.

### Pre-calculation

Before using eebiic, you have to calculate the event interval if you only have count data ([tidy data format](https://www.jstatsoft.org/article/view/v059i10)). See test files in /eebiic/tests/data/test_c2i.
These counts file can be converted and summarized to a single stacking table by

```bash
eebiic_c2i <Output_path=Interval_path> <Count_path> <Testfood_path> <Placebo_path>
```

Please refer to the [test file](https://github.com/metagen/EEBIIC/tree/master/eebiic/tests/data/test_c2i) for the format of input files.

### Estimation

Estimate effect with interval count file by

```bash
eebiic_estimate <Output_path> <Interval_path>
```

In default, model number 5 will run. If you want to change your idea of the effect, please change the model by `-m` option.
We have candidates shown below.

| No. | Effect of diet     | Scale parameter | Shape parameter | Placebo effect                         | Test food effect | Prior distribution       |
|-----|--------------------|-----------------|-----------------|----------------------------------------|------------------|--------------------------|
| 1   | To scale parameter | individual      | shared          | individual                             | individual       | -                        |
| 2   | To scale parameter | individual      | shared          | shared                                 | shared           | -                        |
| 3   | To scale parameter | shared          | shared          | shared                                 | shared           | -                        |
| 4   | To scale parameter | individual      | individual      | individual                             | individual       | -                        |
| 5   | To scale parameter | individual      | individual      | individual                             | individual       | half-normal distribution |
| 6   | To scale parameter | individual      | individual      | shared                                 | shared           | half-normal distribution |
| 7   | To scale parameter | individual      | individual      | individual                             | shared           | half-normal distribution |
| 8   | To scale parameter | individual      | individual      | shared                                 | individual       | half-normal distribution |
| 9   | To scale parameter | individual      | individual      | shared                                 | -                | half-normal distribution |
| 10  | To scale parameter | individual      | individual      | -                                      | shared           | half-normal distribution |
| 11  | To shape parameter | individual      | individual      | individual                             | individual       | half-normal distribution |
| 12  | To scale parameter | individual      | individual      | individual(Only in placebo food terms) | individual       | half-normal distribution |
| 13  | To scale parameter | individual      | individual      | -                                      | -                | half-normal distribution |

Here is a head part of output file of model 5. As this is a summary table of posterior distribution.

* Columns
    * mean: mean of posterior distribution sampled for the model by MCMC algorithm
    * se_mean sd: standard error of mean
    * sd: standard deviation of posterior distribution
    * 2.5, 5, 25, 50, 75, 95, 97.5%: quantile of posterior distribution
    * n_eff: effective sampel size
    * Rhat: Rhat value to determine the convergence
* Row
    * gut_state: scale parameter of weibull distribution in normal state
    * shape: shape parameter of weibull distribution
    * beta[i,j]: subject i's intervention effect for test food(j=0) or placebo(j=1)
    * gut_state_mu: mean parameter of posterior normal distribution of scale parameter
    * gut_state_sigma: scale parameter of posterior normal distribution of scale parameter
    * beta_sigma[j]: scale parameter of posterior normal distribution of intervention effect for test food(j=0) or placebo(j=1)

```
        mean    se_mean sd      2.5%    5%      25%     50%     75%     95%     97.5%   n_eff   Rhat
gut_state[0]    -4.332323922821513      0.08838509781942684     1.2054120233672116      -6.898597698973268      -6.390515824635212      -5.08772992240606       -4.259272622465383      -3.475084464643905
      -2.542108525419354      -2.2752464242033543     186.0   1.0260160438672548
```



## Notice

* After estimated, please check whether Rhat become lower than 1.1. If not, MCMC sampling didn't convergent
* We recommend you to check n_eff is greater than 100.
* If you want to compare models, please use WAIC which will be printed after sampling.

## Citation

Nakamura Y., Suzuki S., Murakami S., Higashi K., Watarai N., Nishimoto Y., Umetsu J., Suzuki S., Ishii C., Ito Y., Mori Y., Kohno M., Yamada T., Fukuda S., Multi-omics analysis identified fecal biomarkers for bowel movement responders with enteric seamless capsules containing Bifidobacterium longum: a randomized controlled trial, submitting

## License

BSD 3-Clause
