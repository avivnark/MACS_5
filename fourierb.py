# -*- coding: utf-8 -*-
"""fourierB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qLRLWGpp40PdX5b-Mp1bJ7RkGhCRMCKs

# Frequency domain and Fourier transform
"""

# Commented out IPython magic to ensure Python compatibility.
import cmath, numpy, scipy
from scipy import fftpack
from scipy.fft import fft
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
# %matplotlib inline

"""## Complex numbers

The imaginary number $i$ is defined as $\sqrt{-1}$. Python can handle complex numbers natively.
"""

numpy.sqrt(-1)

numpy.sqrt(complex(-1))

"""We can use complex literals in Python:"""

x = 2 + 1j
print(x, x.real, x.imag, x.conjugate())

x*x.conjugate()

y = 13  - 21j
print(f"{x*y:.0f} {x+y:.0f}, {x**y:.2f}")

"""Regular math functions are applicable to real numbers only."""

import math
math.exp(1j)

"""However, mathematical functions from either `cmath` or `numpy` work on complex numbers."""

print("{:.2f} {:.2f} {:.2f}".format(cmath.exp(cmath.pi*1j), cmath.sin((1+1j)*cmath.pi), cmath.cos(-1+1j)))
print("{:.2f} {:.2f} {:.2f}".format(numpy.exp(numpy.pi*1j), numpy.sin((1+1j)*numpy.pi), numpy.cos(-1+1j)))

"""Transition between polar and rectangular representations is supported in `cmath`."""

r, phi = cmath.polar(x)
x1 = cmath.rect(r, phi)
print(f"{x:.2f} {x1:.2f} r={r:.2f} phi={phi:.2f}")

plt.figure(figsize=(6, 8))
plt.xlim((-0.5, 2.5))
plt.ylim((-2, 2))
plt.grid()
x, y, z = 1+0j, 2+1j, 0.5-1.7j
for k, v in {"x":x, "y":y, "z":z}.items():
    plt.plot([0, v.real], [0, v.imag], label=k)
    plt.scatter([v.real], [v.imag])
plt.legend()

"""## Fourier transform"""



"""Fourier transform transforms between time domain and frequency domain"""

# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = numpy.linspace(0.0, N*T, N)
y1 = numpy.sin(50.0 * 2.0*numpy.pi*x)
y2 = 0.5*numpy.sin(80.0 * 2.0*numpy.pi*x)
for y in [y1, y2, y1 + y2, y1*y2, numpy.exp(-x) + y1 + y2, numpy.exp(-x)*(y1 + y2)]:
    fig, ax = plt.subplots(1, 2, figsize=(20, 4))
    ax[0].set_title("time domain")
    ax[0].plot(x, y)
    ax[0].grid()
    yf = fft(y)
    xf = numpy.linspace(0.0, 1.0/(2.0*T), N//2)
    ax[1].set_title("frequency domain")
    ax[1].plot(xf, 2.0/N * numpy.abs(yf[0:N//2]))
    ax[1].grid()
    plt.show()

"""## Application: image denoising"""

im = plt.imread('http://www.offtopia.net/macs-course/notebooks/moonlanding.png').astype(float)

plt.figure()
plt.imshow(im, plt.cm.gray)
plt.title('Original image')

im

def plot_spectrum(im_fft):
    # A logarithmic colormap
    plt.imshow(numpy.abs(im_fft), norm=LogNorm(vmin=5))
    plt.colorbar()

"""### Full spectrum"""

im_fft = fftpack.fft2(im)

plt.figure()
plot_spectrum(im_fft)
plt.title('Fourier transform')

"""### Filtered spectrum

To denoise the image, we remove intermediate frequencies, keeping only a few low frequencies and a few high frequencies.
"""

# In the lines following, we'll make a copy of the original spectrum and
# truncate coefficients.

# Define the fraction of coefficients (in each direction) we keep
keep_fraction = 0.1

# Call ff a copy of the original transform. Numpy arrays have a copy
# method for this purpose.
im_fft2 = im_fft.copy()
im_fft_noise = im_fft.copy()

# Set r and c to be the number of rows and columns of the array.
r, c = im_fft2.shape

# Set to zero all rows with indices between r*keep_fraction and
# r*(1-keep_fraction):
im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction)), ] = 0

# Similarly with the columns:
im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0

# Opposite for the noise
im_fft_noise[:int(r*keep_fraction), int(c*(1-keep_fraction)):] = 0
im_fft_noise[:int(r*keep_fraction), :int(c*keep_fraction)] = 0
im_fft_noise[int(r*(1-keep_fraction)):, int(c*(1-keep_fraction)):] = 0
im_fft_noise[int(r*(1-keep_fraction)):, :int(c*keep_fraction)] = 0

plt.figure()
plot_spectrum(im_fft2)
plt.title('Filtered Spectrum')
plt.show()

plt.figure()
plot_spectrum(im_fft_noise)
plt.title('Noise Spectrum')
plt.show()

"""### Reconstructed image"""

# Reconstruct the denoised image from the filtered spectrum, keep only the
# real part for display.
im_new = fftpack.ifft2(im_fft2).real

plt.figure()
plt.imshow(im_new, plt.cm.gray)
plt.title('Reconstructed Image')

"""### Removed noise#"""

im_noise = fftpack.ifft2(im_fft_noise).real

plt.figure()
plt.imshow(im_noise, plt.cm.gray)
plt.title('Noise')

"""### Superimposed image and noise, again"""

im_orig = fftpack.ifft2(im_fft2 + im_fft_noise).real

plt.figure()
plt.imshow(im_orig, plt.cm.gray)
plt.title('Original Image, Recovered')