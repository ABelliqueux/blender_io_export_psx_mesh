typedef struct {  
	TMESH *     tmesh;
	int *       index;
	TIM_IMAGE * tim;  
	u_long *    tim_data;
	} MESH;

SVECTOR modelCube_mesh[] = {
	{-56.728477478027344,70.00000476837158,-122.00001239776611},
	{-236.72844886779785,190.00001907348633,-302.00002670288086},
	{123.27152252197266,190.00000476837158,-122.00001239776611},
	{63.271522521972656,129.99999046325684,177.99997329711914},
	{-176.7284631729126,70.00000476837158,-122.00001239776611},
	{-236.72844886779785,70.00001192092896,-182.0000123977661},
	{-176.7284631729126,190.00001907348633,-242.00002670288086},
	{-56.728477478027344,190.00001907348633,-242.00002670288086},
	{-176.7284631729126,190.00001907348633,-302.00002670288086},
	{-116.7284631729126,190.00001907348633,-302.00002670288086},
	{3.2715225219726562,190.00001907348633,-242.00002670288086},
	{63.271522521972656,190.00001907348633,-242.00002670288086},
	{-56.728477478027344,190.00001907348633,-302.00002670288086},
	{3.2715225219726562,190.00001907348633,-302.00002670288086},
	{63.271522521972656,69.99999046325684,177.99997329711914},
	{-116.7284631729126,190.00001907348633,-242.00002670288086},
	{63.271522521972656,190.00001907348633,-302.00002670288086},
	{123.27152252197266,190.00001907348633,-302.00002670288086},
	{-56.728477478027344,190.00000476837158,-122.00001239776611},
	{183.27152252197266,190.00001907348633,-302.00002670288086},
	{-236.72844886779785,70.00000476837158,-122.00001239776611},
	{-116.7284631729126,190.00001907348633,-182.0000123977661},
	{3.2715225219726562,190.00000476837158,-122.00001239776611},
	{3.2715225219726562,190.00001907348633,-182.0000123977661},
	{-56.728477478027344,190.00001907348633,-182.0000123977661},
	{3.2715225219726562,130.00000476837158,-122.00001239776611},
	{-176.7284631729126,190.00001907348633,-182.0000123977661},
	{183.27152252197266,190.00000476837158,-122.00001239776611},
	{63.271522521972656,189.99999046325684,177.99997329711914},
	{63.271522521972656,190.00001907348633,-182.0000123977661},
	{183.27152252197266,190.00001907348633,-182.0000123977661},
	{123.27152252197266,190.00001907348633,-182.0000123977661},
	{123.27152252197266,190.00001907348633,-242.00002670288086},
	{183.27152252197266,190.00001907348633,-242.00002670288086},
	{63.271522521972656,130.00000476837158,-2.0000123977661133},
	{243.27152252197266,190.00001907348633,-302.00002670288086},
	{123.27152252197266,190.00000476837158,117.99998760223389},
	{123.27152252197266,190.00000476837158,-62.00000524520874},
	{183.27152252197266,190.00000476837158,-2.0000123977661133},
	{123.27152252197266,190.00000476837158,-2.0000123977661133},
	{123.27152252197266,189.99999046325684,177.99997329711914},
	{243.27152252197266,129.99999046325684,177.99997329711914},
	{243.27152252197266,190.00001907348633,-182.0000123977661},
	{123.27152252197266,190.00000476837158,57.99998760223389},
	{183.27152252197266,190.00000476837158,117.99998760223389},
	{183.27152252197266,190.00000476837158,57.99998760223389},
	{243.27152252197266,190.00001907348633,-242.00002670288086},
	{183.27152252197266,190.00000476837158,-62.00000524520874},
	{243.27152252197266,190.00000476837158,-122.00001239776611},
	{243.27152252197266,190.00000476837158,-62.00000524520874},
	{243.27152252197266,189.99999046325684,177.99997329711914},
	{243.27152252197266,190.00000476837158,-2.0000123977661133},
	{243.27152252197266,190.00000476837158,57.99998760223389},
	{243.27152252197266,190.00000476837158,117.99998760223389},
	{-236.72844886779785,190.00000476837158,-122.00001239776611},
	{183.27152252197266,129.99999046325684,177.99997329711914},
	{63.271522521972656,190.00000476837158,-122.00001239776611},
	{-116.7284631729126,190.00000476837158,-122.00001239776611},
	{-176.7284631729126,190.00000476837158,-122.00001239776611},
	{-236.72844886779785,130.00000476837158,-122.00001239776611},
	{63.271522521972656,190.00000476837158,-2.0000123977661133},
	{-56.728477478027344,130.00000476837158,-122.00001239776611},
	{63.271522521972656,190.00000476837158,117.99998760223389},
	{63.271522521972656,130.00000476837158,-122.00001239776611},
	{63.271522521972656,190.00000476837158,-62.00000524520874},
	{63.271522521972656,130.00000476837158,-62.00001239776611},
	{63.271522521972656,190.00000476837158,57.99998760223389},
	{63.271522521972656,130.00000476837158,57.99998760223389},
	{-176.7284631729126,130.00000476837158,-122.00001239776611},
	{63.271522521972656,69.99999046325684,-2.0000123977661133},
	{63.271522521972656,70.00000476837158,-62.00001239776611},
	{63.271522521972656,130.00000476837158,117.99998760223389},
	{63.271522521972656,69.99999046325684,57.99998760223389},
	{63.271522521972656,69.99999046325684,117.99998760223389},
	{63.271522521972656,70.00000476837158,-122.00001239776611},
	{3.2715225219726562,70.00000476837158,-122.00001239776611},
	{-116.7284631729126,130.00000476837158,-122.00001239776611},
	{-116.7284631729126,70.00000476837158,-122.00001239776611},
	{183.27152252197266,189.99999046325684,177.99997329711914},
	{-236.72844886779785,130.00001907348633,-242.00002670288086},
	{123.27152252197266,69.99999046325684,177.99997329711914},
	{-236.72844886779785,190.00001907348633,-242.00002670288086},
	{183.27152252197266,69.99999046325684,177.99997329711914},
	{243.27152252197266,69.99999046325684,177.99997329711914},
	{-236.72844886779785,190.00001907348633,-182.0000123977661},
	{123.27152252197266,129.99999046325684,177.99997329711914},
	{-236.72844886779785,130.00001907348633,-182.0000123977661},
	{-236.72844886779785,130.00001907348633,-302.00002670288086},
	{-236.72844886779785,70.00001192092896,-242.00002670288086},
	{-236.72844886779785,70.00001907348633,-302.00002670288086}
};

