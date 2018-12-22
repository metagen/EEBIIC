#!/usr/bin/env python
# vim:fileencoding=utf-8
# Author: Shinya Suzuki
# Created: 2017-05-24
import argparse
import numpy as np
import os
import pandas as pd
import pickle
from eebiic.utils import get_logger
from pkg_resources import resource_filename
from tabulate import tabulate


def argument_parse(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("output",
                        type=str,
                        help="File path of output")
    parser.add_argument("interval_matrix",
                        type=str,
                        help="File path of state matrix")
    parser.add_argument("-fod", "--fit_out_dest",
                        nargs="?",
                        default=None,
                        type=str,
                        help="File path of estimated result (default: None)")
    parser.add_argument("-lld", "--log_likelihood_dest",
                        nargs="?",
                        default=None,
                        type=str,
                        help="File path of estimated lig_lik (default: None)")
    parser.add_argument("-m", "--model_name",
                        nargs="?",
                        type=str,
                        default="freq5",
                        choices=[
                            "freq1",
                            "freq2",
                            "freq3",
                            "freq4",
                            "freq5",
                            "freq6",
                            "freq7",
                            "freq8",
                            "freq9",
                            "freq10",
                            "freq11",
                            "freq12",
                            "freq13"
                        ],
                        help="Model type (default: freq5)")
    parser.add_argument("-si", "--staniter",
                        nargs="?",
                        default=6000,
                        type=int,
                        help="Number of Stan iteration (default: 6000)")
    parser.add_argument("-sw", "--stanwarmup",
                        nargs="?",
                        default=1000,
                        type=int,
                        help="Number of Stan warm up (defaultL 1000)")
    parser.add_argument("-sc", "--stanchain",
                        nargs="?",
                        default=8,
                        type=int,
                        help="Number of stan chains (default: 8)")
    parser.add_argument("-st", "--stanthin",
                        nargs="?",
                        default=1,
                        type=int,
                        help="Number of Stan thin (default: 1)")
    parser.add_argument("-ss", "--stanseed",
                        nargs="?",
                        default=1234,
                        type=int,
                        help="Number of Stan seed (defaultt: 1234)")
    parser.add_argument("-j", "--n_jobs",
                        nargs="?",
                        default=-1,
                        type=int,
                        help="Number of CPU for sampling (defualt: -1, all)")
    args = parser.parse_args(argv)
    return vars(args)


def get_waic(log_lik: np.ndarray, t: str="bda3") -> float:
    if t == "bda3":
        # See (Gelman, et al., "BDA3", 2013) Page 174
        lppd = np.sum(np.log(np.mean(np.exp(log_lik), axis=0)))
        pwaic = np.sum(np.var(log_lik, axis=0))
        waic = -2.0 * lppd + 2.0 * pwaic
    elif t == "original":
        # See (Sumio Watanabe, 2010, JMLR) formula (4), (5), (6)
        T = - np.mean(np.log(np.mean(np.exp(log_lik), axis=0)))
        fV = np.mean(np.var(log_lik, axis=0))
        waic = T + fV
    return waic


def load_model(model_type: str):
    target_path = resource_filename(
        "eebiic",
        "stan_models/{0}.pkl".format(model_type)
    )
    with open(target_path, "rb") as f:
        model = pickle.load(f)
    return model


def save_fit(fit, fod: str):
    with open(fod, "wb") as f:
        pickle.dump(fit, f)


def save_log_lik(fit, lld: str):
    log_lik = fit.extract("log_lik")["log_lik"]
    np.savetxt(lld, log_lik, delimiter="\t")


def summarize_fit(fit):
    prob = [0.025, 0.05, 0.25, 0.5, 0.75, 0.95, 0.975]
    summary = fit.summary(probs=prob)
    summary_df = pd.DataFrame(summary["summary"],
                              index=summary["summary_rownames"],
                              columns=summary["summary_colnames"])
    return summary_df


def main(output, interval_matrix, fit_out_dest, log_likelihood_dest,
         model_name, staniter, stanwarmup, stanchain, stanthin, stanseed,
         n_jobs, logger):
    i_df = pd.read_csv(interval_matrix, sep="\t")
    I = len(i_df)
    N = i_df["subject"].unique().size
    SubjectID = i_df["subject"]
    Interval = i_df["interval"].values
    Placebo = i_df["placebo"].values
    Testfood = i_df["testfood"].values

    # Prepare data for stan
    stan_data = {
        "I": I,
        "N": N,
        "SubjectID": SubjectID,
        "Interval": Interval,
        "Placebo": Placebo,
        "Testfood": Testfood
    }
    # Concerning percentile

    # Load model
    model = load_model(model_name)

    # Start sampling by MCMC
    logger.info("Start MCMC sampling")
    fit = model.sampling(data=stan_data,
                         iter=staniter,
                         warmup=stanwarmup,
                         chains=stanchain,
                         seed=stanseed,
                         n_jobs=n_jobs)

    # Summarize MCMC result by dataframe
    summary_df = summarize_fit(fit)

    # Output summary table.
    if os.path.splitext(output) == ".md":
        with open(output, "w") as f:
            f.write(tabulate(summary_df,
                             list(summary_df.columns),
                             tablefmt="pipe"))
    else:
        summary_df.to_csv(output, sep="\t")
    logger.info("MCMC result summary is saved at {0}".format(output))

    # Compute WAIC
    log_lik = fit.extract("log_lik")["log_lik"]
    waic = get_waic(log_lik)
    logger.info("WAIC={0}".format(waic))

    if fit_out_dest is not None:
        logger.info("Saving MCMC all result to {0}".format(fit_out_dest))
        save_fit(fit, fit_out_dest)
    if log_likelihood_dest is not None:
        logger.info("Saving log likelifood to {0}".format(log_likelihood_dest))
        save_log_lik(fit, log_likelihood_dest)


def main_wrapper():
    main(logger=get_logger(__name__), **argument_parse())


if __name__ == '__main__':
    main_wrapper()
