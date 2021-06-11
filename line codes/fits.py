
import pandas as pd,numpy as np, matplotlib.pyplot as plt,os,glob
import peakutils #baselining library
from matplotlib.ticker import MultipleLocator
from scipy.optimize import curve_fit
from pathlib import *
#import mplcursors
from lmfit import Parameters, minimize
from scipy import stats


def new_plot_LIG(d1,d2,d1_,d2_,e,line_number):
   
  
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().run_line_magic('pylab', 'inline')
    get_ipython().run_line_magic('matplotlib', 'inline')
    
    
    d1['I'] = d1['I']-d1_['I']
    base1 = peakutils.baseline(d1['I'], 1)
    d1['I_base']= d1['I']-base1
    d1 = d1[(d1['W']>1220) & (d1['W']<1750)]

    d2['I'] = d2['I']-d2_['I']
    d2 = d2[(d2['W']>2550) & (d2['W']<2850)]
    
    d2= d2[(np.abs(stats.zscore(d2))<3).all(axis=1)]
    base2 = peakutils.baseline(d2['I'], 1)
    d2['I_base'] = d2['I']-base2
    
    

    def PseudoVoigtFunction(WavNr, Pos, Amp, GammaL, FracL):
        SigmaG = GammaL / np.sqrt(2*np.log(2)) # Calculate the sigma parameter  for the Gaussian distribution from GammaL (coupled in Pseudo-Voigt)
        LorentzPart = Amp * (GammaL**2 / ((WavNr - Pos)**2 + GammaL**2)) # Lorentzian distribution
        GaussPart = Amp * np.exp( -((WavNr - Pos)/SigmaG)**2) # Gaussian distribution
        Fit = FracL * LorentzPart + (1 - FracL) * GaussPart # Linear combination of the two parts (or distributions)
        return Fit

    def one_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a3 = pars['a3'].value
        c3 = pars['c3'].value
        s3 = pars['s3'].value
        f3 = pars['f3'].value

        peak1 = PseudoVoigtFunction(x.astype(float),c3, a3, s3, f3)

        model =  peak1  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated

    def three_pv(pars, x, data=None, eps=None): #Function definition
        # unpack parameters, extract .value attribute for each parameter
        a1 = pars['a1'].value
        c1 = pars['c1'].value
        s1 = pars['s1'].value
        f1 = pars['f1'].value
        
        a4 = pars['a4'].value
        c4 = pars['c4'].value
        s4 = pars['s4'].value
        f4 = pars['f4'].value
        
        a2 = pars['a2'].value
        c2 = pars['c2'].value
        s2 = pars['s2'].value
        f2 = pars['f2'].value
        

        peak1 = PseudoVoigtFunction(x.astype(float), c1, a1, s1, f1)
        peak3 = PseudoVoigtFunction(x.astype(float), c4, a4, s4, f4)
        peak2 = PseudoVoigtFunction(x.astype(float), c2, a2, s2, f2)

        model =  peak1 + peak3 + peak2  # The global model is the sum of the Gaussian peaks

        if data is None: # if we don't have data, the function only returns the direct calculation
            return model, peak1, peak3, peak2
        if eps is None: # without errors, no ponderation
            return (model - data)
        return (model - data)/eps # with errors, the difference is ponderated


    ps1 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps1.add_many(('a1',    1 ,   True,     0, None,  None),
                 ('c1',   1350,   True,  1330, 1370,  None),
                 ('s1',     20,   True,    10,   200,  None),  # 200 so that we get proper fit width of unpatterned peak 
                 ('f1',    0.5,   True,  0, 1,  None),
                 ('a4',    1 ,   True,     0, None,  None), # peak middle of GD
                 ('c4',   1500,   True,  1480, 1520,  None),
                 ('s4',     20,   True,    10,   200,  None),  
                 ('f4',    0.5,   True,  0, 1,  None),
                 ('a2',      1,   True,     0, None,  None),
                 ('c2',    1600,   True, 1560,  1640,  None),
                 ('s2',     20,   True,    10,   200,  None),
                 ('f2',    0.5,   True,  0, 1,  None))

    ps2 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps2.add_many(('a3',      1,   True,     0, None,  None),
                 ('c3',    2700,   True, 2650,  2750,  None),
                 ('s3',     20,   True,    10,   200,  None),
                 ('f3',    0.5,   True,  0, 1,  None))



    x = d1['W']
    y = d1['I_base']
    out = minimize(three_pv, ps1, method = 'leastsq', args=(x, y))

    x2 = d2['W']
    y2 = d2['I_base']
    out2 = minimize(one_pv, ps2, method = 'leastsq', args=(x2, y2))

    f, (ax,ax2)=plt.subplots(1,2,sharey=True, gridspec_kw = {'width_ratios':[2.5, 1]})
    f.subplots_adjust(wspace=0.1)

    ax.xaxis.set_major_locator(MultipleLocator(200))
    ax2.xaxis.set_major_locator(MultipleLocator(200))

    ax.set_yticklabels([])

    ax.plot(x,y,'-',label='measured',)
    ax.plot(x,three_pv(out.params, x)[0],label='fit')
    ax.plot(x,three_pv(out.params, x)[1],label='fit')
    ax.plot(x,three_pv(out.params, x)[2],label='fit')
    ax.plot(x,three_pv(out.params, x)[3],label='fit')
