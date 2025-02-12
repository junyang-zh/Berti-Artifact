#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from scipy.stats import gmean

if __name__ == "__main__":
    rc('font', size=13)
    name  = []
    torder = ['IP-stride', 'MLOP', 'IPCP', 'vBerti', 'fBerti']
    time_a = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }

    late_a = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }

    time_c = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }

    late_c = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }

    time_c2 = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }
    
    late_c2 = {
            'IP-stride': [],
            'vBerti': [],
            'fBerti': [],
            'IPCP': [],
            'MLOP': [],
            }

    color = {
            'IP-stride': 'snow',
            'MLOP': 'black',
            'IPCP': 'lightgray',
            'vBerti': 'gray',
            'fBerti': 'gainsboro',
            }

    pattern = {
            'IP-stride': '\\\\\\',
            'MLOP': '',
            'IPCP': '',
            'vBerti': '...',
            'fBerti': '///',
            }

    translation = {
        'ip_stride+no': 'IP-stride',
        'mlop_dpc3+no': 'MLOP',
        'ipcp_isca2020+no': 'IPCP',
        'vberti+no': 'vBerti',
        'fberti+no': 'fBerti',
            }

    translation_suite = ['SPEC17-MemInt']

    bench = []
    
    text = {}

    with open(sys.argv[1]) as f:
        raw = f.read().split('\n')

        last = None
        for idx, i in enumerate(raw[:-1]):
            splitted = i.split(';')

            if len(splitted) == 1:
                bench.append(splitted[0])
            else:
                pref = "{}+{}".format(splitted[0], splitted[1])
                if pref not in translation:
                    continue
                time_a[translation[pref]].append(float(splitted[3]) * 100)
                late_a[translation[pref]].append(float(splitted[4]) * 100)
                name.append(pref)

    elem = ['(a)', '(b)', '(c)']

    #fig, ax = plt.subplots(1, 3, figsize=(7,3))
    fig, ax = plt.subplots(1, 2, figsize=(7,3))
    line = ""
    # Idx
    for idx, i in enumerate(translation_suite):
        y = np.arange(len(translation))
        line = i

        x1 = []
        x2 = []
        x3 = []
        x4 = []
        x5 = []
        x6 = []
        for ii in torder:
            x1.append(time_a[ii][idx])
            x2.append(late_a[ii][idx])
            line = "{}; {} (Timely: {}, Late: {})".format(line, ii,
                    time_a[ii][idx], late_a[ii][idx])

        if idx == 0:
            ax[idx].bar(np.arange(len(x1)), x1, color='gray', edgecolor='black', 
                    label="Timely", zorder=3)
            ax[idx].bar(np.arange(len(x1)), x2, color='black', edgecolor='black', 
                    label="Late", zorder=2)
        else:
            ax[idx].bar(np.arange(len(x1)), x1, color='gray', edgecolor='black', 
                    zorder=3)
            ax[idx].bar(np.arange(len(x1)), x2, color='black', edgecolor='black', 
                    zorder=2)

        ax[idx].set_yticks([i for i in range(0, 101, 10)])
        ax[idx].set_yticks([i for i in range(0, 101, 5)], minor=True)
        ax[idx].set_xticks(np.arange(len(x1)))
        ax[idx].set_xticklabels(torder, rotation=25)

        if idx == 0:
            ax[idx].set_ylabel("L1D Prefetch Accuracy")
        #    ax[idx].set_yticklabels([])

        ax[idx].yaxis.grid(True, zorder=1, which='major')
        ax[idx].yaxis.grid(True, zorder=1, which='minor', linestyle='--')

        ax[idx].set_xlabel("{} {}".format(elem[idx], i))

        print(line)

    legend = fig.legend(loc=9, bbox_to_anchor=(0.5, 1.10),
          ncol=3, edgecolor='black', framealpha=1.0)

    fig.tight_layout()
    plt.savefig("fig10.pdf",  bbox_inches = 'tight')