SVECTOR modelCube_normal[] = {
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	0.0,-1.0,-2.3841863594498136e-07,0,
	0.0,-1.0,-2.3841863594498136e-07,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	-0.0,-1.0,-0.0,0,
	0.0,-1.0,-2.3841863594498136e-07,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	1.0,0.0,-0.0,0,
	1.0,-0.0,0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	0.0,0.0,1.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	-0.0,-1.0,-2.3841863594498136e-07,0,
	-0.0,-1.0,-2.3841863594498136e-07,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	-0.0,-1.0,-2.384185791015625e-07,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	0.0,-1.0,0.0,0,
	-0.0,-1.0,-2.3841863594498136e-07,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	1.0,0.0,0.0,0,
	1.0,-0.0,0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,0.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	0.0,-0.0,1.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,-0.0,0,
	1.0,0.0,0.0,0,
	1.0,0.0,-0.0,0
};

SVECTOR modelCube_uv[] = {
	255.9749972820282,63.024998903274536, 0, 0,
	192.02500641345978,126.97498977184296, 0, 0,
	255.9749972820282,126.97498977184296, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	192.02488481998444,63.024877309799194, 0, 0,
	255.97511887550354,126.9751113653183, 0, 0,
	255.97511887550354,63.024877309799194, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.02466064691544,126.97533935308456, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	191.9751226902008,63.024877309799194, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	191.9751226902008,63.024877309799194, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	191.9751226902008,63.024877309799194, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	191.9751226902008,63.024877309799194, 0, 0,
	0.024885178245313,63.024877309799194, 0, 0,
	63.97511512041092,126.9751113653183, 0, 0,
	63.97511512041092,63.024877309799194, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,126.97498977184296, 0, 0,
	192.02488481998444,63.024877309799194, 0, 0,
	255.97511887550354,126.9751113653183, 0, 0,
	255.97511887550354,63.024877309799194, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	128.02501022815704,62.97499358654022, 0, 0,
	255.97536206245422,126.97533935308456, 0, 0,
	192.02465683221817,63.02463412284851, 0, 0,
	192.02465683221817,126.97533935308456, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,63.02475571632385, 0, 0,
	192.0247632265091,126.97523295879364, 0, 0,
	255.97524046897888,63.02475571632385, 0, 0,
	192.0247632265091,63.02475571632385, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	0.024999619272421114,190.9749935567379, 0, 0,
	255.9749972820282,63.024998903274536, 0, 0,
	192.02500641345978,63.024998903274536, 0, 0,
	192.02500641345978,126.97498977184296, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	192.02488481998444,63.024877309799194, 0, 0,
	192.02488481998444,126.9751113653183, 0, 0,
	255.97511887550354,126.9751113653183, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	191.9753658771515,126.97533935308456, 0, 0,
	191.9753658771515,63.02463412284851, 0, 0,
	128.02466064691544,63.02463412284851, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	128.0248886346817,126.9751113653183, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	128.0248886346817,126.9751113653183, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	128.0248886346817,126.9751113653183, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	128.0248886346817,63.024877309799194, 0, 0,
	128.0248886346817,126.9751113653183, 0, 0,
	191.9751226902008,126.9751113653183, 0, 0,
	0.024885178245313,63.024877309799194, 0, 0,
	0.024885178245313,126.9751113653183, 0, 0,
	63.97511512041092,126.9751113653183, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	191.97500109672546,63.024998903274536, 0, 0,
	128.02501022815704,63.024998903274536, 0, 0,
	128.02501022815704,126.97498977184296, 0, 0,
	192.02488481998444,63.024877309799194, 0, 0,
	192.02488481998444,126.9751113653183, 0, 0,
	255.97511887550354,126.9751113653183, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	191.97500109672546,62.97499358654022, 0, 0,
	191.97500109672546,-0.9749972820281982, 0, 0,
	128.02501022815704,-0.9749972820281982, 0, 0,
	255.97536206245422,126.97533935308456, 0, 0,
	255.97536206245422,63.02463412284851, 0, 0,
	192.02465683221817,63.02463412284851, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	128.02476704120636,126.97523295879364, 0, 0,
	191.97524428367615,126.97523295879364, 0, 0,
	191.97524428367615,63.02475571632385, 0, 0,
	192.0247632265091,126.97523295879364, 0, 0,
	255.97524046897888,126.97523295879364, 0, 0,
	255.97524046897888,63.02475571632385, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	192.02500641345978,62.97499358654022, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	255.9749972820282,62.97499358654022, 0, 0,
	255.9749972820282,-0.9749972820281982, 0, 0,
	192.02500641345978,-0.9749972820281982, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0,
	63.975001126527786,190.9749935567379, 0, 0,
	63.975001126527786,127.02499508857727, 0, 0,
	0.024999619272421114,127.02499508857727, 0, 0
};

