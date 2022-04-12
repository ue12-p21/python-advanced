import numpy as np
import matplotlib.pyplot as plt

import streamlit as st

def sinus4(freq, phase, amplitude, domain):

    figure = plt.figure()
    X = np.linspace(0., domain*np.pi, 500)
    Y = amplitude * np.sin(freq*(X+phase))
    # comme on va régler l'amplitude, on fixe l'échelle en Y
    plt.clf()
    plt.ylim(-5, 5)
    plt.plot(X, Y)
    return figure


freq = st.slider("frequency", value=1, min_value=1, max_value=10, step=1)

phase = 0

amplitude = st.selectbox(
     'Amplitude',
     (.1, 1, 3, 5),
     # the index in the tuple above
     # so that initial value is 3
     index=2)


domain = 4

st.pyplot(fig=sinus4(freq, phase, amplitude, domain))
