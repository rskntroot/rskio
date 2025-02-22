# Single Board Computers

## Brief

Employing containerized applications via clustering ARM-based Single Board Computers (SBC)

- by `rskntroot` on `2024-05-30`

## Background

My fascination with ARM-based microcontrollers is in their use as an extremely lightweight replacement for rack-mounted servers.
 In this regard, a power-efficent SoC that can run containerized services has quite the appeal for personal-use applications.
 With the cost of power these days I am baffled at the thought of running the previous generations discounted servers at home.

A few years ago, with the ever raging popularity and scarcity of RaspberryPis,
 I like many others found myself looking for an alternative "PiLike" SoCs.
 After finding LibreComputers offerings, I was delighted to find the "Le Potato".
 For under $40 USD, the [AML-S905X-CC-V1](https://libre.computer/products/aml-s905x-cc/) could reliably run Ubuntu-Server with support for containers!
 Usage of a mainstream Linux-disto on SoC was a game-changer.

Fast forward to 2024, I stumbled across the somewhat quiet release of the 2023 [AML-S905X-CC-V2](https://libre.computer/products/aml-s905x-cc-v2/).
 For just around $35 USD, this release sports USB-C power-in.
 But even better is the PoE support with the addition of a $15 USD [PoE hat](https://www.loverpi.com/products/loverpi-poe-hat-with-pwm-fan-controller-for-aml-s905x-cc-v2-sweet-potato),
 you can deploy these with a single cable, given you have the infrastructure for it and don't mind 100Mb/s.

## Recommendation

The [Sweet Potato AML-S905X-CC-V2](https://libre.computer/products/aml-s905x-cc-v2/) is a great starter board.
 Seriously, check out the specs.
 This little guy is packing just enough for a streamlined CI/CD pipeline to host some tolerant webservices on the edge.
 (For obvious reasons, "the edge" is just my family and friend's houses across the United States.)

If you need more RAM, USB3.0, or AI Acceleration is mandatory, checkout LibreComputer's
  [Alta](https://libre.computer/products/aml-a311d-cc/) which will quickly double your investment.

## Projects

This website is hosted on 2 sweet potatos with an alta as the cluster controller.

## Notes

### PoE Setup

Using Power over Ethernet (PoE) to run your SoCs is just awesome! You only need 1 cable?! Be sure to get yourself some good cables and a solid PoE switch.

I have personnally been using these:

- [CAT8 Ethernet cables](https://www.amazon.com/dp/B08PL1P53C/)
    - Ive used countless Ethernet Cables and fashioning hundreds of my own; can confirm these are premium.
- [1G PoE+ 8-port Switch](https://www.amazon.com/dp/B08FCQ8BRC)
    - Unmanaged switch that I can recommend. Works like a charm.

### CAT8 Real?

Telco Data [article](https://www.telco-data.com/blog/cat-cables/):

"Category 8 is the official successor to Cat6A cabling.
 It is officially recognized by the IEEE and EIA and parts and pieces are standardized across manufacturers.
 The primary benefit of Cat8 cabling is faster throughput over short distances: 40 Gbps up to 78’ and 25 Gbps up to 100’.
 From 100’ to 328’, Cat8 provides the same 10Gbps throughput as Cat6A cabling."

ANSI/TIA [TIA Press Release](https://standards.tiaonline.org/tia-issues-new-balanced-twisted-pair-telecommunications-cabling-and-components-standard-addendum-1):

"TIA-568-C.2-1 - This addendum specifies minimum requirements for shielded category 8 balanced twisted-pair telecommunications
 cabling (e.g. channels and permanent links) and components (e.g. cable,connectors, connecting hardware, and equipment cords)
 that are used up to and including the equipment outlet/connector in data centers, equipment rooms, and other spaces that need
 high speed applications. This addendum also specifies field test procedures and applicable laboratory reference measurement
 procedures for all transmission parameters."
