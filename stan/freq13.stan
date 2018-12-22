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
    real<lower=0> shape[N] ;
    real gut_state_mu ;
    real<lower=0> gut_state_sigma ;
    real<lower=0> shape_sigma ;
}

transformed parameters {
    real lambda[I] ;
    for (i in 1:I){
        lambda[i] = exp(- gut_state[SubjectID[i]] / shape[SubjectID[i]]) ;
    }
}

model {
    for (i in 1:I){
        Interval[i] ~ weibull(shape[SubjectID[i]], lambda[i]) ;
    }
    for (n in 1:N){
        gut_state[n] ~ normal(gut_state_mu, gut_state_sigma) ;
        shape[n] ~ normal(0, shape_sigma) ;
    }
    gut_state_mu ~ uniform(0, 1000) ;
    gut_state_sigma ~ uniform(0, 1000) ;
    shape_sigma ~ uniform(0, 1000) ;
}
generated quantities {
    real log_lik[I] ;
    real lambda_normal[N] ;
    for (i in 1:I){
        log_lik[i] = weibull_lpdf(Interval[i] | shape[SubjectID[i]], lambda[i]) ;
    }
    for (n in 1:N){
        lambda_normal[n] = exp(- gut_state[n] / shape[n]) ;
    }
}
