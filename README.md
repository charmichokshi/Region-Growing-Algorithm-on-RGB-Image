# Region-Growing
Implementation of Region Growing Algorithm on RGB Colour Image with Parallel Processing. 

RegionGrowing.py 
**Input:**  Colour Image (1.tif)
        Manually labelled Image (less accurately segmented) (2.tif)
**Output:** Precisely segmented Image (out.tif)
    
Use Function region_growing() to just implement region growing algorithm on a single coloured image.

**Methodology:**

![alt text](https://github.com/charmichokshi/Region-Growing/blob/master/methodology2.PNG)


**Results:**


**Vadodara city:** the road which was neglected in manually labelled image, has detected after applying the unsupervised segmentation, region growing and progressive thresholding techniques. 

**Sagar city:** the urban area which was overestimated has been taken care.

**Jabalpur city:** the visibility of road has been increased as compare to manually labelled image.

![alt text](https://github.com/charmichokshi/Region-Growing/blob/master/results.PNG)
