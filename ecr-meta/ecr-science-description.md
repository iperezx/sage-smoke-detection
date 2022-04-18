## Background
Wildland fires have destroyed 4% of California in 2020, the worst fire season in history. A common observation is that major destruction by fires is a worldwide trend,  and fire behavior is changing due to a combination of natural and anthropogenic factors, and frequency of catastophic fires is increasing [1]. Preventing the propagation of wildfires heavily relies on observations to be able to deploy resources and firefighters to combat the spread of wildfires.

There is no doubt that having the right tools combat both the initiation and propagation of wildfire is key to preventing events present an economic burden to our economy. This case study provides the next step to providing firefighters with the right tools to combat wildfires. The NSF-funded WIFIRE project (wifire.ucsd.edu) took the first steps to tackle this problem, successfully creating an integrated system for wildfire monitoring, simulation, and response. Today, WIFIRE provides an end-to-end management cyberinfrastructure (CI) with integrated data collection from many real-time and archived data sources, knowledge management through AI, and modeling wildfire behavior using a plethora of community-developed wildfire modeling and simulation services at the digital continuum using many modes of computing.

Automatic detection of a fire ignition or the perimeter of an ongoing fire is still a research topic that combines capturing imagery through remote sensing and analyzing the captured imagery through AI [2]. Any infrastructure built to enable these research efforts should provide support for data hosting, model training, model deployment and inference steps of the associated AI process. However, once reliable AI methods for this purpose are available, they have the potential to provide unprecedented edge intelligence capabilities in this domain. This potential made real-time smoke detection also one of the scientific case studies for the Sage AI on the Edge project.

## Workflow description
The edge compute environment consist of the sensor data acquisition system (HPWREN cameras [3] or Wild Sage Nodes) and the smoke detection plugin. The plugin uses a novel deep learning architecture called SmokeyNet [4] which uses spatiotemporal information from camera imagery for real-time wildfire smoke detection. When trained on the FIgLib dataset, SmokeyNet outperforms comparable baselines and rivals human performance. The trainning data comes from the Fire Ignition Library [5] which is an open source image library that consist of historical fires that were labeled as smoke or no smoke 40 minutes before and after the fire started and became visible from the HPWREN cameras.

### References
[1] John Salguero, Jingjing Li, Alireza Farahmand, and John T. Reager. 2020. Wild-fire Trend Analysis over the Contiguous United States Using Remote SensingObservations.Remote Sensing12, 16 (2020). https://doi.org/10.3390/rs12162565.

[2] Kinshuk Govil, Morgan L. Welch, J. Timothy Ball, and Carlton R. Pennypacker.2020. Preliminary Results from a Wildfire Detection System Using Deep Learningon Remote Camera Images.Remote Sensing12, 1 (Jan 2020), 166.https://doi.org/10.3390/rs12010166

[3] 2021. Website for High Performance Wireless Research and Education Network.http://hpwren.ucsd.edu

[4] Dewangan, A.; Pande, Y.; Braun, H.-W.; Vernon, F.; Perez, I.; Altintas, I.; Cottrell, G.W.; Nguyen, M.H. FIgLib & SmokeyNet: Dataset and Deep Learning Model for Real-Time Wildland Fire Smoke Detection. Remote Sens. 2022, 14, 1007. https://doi.org/10.3390/rs14041007

[5] 2021. Labeled Training Data for Smoke Detection in the HPWREN Fire IgnitionImage Library. http://hpwren.ucsd.edu/HPWREN-FIgLib/