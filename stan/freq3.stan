data {
    int I ;
    int N ; // Number of subjects
    int<lower=1, upper=N> SubjectID[I] ;
    real<lower=0> Interval[I] ;
    int<lower=0, upper=1> Placebo[I] ;
    int<lower=0, upper=1> Testfood[I] ;
}

parameters {
    real gut_state ;
    real beta[2] ;
    real<lower=0> shape ;
}

transformed parameters {
    real gut_state_affected[I] ;
    real lambda[I] ;
    for (i in 1:I){
        gut_state_affected[i] = gut_state + beta[1] * Testfood[i] + beta[2] * Placebo[i] ;
        lambda[i] = exp(- gut_state_affected[i] / shape) ;
    }
}

model {
    for (i in 1:I){
        Interval[i] ~ weibull(shape, lambda[i]) ;
    }
    shape ~ uniform(0,1000) ;
}
generated quantities {
    real log_lik[I] ;
    real p_beta1_greater_0 ;
    real p_beta2_greater_0 ;
    real p_beta1_greater_beta2 ;

    for (i in 1:I){
        log_lik[i] = weibull_lpdf(Interval[i] | shape, lambda[i]) ;
    }
    p_beta1_greater_0 = beta[1] > 0 ? 1 : 0 ;
    p_beta2_greater_0 = beta[2] > 0 ? 1 : 0 ;
    p_beta1_greater_beta2 = beta[1] > beta[2] ? 1 : 0 ;
}
