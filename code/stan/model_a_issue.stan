// DNC post-mortem - Model A (issue version, Gaussian outcome on z-scores)
//
// Same hierarchical demographic + cohort structure as model_a.stan
// but outcome is a continuous z-standardized issue position (not vote).
//
// Used for per-issue analysis on each substrate where the issue is present.

data {
  int<lower=1> N;
  int<lower=1> K_fund;
  matrix[N, K_fund] X_fund;

  int<lower=1> N_race;
  int<lower=1> N_educ;
  int<lower=1> N_cohort;
  int<lower=1> N_gender;
  int<lower=1> N_region;

  array[N] int<lower=1, upper=N_race> race;
  array[N] int<lower=1, upper=N_educ> educ;
  array[N] int<lower=1, upper=N_cohort> cohort;
  array[N] int<lower=1, upper=N_gender> gender;
  array[N] int<lower=1, upper=N_region> region;

  vector[N] y;                   // z-standardized issue position
  vector<lower=0>[N] weight;
}

parameters {
  real alpha;
  vector[K_fund] beta_fund;

  vector[N_race]   z_race;
  vector[N_educ]   z_educ;
  vector[N_cohort] z_cohort;
  vector[N_gender] z_gender;
  vector[N_region] z_region;

  real<lower=0> sigma_race;
  real<lower=0> sigma_educ;
  real<lower=0> sigma_cohort;
  real<lower=0> sigma_gender;
  real<lower=0> sigma_region;
  real<lower=0> sigma_y;         // residual SD
}

transformed parameters {
  vector[N_race]   race_eff   = z_race   * sigma_race;
  vector[N_educ]   educ_eff   = z_educ   * sigma_educ;
  vector[N_cohort] cohort_eff = z_cohort * sigma_cohort;
  vector[N_gender] gender_eff = z_gender * sigma_gender;
  vector[N_region] region_eff = z_region * sigma_region;
}

model {
  alpha     ~ normal(0, 1);
  beta_fund ~ normal(0, 1);

  sigma_race   ~ normal(0, 1);
  sigma_educ   ~ normal(0, 1);
  sigma_cohort ~ normal(0, 1);
  sigma_gender ~ normal(0, 1);
  sigma_region ~ normal(0, 1);
  sigma_y      ~ normal(0, 1);

  z_race   ~ std_normal();
  z_educ   ~ std_normal();
  z_cohort ~ std_normal();
  z_gender ~ std_normal();
  z_region ~ std_normal();

  vector[N] mu = alpha + X_fund * beta_fund
               + race_eff[race]
               + educ_eff[educ]
               + cohort_eff[cohort]
               + gender_eff[gender]
               + region_eff[region];

  for (n in 1:N) {
    target += weight[n] * normal_lpdf(y[n] | mu[n], sigma_y);
  }
}

generated quantities {
  vector[N] log_lik;
  {
    vector[N] mu = alpha + X_fund * beta_fund
                 + race_eff[race]
                 + educ_eff[educ]
                 + cohort_eff[cohort]
                 + gender_eff[gender]
                 + region_eff[region];
    for (n in 1:N) {
      log_lik[n] = normal_lpdf(y[n] | mu[n], sigma_y);
    }
  }
}
