// DNC post-mortem - Model A + cohort×race hierarchical interaction
// Pre-reg §4 base + result_v1.0 §9 follow-up #3.
//
// Adds a 5×6 (cohort × race) interaction layer to Model A. Each
// (cohort, race) cell has its own random-effect deviation from the
// additive marginal sum, shared via a single sigma_cohort_race
// (half-normal(0, 0.5) — tighter than marginals because interaction
// is expected to be smaller).
//
// The marginal cohort_eff and race_eff still represent the average
// effect across the other dimension; cohort_race_eff[c, r] is the
// CELL-SPECIFIC departure from that additive sum.

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

  array[N] int<lower=0, upper=1> y;
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

  matrix[N_cohort, N_race] z_cohort_race;

  real<lower=0> sigma_race;
  real<lower=0> sigma_educ;
  real<lower=0> sigma_cohort;
  real<lower=0> sigma_gender;
  real<lower=0> sigma_region;
  real<lower=0> sigma_cohort_race;
}

transformed parameters {
  vector[N_race]   race_eff   = z_race   * sigma_race;
  vector[N_educ]   educ_eff   = z_educ   * sigma_educ;
  vector[N_cohort] cohort_eff = z_cohort * sigma_cohort;
  vector[N_gender] gender_eff = z_gender * sigma_gender;
  vector[N_region] region_eff = z_region * sigma_region;

  matrix[N_cohort, N_race] cohort_race_eff = z_cohort_race * sigma_cohort_race;
}

model {
  alpha     ~ normal(0, 2);
  beta_fund ~ normal(0, 1);

  sigma_race         ~ normal(0, 1);
  sigma_educ         ~ normal(0, 1);
  sigma_cohort       ~ normal(0, 1);
  sigma_gender       ~ normal(0, 1);
  sigma_region       ~ normal(0, 1);
  sigma_cohort_race  ~ normal(0, 0.5);   // tighter prior: interaction smaller than marginals

  z_race   ~ std_normal();
  z_educ   ~ std_normal();
  z_cohort ~ std_normal();
  z_gender ~ std_normal();
  z_region ~ std_normal();
  to_vector(z_cohort_race) ~ std_normal();

  vector[N] eta = alpha + X_fund * beta_fund
                + race_eff[race]
                + educ_eff[educ]
                + cohort_eff[cohort]
                + gender_eff[gender]
                + region_eff[region];
  for (n in 1:N) {
    eta[n] += cohort_race_eff[cohort[n], race[n]];
    target += weight[n] * bernoulli_logit_lpmf(y[n] | eta[n]);
  }
}