#     ax.plot(x,four_pv(out.params, x)[4],label='fit')
    ax2.plot(x2,y2,'-')
    ax2.plot(x2,one_pv(out2.params, x2)[0])

    f.text(0.05, 0.5, 'Intensity [a.u.]', va='center', rotation='vertical', fontsize=16)
    f.text(0.5, 0.01, 'Raman shift [cm$^{-1}$]', ha='center', rotation='horizontal',fontsize=16)

    # hide the spines between ax and ax2
    ax.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax.yaxis.tick_left()
    # ax.tick_params(labelright='off')  # don't put tick labels at the top
    ax2.yaxis.tick_right()
    # ax.yaxis.label('test')

    d = .02  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)        # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, + d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((- d, + d), (- d, + d), **kwargs)  # bottom-left diagonal
    ax2.plot((- d, + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # ax.legend(loc='upper right')
#     plt.savefig(p/'Raman_raw_111.png', format='png', dpi=300)
    #plt.show()
    cc="Line "+str(line_number)+" Point number " + str(e)
    mm=cc+".png"
    plt.savefig(mm,dpi=200)
    df1 = pd.DataFrame({key: [par.value] for key, par in out.params.items()})
    df2 = pd.DataFrame({key: [par.value] for key, par in out2.params.items()})

    df = pd.concat([df1,df2],axis=1)

    if df['s1'].values > 300:
        df[['a1','c1','s1','f1']] = 0

    if df['s2'].values > 120:
        df[['a2','c2','s2','f2']] = 0

    if df['s3'].values > 120:
        df[['a3','c3','s3','f3']] = 0
        

    df.columns= ['D','PD','WD','FD','D1','PD1','WD1','FD1','G','PG','WG','FG','2D','P2D','W2D','F2D']
    df['GD']=df['G']/df['D']
    df['2DG']=df['2D']/df['G']
    if np.mean(d1[d1['W']<1255]['I_base']) > 0.7*np.mean(d1[(d1['W']>1340) & (d1['W']<1350)]['I_base'])        or np.mean(d1[(d1['W']>1400) & (d1['W']<1550)]['I_base']) > 0.7*np.mean(d1[(d1['W']>1340) & (d1['W']<1350)]['I_base']):
        print("patterning not done")

    se=[df['D'].values[0],df['PD'].values[0],df['WD'].values[0],df['FD'].values[0],df['D1'].values[0],        df['PD1'].values[0],df['WD1'].values[0],df['FD1'].values[0],df['G'].values[0],       df['PG'].values[0],df['WG'].values[0],df['FG'].values[0],df['2D'].values[0],        df['P2D'].values[0],df['W2D'].values[0],df['F2D'].values[0]]
    
    return df['G'],df['D']




