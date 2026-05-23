// DNC post-mortem - Model A (demographic baseline, pre-reg §4 + §7)
//
// Hierarchical demographic + cohort logistic on outcome y ∈ {0, 1}.
// Pre-reg §4: race × education × birth-cohort × gender × region.
// All hierarchical effects use non-centered parameterization (per
// [[feedback_non_centered_for_sparse_funnels]]).
//
// Fundamentals baseline (continuous): 2020 vote recall (one-hot encoded
// in X_fund), Cook PVI, state result margin, economic perception
// z-score, incumbency-direction binary.
//
// Used for both:
//   - vote-choice (binary Harris=1 / Trump=0 among major-party voters)
//   - per-issue (z-standardized issue position; modeled as Gaussian
//     outcome via the issue-version of this model, see model_a_issue.stan)

data {
  int<lower=1> N;
  int<lower=1> K_fund;             // # fundamentals columns
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
  vector<lower=0>[N] weight;       // survey weight (1 if unweighted)
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
}

transformed parameters {
  vector[N_race]   race_eff   = z_race   * sigma_race;
  vector[N_educ]   educ_eff   = z_educ   * sigma_educ;
  vector[N_cohort] cohort_eff = z_cohort * sigma_cohort;
  vector[N_gender] gender_eff = z_gender * sigma_gender;
  vector[N_region] region_eff = z_region * sigma_region;
}

model {
  // Priors
  alpha     ~ normal(0, 2);
  beta_fund ~ normal(0, 1);

  sigma_race   ~ normal(0, 1);
  sigma_educ   ~ normal(0, 1);
  sigma_cohort ~ normal(0, 1);
  sigma_gender ~ normal(0, 1);
  sigma_region ~ normal(0, 1);

  z_race   ~ std_normal();
  z_educ   ~ std_normal();
  z_cohort ~ std_normal();
  z_gender ~ std_normal();
  z_region ~ std_normal();

  // Weighted likelihood (weights = 1 for unweighted analyses)
  vector[N] eta = alpha + X_fund * beta_fund
                + race_eff[race]
                + educ_eff[educ]
                + cohort_eff[cohort]
                + gender_eff[gender]
                + region_eff[region];

  for (n in 1:N) {
    target += weight[n] * bernoulli_logit_lpmf(y[n] | eta[n]);
  }
}

generated quantities {
  vector[N] log_lik;
  {
    vector[N] eta = alpha + X_fund * beta_fund
                  + race_eff[race]
                  + educ_eff[educ]
                  + cohort_eff[cohort]
                  + gender_eff[gender]
                  + region_eff[region];
    for (n in 1:N) {
      log_lik[n] = bernoulli_logit_lpmf(y[n] | eta[n]);
    }
  }
}
