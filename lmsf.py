import numpy as np

def lmsf_1d(sig, n=5, t=0.5):
    """Local Mean Suppression Filter (LMSF) for a sequence of equidistant signal samples.
    
    Parameters
    ----------
    sig : 1D (length) numpy array.
        The input discrete signal.
    n : int (positive).
        The integer parameter n defines the size (2n+1) of averaging window.
        n cannot be less than 1 and n cannot be greater than n_max, where
        n_max = floor(length/2) - 1
    t : float (positive).
        The signal threshold.
        In most practical cases, t can be set between 0.5 and 1.
    
    Returns
    -------
    sig_avr : 1D (length) numpy array.
        The LMSF response to the input signal, the signal sequence with low levels replaced by zeros."""
    w = len(sig)
    ker = np.ones((2*n+1,), dtype='int32')
    row = np.ones((1,w), dtype='int32')
    sig_avr = np.convolve(sig, ker, mode='same')
    norm = np.convolve(row[0,:], ker, mode='same')
    sig_avr = np.divide(sig_avr, norm)
    norm = sig < t*sig_avr
    sig_avr = sig.copy()
    sig_avr[norm] = 0
    return sig_avr

def lmsf_2d(img, n=5, t=0.5):
    """Local Mean Suppression Filter (LMSF) for a gray-scale image.
    
    Parameters
    ----------
    img : 2D (height, width) numpy array.
        The input gray-scale image.
    n : int (positive).
        The integer parameter n defines the side length (2n+1) of square averaging window.
        n cannot be less than 1 and n cannot be greater than n_max, where
        n_max = floor(min(height, width)/2) - 1
    t : float (positive).
        The intensity threshold.
        In most practical cases, t can be set between 0.5 and 1.
    
    Returns
    -------
    img_avr : 2D (height, width) numpy array.
        The LMSF response to the input image, the image with denoised background."""
    h = img.shape[0]
    w = img.shape[1]
    ker = np.ones((2*n+1,), dtype='int32')
    row = np.ones((1,w), dtype='int32')
    img_avr = np.zeros((h,w), dtype='float64')
    norm = np.zeros((h,w), dtype='int32')
    for i in range(h):
        img_avr[i,:] = np.convolve(img[i,:], ker, mode='same')
        norm[i,:] = np.convolve(row[0,:], ker, mode='same')
    for j in range(w):
        img_avr[:,j] = np.convolve(img_avr[:,j], ker, mode='same')
        norm[:,j] = np.convolve(norm[:,j], ker, mode='same')
    img_avr = np.divide(img_avr, norm)
    norm = img < t*img_avr
    img_avr = img.copy()
    img_avr[norm] = 0
    return img_avr

def lmsf_2d_cumulative(img, t=0.5, nn=[5,10,20,40]):
    """Cumulative LMSF for background denoising of gray-scale images."""
    mask_cum = np.ones((img.shape), dtype='bool')
    for n in nn:
        img_filtered = lmsf_2d(img, n=n, t=t)
        mask_cum = np.logical_and(mask_cum, img_filtered != 0)
    mask_cum = np.logical_not(mask_cum)
    img_filtered = img.copy()
    img_filtered[mask_cum] = 0
    return img_filtered