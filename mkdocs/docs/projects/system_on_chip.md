# System on Chip

## Brief

Employing containerized applications via clustering modern ARM-based System on Chip (SoC) 

- by `rskntroot` on `2024-05-30`

## Background

With over 10 years of industry experience in computing technologies, I have owned a handful of RaspBerryPi through the years. After learning basic circuitry and microcontroller fundamentals thanks to Arduino back in 2010 or so, I watched rPi quickly captivate the industry. As a hobbist, I spent many hours trying to come to terms with the limitations in RaspbianOS; followed by even more time bridging the knowledge gap between what I knew from networking, embedded-systems, virtualization platforms, and Enterprise Linux and this fledgling ARM-based ecosystem.

As someone who has spent far more time building and managing Enterprise networks, servers, and services; all while trying to convice tenured Microsoft-indoctrinated IT admins that containerization in Linux was the future; I certainly didn't spend enough time completing weekend circuitry projects. It likely comes as no surprise that my fascination with ARM-based microcontrollers is in their use as an extremely lightweight replacement for rack-mounted servers--given you are NOT running computationally or storage-heavy workloads. In this regard, a power-efficent SoC that can run containerized services has quite the appeal for personal-use applications. With the cost of power these days I am baffled at the thought of running the previous generations discounted servers at home.

A few years ago, with the ever raging popularity of RaspberryPis, I like many others found myself looking for an alternative "PiLike" SoCs. After finding LibreComputers offerings, I was delighted to find the "Le Potato". For under $40 USD, the [AML-S905X-CC-V1](https://libre.computer/products/aml-s905x-cc/) could reliably run Ubuntu-Server (headless) with support for containers?! Usage of a mainstream Linux-disto on SoC was a game-changer for me. So I bought a couple and worked through the ever so "minor challenges" of getting started with a new platform. To my suprise it was rather straightforward.

Fast forward to 2024, I stumbled across the somewhat quiet release of the 2023 [AML-S905X-CC-V2](https://libre.computer/products/aml-s905x-cc-v2/). Man how time flies. For just around $35 USD, this release sports USB-C power-in. But even better is the PoE support with the addition of a $15 USD [PoE hat](https://www.loverpi.com/products/loverpi-poe-hat-with-pwm-fan-controller-for-aml-s905x-cc-v2-sweet-potato?_pos=1&_psq=poe&_ss=e&_v=1.0), you can deploy these with a single cable, given you have the infrastructure for it.

## Recommendation

Efficient, featureful, and cheap; the [Sweet Potato AML-S905X-CC-V2](https://libre.computer/products/aml-s905x-cc-v2/) is just what the doctor ordered. Seriously, check out the specs. One could always ask for more cores, RAM, eMMC. However, this little guy is packing just enough for a streamlined CI/CD pipeline to host some tolerant webservices across the edge. (For obvious reasons, "the edge" is just my family and friend's houses across the United States.)

If you need more RAM, USB3.0, or AI Acceleration is mandatory, checkout LibreComputer's [Alta](https://libre.computer/products/aml-a311d-cc/) or [Solitude](https://libre.computer/products/aml-s905d3-cc/) Models which can quickly double your investment.

## Projects

This website is hosted on these bad bois, the sweet potato that is.

> sphinx-docs w/ markdown generated website hosted on nginx alpine-linux
>
> `github` [rskntroot/rskio](https://github.com/rskntroot/rskio)


> traefik fe proxy w/ sticky loadbalancing for docker swarm
>
> `github` [rskntroot/traefik](https://github.com/rskntroot/traefik/)

### LLM on ARM

For my purposes, a handful of Sweet Potatos will do the trick, but if I start playing around with any [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model)... like I keep telling myself I will, a few Altas in a cluster sounds like a fun experiment.

Maybe just biting the bullet and buying into in the [Nvidia Jerson](https://developer.nvidia.com/embedded-computing) offerings may be the play.

Or even just use that 4000-series Nvidia GPU for something other than filling up space in your handbuilt PC like the washed-up gamer you are (but that's not ARM!).

## Notes

### PoE Setup

Using Power over Ethernet (PoE) to run your SoCs is just awesome! You only need 1 cable?! Be sure to get yourself some good cables and a solid PoE switch.

I have personnally been using these:

- [CAT8 Ethernet cables](https://www.amazon.com/Ethernet-Internet-Network-Professional-Shielded/dp/B08PL1P53C/ref=sr_1_4?crid=1ELCUKBT7V3YB&dib=eyJ2IjoiMSJ9.W2iSbQd5bQGYHCf-9Vt3AovS1xEhC0zzsheMJG1QFnYut2JmmRCQzZmwq60K1uSUoGiTU8RUzjOTwybWF9lFZrGDx4abFxPwgCaCQTvL9Fvqa6UQ4Qu6o6JWEZRkWwNUWK34Izz1HPf1r54hVQ2NrN6f1r6PDUk2NDEab2zld8MVx2zRT4-s-8-jgwi8ng6wccQVAiJu-kTGeN_fkNohbUcpUMkmE-ARnhBrV05qIZg.OigmTuqYLiyRtsbLu-nXFx2nluGZo0e0IwjWTcXuHgg&dib_tag=se&keywords=cat8%2Bethernet%2Bcable&qid=1717047302&sprefix=cat8%2Caps%2C134&sr=8-4&th=1) by [VABOGU](https://www.amazon.com/stores/VABOGU/page/20815F77-3E58-4871-A2EB-1772920695D9?ref_=ast_bln)
    - Ive used countless Ethernet Cables and fashioning hundreds of my own, I can confirm these are premium.
- [1G PoE+ 8-port Switch](https://www.amazon.com/dp/B08FCQ8BRC?ref=nb_sb_ss_w_as-reorder_k1_1_9&amp=&crid=1OZ5HYTQCXGAQ&amp=&sprefix=poe+switc) by [AMCREST](https://www.amazon.com/stores/Amcrest/page/2404E471-79FC-4D18-B767-8777D048264F?ref_=ast_bln)
    - Unmanaged switch that I can recommend. Works like a charm.

### CAT8 Real?

Telco Data [article](https://www.telco-data.com/blog/cat-cables/):

"Category 8 is the official successor to Cat6A cabling. It is officially recognized by the IEEE and EIA and parts and pieces are standardized across manufacturers. The primary benefit of Cat8 cabling is faster throughput over short distances: 40 Gbps up to 78’ and 25 Gbps up to 100’. From 100’ to 328’, Cat8 provides the same 10Gbps throughput as Cat6A cabling."


 ANSI/TIA [TIA Press Release](https://standards.tiaonline.org/tia-issues-new-balanced-twisted-pair-telecommunications-cabling-and-components-standard-addendum-1):

 "TIA-568-C.2-1 - This addendum specifies minimum requirements for shielded category 8 balanced twisted-pair telecommunications cabling (e.g. channels and permanent links) and components (e.g. cable,connectors, connecting hardware, and equipment cords) that are used up to and including the equipment outlet/connector in data centers, equipment rooms, and other spaces that need high speed applications. This addendum also specifies field test procedures and applicable laboratory reference measurement procedures for all transmission parameters."

