
from lib.PythonSetup import *

def get_rand_number(size, min_value, max_value):
    range = max_value - min_value
    choice = np.random.random_sample(size = size)
    return min_value + range*choice

def get_dist_sample(size, dist_name, mu, sigma):
    dist = getattr(scipy.stats, dist_name)
    return dist(loc=mu, scale=sigma).rvs(size) if dist_name=='norm' else dist(s=sigma, loc=0, scale=np.exp(mu)).rvs(size)

def get_dist_pdf(x, dist_name, mu, sigma):
    dist = getattr(scipy.stats, dist_name)
    return dist(loc=mu, scale=sigma).pdf(x) if dist_name=='norm' else dist(s=sigma, loc=0, scale=np.exp(mu)).pdf(x)

def get_dist_logpdf(x, dist_name, mu, sigma):
    dist = getattr(scipy.stats, dist_name)
    return dist(loc=mu, scale=sigma).logpdf(x) if dist_name=='norm' else dist(s=sigma, loc=0, scale=np.exp(mu)).logpdf(x)

def get_dist_cdf(x, dist_name, mu, sigma):
    dist = getattr(scipy.stats, dist_name)
    return dist(loc=mu, scale=sigma).cdf(x) if dist_name=='norm' else dist(s=sigma, loc=0, scale=np.exp(mu)).cdf(x)

def crude_MC(num_of_samples, function):
    return 1./num_of_samples * np.sum(function)

def get_MC_samples(num_of_samples, mu, sigma):    
    samples = np.exp(multivariate_normal.rvs(mean=mu, cov=np.diag(np.square(sigma)), size=num_of_samples, random_state=None))   
    return samples

def get_MC_estimate(num_of_samples, function):         
    return 1./num_of_samples * np.sum(function)

def get_MC_variance(num_of_samples, function):         

    mean_of_sq = 1./num_of_samples * np.sum(np.square(function))
    sq_of_mean = (1./num_of_samples * np.sum(function))**2

    return (1./num_of_samples) * (mean_of_sq - sq_of_mean)

def get_MCMC_estimate(num_of_samples, num_of_vars, samples, function, mu, sigma):
    
    p = multivariate_normal.logpdf(np.log(samples), mean=mu, cov=np.diag(np.square(sigma))) - np.sum(np.log(samples), axis=1)
    q = np.log(sm.nonparametric.KDEMultivariate(samples, var_type='c'*num_of_vars).pdf())

    ln_of_estimate = np.log(function) + p - q

    return 1./np.sum(np.exp(p-q)) * np.sum(np.exp(ln_of_estimate))

def get_MCMC_variance(num_of_samples, num_of_vars, samples, function, mu, sigma):  
    
    p = multivariate_normal.logpdf(np.log(samples), mean=mu, cov=np.diag(np.square(sigma))) - np.sum(np.log(samples), axis=1)
    q = np.log(sm.nonparametric.KDEMultivariate(samples, var_type='c'*num_of_vars).pdf())
    
    estimate = np.sum(np.exp(np.log(function) + p - q))/np.sum(np.exp(p-q))
    
    nominator = np.sum(np.exp(2*p-2*q)*np.square(function-estimate))
    denominator = np.sum(np.exp(p-q))**2

    return nominator/denominator

def get_MCMC_IS_estimate(num_of_samples, num_of_vars, samples, function, mu, sigma, kde):
    
    p = multivariate_normal.logpdf(np.log(samples), mean=mu, cov=np.diag(np.square(sigma))) - np.sum(np.log(samples), axis=1)
    p = np.nan_to_num(p, nan=-1000)
#     q = kde.logpdf(samples.T)
    q = np.log(sm.nonparametric.KDEMultivariate(samples, var_type='c'*num_of_vars).pdf())
    
    ln_of_estimate = np.log(function) + p - q
    
    return 1./np.sum(np.exp(p-q)) * np.sum(np.exp(ln_of_estimate))

def get_MCMC_IS_variance(num_of_samples, num_of_vars, samples, function, mu, sigma, kde):  
    
    p = multivariate_normal.logpdf(np.log(samples), mean=mu, cov=np.diag(np.square(sigma))) - np.sum(np.log(samples), axis=1)
    p = np.nan_to_num(p, nan=-1000)
    q = kde.logpdf(samples.T)
    
    estimate = np.sum(np.exp(np.log(function) + p - q))/np.sum(np.exp(p-q))
    
    nominator = np.sum(np.exp(2*p-2*q)*np.square(function-estimate))
    denominator = np.sum(np.exp(p-q))**2

    return nominator/denominator

def get_KDE_samples(num_of_samples, kde):    
    n, d = kde.data.shape
    indices = np.random.randint(0, n, num_of_samples)
    cov = np.diag(kde.bw)**2
    means = kde.data[indices, :]
    norm = np.random.multivariate_normal(np.zeros(d), cov, num_of_samples)
    return np.transpose(means + norm)
