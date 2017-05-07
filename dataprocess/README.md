# Data augmentation
* Random crops
* contrast and color jittering
* pretrained on LOC + pretrained global context：在LOC上训练时，得到proposal以后，做roi pooling时，多出一支在roi周围加一圈background后再进行pooling.
