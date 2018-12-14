data {
    int I ;
    int N ; // Number of subjects
    int<lower=1, upper=N> SubjectID[I] ;
    real<lower=0> Interval[I] ;
    int<lower=0, upper=1> Placebo[I] ;
    int<lower=0, upper=1> Testfood[I] ;
}

parameters {
    real gut_state[N] ;
    real beta[N, 2] ;
    real<lower=0> shape[N] ;
    real gut_state_mu ;
    real<lower=0> gut_state_sigma ;
    real<lower=0> shape_sigma ;
    real beta_sigma[2] ;
}

transformed parameters {
    real gut_state_affected[I] ;
    real lambda[I] ;
    for (i in 1:I){
        gut_state_affected[i] = gut_state[SubjectID[i]] + beta[SubjectID[i], 1] * Testfood[i] + beta[SubjectID[i], 2] * Placebo[i] ;
        lambda[i] = exp(- gut_state_affected[i] / shape[SubjectID[i]]) ;
    }
}

model {
    for (i in 1:I){
        Interval[i] ~ weibull(shape[SubjectID[i]], lambda[i]) ;
    }
    for (n in 1:N){
        for (i in 1:2){
            beta[n, i] ~ normal(0, beta_sigma[i]) ;
        }
        gut_state[n] ~ normal(gut_state_mu, gut_state_sigma) ;
        shape[n] ~ normal(0, shape_sigma) ;
    }
    gut_state_mu ~ uniform(0, 1000) ;
    gut_state_sigma ~ uniform(0, 1000) ;
    shape_sigma ~ uniform(0, 1000) ;
    beta_sigma[1] ~ uniform(0, 1000) ;
    beta_sigma[2] ~ uniform(0, 1000) ;
}
generated quantities {
    real log_lik[I] ;
    real lambda_normal[N] ;
    real p_beta1_greater_0[N] ; // Probability that beta[1] is greater than zero.
    real p_beta2_greater_0[N] ; // Probability that beta[2] is greater than zero.
    real p_beta1_greater_beta2[N] ; // Probability that beta[1] is greater than beta[2]
    real p_beta1x_greater_beta1y[N, N] ; // Probability that beta[1] of subject x is greater than that of subject y.
    real p_beta2x_greater_beta2y[N, N] ; // Probability that beta[2] of subject x is greater than that of subject y.
    for (i in 1:I){
        log_lik[i] = weibull_lpdf(Interval[i] | shape[SubjectID[i]], lambda[i]) ;
    }
    for (n in 1:N){
        lambda_normal[n] = exp(- gut_state[n] / shape[n]) ;
        p_beta1_greater_0[n] = beta[n, 1] > 0 ? 1 : 0 ;
        p_beta2_greater_0[n] = beta[n, 2] > 0 ? 1 : 0 ;
        p_beta1_greater_beta2[n] = beta[n, 1] > beta[n, 2] ? 1 : 0 ;
        for (m in 1:N){
            p_beta1x_greater_beta1y[n, m] = beta[n, 1] > beta[m, 1] ? 1 : 0 ;
            p_beta2x_greater_beta2y[n, m] = beta[n, 2] > beta[m, 2] ? 1 : 0 ;
        }
    }
}