CVECTOR modelCube_color[] = {
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0,
	80,80,80,0,
	128,128,128,0,
	128,128,128,0
};

int modelCube_index[] = {
	81,8,6,
	84,6,26,
	54,26,58,
	6,9,15,
	15,12,7,
	7,13,10,
	10,16,11,
	11,17,32,
	32,19,33,
	58,21,57,
	57,24,18,
	18,23,22,
	22,29,56,
	56,31,2,
	2,30,27,
	31,33,30,
	29,32,31,
	23,11,29,
	24,10,23,
	21,7,24,
	26,15,21,
	64,2,37,
	60,37,39,
	66,39,43,
	62,43,36,
	28,36,40,
	40,44,78,
	36,45,44,
	43,38,45,
	39,47,38,
	37,27,47,
	33,35,46,
	30,46,42,
	27,42,48,
	47,48,49,
	38,49,51,
	45,51,52,
	44,52,53,
	78,53,50,
	54,68,58,
	58,76,57,
	57,61,18,
	18,25,22,
	22,63,56,
	64,63,56,
	64,34,65,
	66,34,60,
	62,67,66,
	28,71,62,
	65,74,63,
	34,70,65,
	67,69,34,
	71,72,67,
	3,73,71,
	25,74,63,
	61,75,25,
	76,0,61,
	68,77,76,
	59,4,68,
	3,80,85,
	85,82,55,
	55,83,41,
	28,85,40,
	40,55,78,
	78,41,50,
	81,87,1,
	84,79,81,
	54,86,84,
	59,5,86,
	86,88,79,
	79,89,87,
	81,1,8,
	84,81,6,
	54,84,26,
	6,8,9,
	15,9,12,
	7,12,13,
	10,13,16,
	11,16,17,
	32,17,19,
	58,26,21,
	57,21,24,
	18,24,23,
	22,23,29,
	56,29,31,
	2,31,30,
	31,32,33,
	29,11,32,
	23,10,11,
	24,7,10,
	21,15,7,
	26,6,15,
	64,56,2,
	60,64,37,
	66,60,39,
	62,66,43,
	28,62,36,
	40,36,44,
	36,43,45,
	43,39,38,
	39,37,47,
	37,2,27,
	33,19,35,
	30,33,46,
	27,30,42,
	47,27,48,
	38,47,49,
	45,38,51,
	44,45,52,
	78,44,53,
	54,59,68,
	58,68,76,
	57,76,61,
	18,61,25,
	22,25,63,
	64,65,63,
	64,60,34,
	66,67,34,
	62,71,67,
	28,3,71,
	65,70,74,
	34,69,70,
	67,72,69,
	71,73,72,
	3,14,73,
	25,75,74,
	61,0,75,
	76,77,0,
	68,4,77,
	59,20,4,
	3,14,80,
	85,80,82,
	55,82,83,
	28,3,85,
	40,85,55,
	78,55,41,
	81,79,87,
	84,86,79,
	54,59,86,
	59,20,5,
	86,5,88,
	79,88,89
};

TMESH modelCube = {
	modelCube_mesh,  
	modelCube_normal,
	modelCube_uv,
	modelCube_color, 
	142
};

extern unsigned long _binary_TIM_home_tim_start[];
extern unsigned long _binary_TIM_home_tim_end[];
extern unsigned long _binary_TIM_home_tim_length;

TIM_IMAGE tim_home;

MESH meshCube = {
	&modelCube,
	modelCube_index,
	&tim_home,
	_binary_TIM_home_tim_start
};

MESH * meshes[1] = {
	&meshCube
}; 
