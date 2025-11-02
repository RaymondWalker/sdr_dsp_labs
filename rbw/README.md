## Resolution Bandwidth (RBW) & Segment Length Trade-Off

### Theory

From the previous section, the characteristic that determined either smoothness or resolution was the **Segment length $(N_{seg})$**. This changes the width of each FFT Bin - aka **Resolution Bandwidth** . The RBW describes the smallest frequency that each segment can represent :
$$ RBW = \frac{f_{s}}{N_{seg}} $$

When choosing RBW, a decision has to be made : slower, detailed readings or visually smooth, less accurate readings. 


### Analysis

From the graphs, it would be wise to choose a segment length larger that 1024 bits but smaller than 4096 bits for the most balanced expereince.  This configuration will yield usable data ( decent resolution aka smaller RBW) while not incurring significant delay. 