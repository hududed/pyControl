#!/usr/bin/env python
# coding: utf-8

# In[1]:


def ration(m1, m2, counter):
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().run_line_magic('pylab', 'inline')

    from matplotlib.ticker import MultipleLocator
    get_ipython().run_line_magic('reload_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')
    get_ipython().run_line_magic('pylab', 'inline')
    import sys
    from lmfit import Parameters, minimize
    import pandas as pd  # python data manipulation and analysis library
    # Library with large collection of high-level mathematical functions to operate on arrays
    import numpy as np
    import matplotlib.pyplot as plt  # python plotting library
    import peakutils  # baselining library

    import os
    import glob
    import csv
 # Library with operating system dependent functionality. Example: Reading data from files on the computer
    bg1 = pd.read_csv("background1D.csv")
    bg2 = pd.read_csv("background2D.csv")
#     fn1 =pd.read_csv("foreground1D.csv")
#     fn2 = pd.read_csv("foreground2D.csv")
    fn1 = pd.read_csv("Point "+str(counter)+" foreground1D.csv")
    fn2 = pd.read_csv("Point "+str(counter)+" foreground2D.csv")

    # d1 = pd.read_csv(fn1)
    d1 = fn1
    # d1_ = pd.read_csv(bg1)
    d1_ = bg1
    d1['I'] = d1['I']-d1_['I']
    base1 = peakutils.baseline(d1['I'], 1)
    d1['I_base'] = d1['I']-base1
    d1 = d1[(d1['W'] > 1250) & (d1['W'] < 1750)]

    # d2 = pd.read_csv(fn2)
    d2 = fn2
    # d2_ = pd.read_csv(bg2)
    d2_ = bg2
    d2['I'] = d2['I']-d2_['I']
    base2 = peakutils.baseline(d2['I'], 1)
    d2['I_base'] = d2['I']-base2
    d2 = d2[(d2['W'] > 2600) & (d2['W'] < 2850)]

    def PseudoVoigtFunction(WavNr, Pos, Amp, GammaL, FracL):
        # Calculate the sigma parameter  for the Gaussian distribution from GammaL (coupled in Pseudo-Voigt)
        SigmaG = GammaL / np.sqrt(2*np.log(2))
        # Lorentzian distribution
        LorentzPart = Amp * (GammaL**2 / ((WavNr - Pos)**2 + GammaL**2))
        # Gaussian distribution
        GaussPart = Amp * np.exp(-((WavNr - Pos)/SigmaG)**2)
        # Linear combination of the two parts (or distributions)
        Fit = FracL * LorentzPart + (1 - FracL) * GaussPart
        return Fit

    def one_pv(pars, x, data=None, eps=None):  # Function definition
        # unpack parameters, extract .value attribute for each parameter
        a3 = pars['a3'].value
        c3 = pars['c3'].value
        s3 = pars['s3'].value
        f3 = pars['f3'].value

        peak1 = PseudoVoigtFunction(x.astype(float), c3, a3, s3, f3)

        model = peak1  # The global model is the sum of the Gaussian peaks

        if data is None:  # if we don't have data, the function only returns the direct calculation
            return model, peak1
        if eps is None:  # without errors, no ponderation
            return (model - data)
        return (model - data)/eps  # with errors, the difference is ponderated

    def two_pv(pars, x, data=None, eps=None):  # Function definition
        # unpack parameters, extract .value attribute for each parameter
        a1 = pars['a1'].value
        c1 = pars['c1'].value
        s1 = pars['s1'].value
        f1 = pars['f1'].value

        a2 = pars['a2'].value
        c2 = pars['c2'].value
        s2 = pars['s2'].value
        f2 = pars['f2'].value

        peak1 = PseudoVoigtFunction(x.astype(float), c1, a1, s1, f1)
        peak2 = PseudoVoigtFunction(x.astype(float), c2, a2, s2, f2)

        model = peak1 + peak2  # The global model is the sum of the Gaussian peaks

        if data is None:  # if we don't have data, the function only returns the direct calculation
            return model, peak1, peak2
        if eps is None:  # without errors, no ponderation
            return (model - data)
        return (model - data)/eps  # with errors, the difference is ponderated

    ps1 = Parameters()

    #            (Name,  Value,  Vary,   Min,  Max,  Expr)
    ps1.add_many(('a1',    1,   True,     0, None,  None),
                 ('c1',   1350,   True,  1330, 1370,  None),
                 # 200 so that we get proper fit width of unpatterned peak
                 ('s1',     20,   True,    10,   200,  None),
                 ('f1',    0.5,   True,  0, 1,  None),
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
    out = minimize(two_pv, ps1, method='leastsq', args=(x, y))

    x2 = d2['W']
    y2 = d2['I_base']
    out2 = minimize(one_pv, ps2, method='leastsq', args=(x2, y2))
    #f, (ax,ax2)=plt.subplots(1,2,sharey=True, gridspec_kw = {'width_ratios':[2.5, 1]})
    f, (ax, ax2) = plt.subplots(1, 2, sharey=True,
                                gridspec_kw={'width_ratios': [2.5, 1]})
    f.subplots_adjust(wspace=0.1)

    ax.xaxis.set_major_locator(MultipleLocator(200))
    ax2.xaxis.set_major_locator(MultipleLocator(200))

    ax.set_yticklabels([])

    ax.plot(x, y, '-', label='measured',)
    ax.plot(x, two_pv(out.params, x)[0], label='fit')
    ax2.plot(x2, y2, '-')
    ax2.plot(x2, one_pv(out2.params, x2)[0])

    f.text(0.05, 0.5, 'Intensity [a.u.]',
           va='center', rotation='vertical', fontsize=16)
    f.text(0.5, 0.01, 'Raman shift [cm$^{-1}$]',
           ha='center', rotation='horizontal', fontsize=16)

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
    ax.plot((1 - d, 1 + d), (1 - d, 1 + d), **
            kwargs)        # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, + d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((- d, + d), (- d, + d), **kwargs)  # bottom-left diagonal
    ax2.plot((- d, + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # ax.legend(loc='upper right')
    # plt.savefig(p/'Raman_raw_111.png', format='png', dpi=300)
    # plt.show()
    plt.figure(figsize=(10, 7))
    plt.plot(x, y)

    plt.plot(x, two_pv(out.params, x)[0])
    plt.xlabel('Raman shift [cm$^{-1}$]')
    plt.ylabel('Intensity [a.u.]')
    i = counter

    # plt.plot(x2,y2)
    import os
    os.chdir(r'C:\Users\labuser\old sample spectra column 48 to 97')
    #if i==0:os.mkdir('figures of the experiments')
    os.chdir('figures of the experiments')
    plt.savefig('Graphene spot ' + str(i) + '.png')
    plt.clf()

    plt.figure(figsize=(10, 7))
    plt.plot(x2, y2)

    plt.plot(x2, one_pv(out2.params, x2)[0])
    plt.xlabel('Raman shift [cm$^{-1}$]')
    plt.ylabel('Intensity [a.u.]')
    i = counter
    # plt.plot(x2,y2)
    plt.savefig('Graphene 2D spot ' + str(i) + '.png')
    plt.clf()
    os.chdir(r'C:\Users\labuser\old sample spectra column 48 to 97')

    df1 = pd.DataFrame({key: [par.value] for key, par in out.params.items()})
    df2 = pd.DataFrame({key: [par.value] for key, par in out2.params.items()})

    df = pd.concat([df1, df2], axis=1)

    if df['s1'].values > 300:
        df[['a1', 'c1', 's1', 'f1']] = 0

    if df['s2'].values > 120:
        df[['a2', 'c2', 's2', 'f2']] = 0

    if df['s3'].values > 120:
        df[['a3', 'c3', 's3', 'f3']] = 0

    df.columns = ['D', 'PD', 'WD', 'FD', 'G', 'PG',
                  'WG', 'FG', '2D', 'P2D', 'W2D', 'F2D']
    df['GD'] = df['G']/df['D']
    df['2DG'] = df['2D']/df['G']

    if (df['WD'].values > 120 and df['D'].values > .5*df['G'].values) or df['WG'].values > 120:

        print("patterning not done")
#         ml_file = pd.read_csv("dataset-2.csv")
#         ml_file.set_value(counter, "ratio"," ")
#         ml_file.to_csv("dataset-2.csv", index=False)
        data = pd.read_csv('dataset-2.csv')
        p = data['power']
        t = data['time']

        import csv
        if counter == 0 or counter == 1:
            toAdd = [p[counter], t[counter]]
            filename = "dataset-2.csv"
            with open(filename, "r") as infile:
                reader = list(csv.reader(infile))
                reader.insert(counter+1, toAdd)

            with open(filename, "w", newline='') as outfile:
                writer = csv.writer(outfile)
                for line in reader:
                    writer.writerow(line)

            df.to_csv("fit.csv", encoding='utf-8', header=False, index=False)

        else:
            if p[counter] == p[counter-1] and p[counter-1] == p[counter-2] and t[counter] == t[counter-1] and t[counter-1] == t[counter-2]:
                print("No shifting will take place")
                ml_file = pd.read_csv("dataset-2.csv")
                ml_file.set_value(counter, "ratio", 0)
                ml_file.to_csv("dataset-2.csv", index=False)
            else:
                toAdd = [p[counter], t[counter]]
                filename = "dataset-2.csv"
                with open(filename, "r") as infile:
                    reader = list(csv.reader(infile))
                    reader.insert(counter+1, toAdd)

                with open(filename, "w", newline='') as outfile:
                    writer = csv.writer(outfile)
                    for line in reader:
                        writer.writerow(line)

            df.to_csv("fit.csv", encoding='utf-8', header=False, index=False)
    else:
        ml_file = pd.read_csv("dataset-2.csv")
        ml_file.set_value(counter, "ratio", df['GD'].values)
        ml_file.to_csv("dataset-2.csv", index=False)
        plot_file = pd.read_csv("plot_data.csv")
        plot_file.set_value(counter, "ratio", df['GD'].values)
        plot_file.to_csv("plot_data.csv", index=False)
        df.to_csv("fit.csv", encoding='utf-8', header=False, index=False)
        p = df['GD']
        twoGD = df['2DG']
        twoD = df['2D']
        G = df['G']
        WD = df['WD']
        WG = df['WG']
        return p, twoGD, twoD, G, WD, WG


# In[ ]:
