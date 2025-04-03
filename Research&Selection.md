# Paper 1: REPLAY AND SYNTHETIC SPEECH DETECTION WITH RES2NET ARCHITECTURE(https://ieeexplore.ieee.org/abstract/document/9413828)
## Key Technical Innovation:
•	Introduces Res2Net architecture to ASV anti-spoofing systems 
•	Modifies ResNet blocks to enable multiple feature scales by splitting feature maps and creating residual-like connections across  channel groups 
•	Increases possible receptive fields resulting in multiple feature scales 
•	Integration with squeeze-and-excitation (SE) block further enhances performance 
•	Decreases model size compared to traditional ResNet models 
## Best Reported Performance:
•	Physical Access (PA): SE-Res2Net50 with CQT features achieved EER of 0.459% and t-DCF of 0.0116 
•	Logical Access (LA): Stat-SE-Res2Net50 achieved EER of 2.86% and t-DCF of
0.068 
•	Outperforms other state-of-the-art single systems for both PA and LA scenarios 
## Promising for Use Case:
•	Defense against unseen spoofing attacks in ASV systems 
•	Effective for detecting both replay attacks (PA) and synthetic speech attacks (LA) 
•	Security-sensitive voice authentication systems 
## Potential Limitations:
•	Model performance varies significantly depending on input features 
•	Still room for improvement in LA scenario detection 
 
•	No specific analysis on computational complexity or real-time performance 


# Paper 2: ResMax: Detecting Voice Spoofing Attacks with Residual Network and Max Feature Map (https://ieeexplore.ieee.org/document/9412165)
## Key Technical Innovation:
•	Combines skip connection from ResNet with max feature map (MFM) from Light CNN 
•	Introduces "ResMax" architecture designed for lightweight implementation 
•	Uses optimized constant Q transform (CQT) feature extraction 
•	Designed specifically with model size and latency constraints for real-world deployment 
## Best Reported Performance:
•	Physical Access (PA): EER of 0.37% on evaluation set, surpassing top ensemble system from ASVspoof 2019 
•	Logical Access (LA): EER of 2.19% 
•	Small model size of only 262K parameters 
## Promising for Use Case:
•	Voice assistant security with strict latency requirements 
•	On-device deployment scenarios requiring small model size 
•	Real-time voice spoofing detection 
•	Business applications with model size constraints under a few megabytes 
## Potential Limitations:
•	Performance degrades with shorter audio samples 
•	Higher error rates for certain voice conversion attacks (A17, A18, A19) 
•	Detection becomes more difficult with high-quality replay devices 
 
•	More challenging to detect attacks when talker-to-ASV distance is very close or very far 


# Paper 3: LEARNING FROM YOURSELF: A SELF-DISTILLATION METHOD FOR FAKE SPEECH DETECTION(https://arxiv.org/abs/2303.01211)
## Key Technical Innovation:
•	Novel self-distillation method that improves performance without increasing inference complexity 
•	Divides networks into segments, using deepest network as teacher model and shallow networks as student models 
•	Implements distillation in both feature and prediction dimensions 
•	Combines three loss types: hard loss (A-softmax), feature loss (L2), and soft loss (KL divergence) 
## Best Reported Performance:
•	Logical Access (LA): Best EER of 0.88% with ECANet18(SD) 
•	Physical Access (PA): Best EER of 0.65% with SENet34(SD) 
•	Significant improvement over baselines (e.g., SENet50 improved from 1.83% to 1.00% EER - 45% improvement) 
•	Ranked 2nd among known single systems for both LA and PA tasks 
## Promising for Use Case:
•	Improving performance without increasing inference computational load 
•	Applicable across different network architectures (ECANet and SENet) 
•	Effective for both replay and synthetic speech detection 
•	Helps capture fine-grained information in shallow networks that's important for FSD 
## Potential Limitations:
 
•	More complex training process with multiple loss components 
•	Requires hyperparameter tuning for balancing different losses 
•	While effective, doesn't achieve top performance compared to some specialized architectures 
•	Extra classifiers needed during training
