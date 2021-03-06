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
    real beta[2] ;
    real<lower=0> shape ;
    real gut_state_mu ;
    real<lower=0> gut_state_sigma ;
}

transformed parameters {
    real gut_state_affected[I] ;
    real lambda[I] ;
    for (i in 1:I){
        gut_state_affected[i] = gut_state[SubjectID[i]] + beta[1] * Testfood[i] + beta[2] * Placebo[i] ;
        lambda[i] = exp(- gut_state_affected[i] / shape) ;
    }
}

model {
    for (i in 1:I){
        Interval[i] ~ weibull(shape, lambda[i]) ;
    }
    for (n in 1:N){
        gut_state[n] ~ normal(gut_state_mu, gut_state_sigma) ;
    }
    shape ~ uniform(0,1000) ;
    gut_state_mu ~ uniform(0, 1000) ;
    gut_state_sigma ~ uniform(0, 1000) ;
}
generated quantities {
    real log_lik[I] ;
    for (i in 1:I){
        log_lik[i] = weibull_lpdf(Interval[i] | shape, lambda[i]) ;
    }
}
