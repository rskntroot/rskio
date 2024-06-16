
# Personal NAS

## Brief

Scoping an 48 terabyte onsite Network Attached Storage (NAS) and Networking solution for personal usage

- by `rskntroot` on `2024-06-12`

## Assumptions

At a minimum, the storage solution must provide redundant copies of the data. The solution must function in the event of a single-drive failure. Individual storage drives used must be enterprise-grade, warrantied, with the expectation of 1 million hours MTBF.

Given standard network connectivity is at or under 1Gbps speeds, 10Gb/s internal networking is not expected. However, the storage solution should provide future expansion options for 10Gb/s networking.

Concerns regarding redudant power or battery backup for the solution are outside the scope of this document and would be handled by the customer. Recommened best practice for storage solutions is to keep on a battery backup to allow for graceful shutdown.

## Hardware

### Chassis

=== "QNAP TS-673A"

    - `1x` QNAP TS-673A 6-Bay `$899 USD`
    - [QNAP Product Page](https://www.qnap.com/en-us/product/ts-673a)

=== "TeamGroup 32GB DDR4 SODIMM"

    - `2x` 16GB DDR4 SODIMM `$60 USD`
    - [TeamGroup Product Page](https://www.teamgroupinc.com/en/product-detail/memory/TEAMGROUP/elite-so-dimm-ddr4/elite-so-dimm-ddr4-TED432G3200C22DC-S01/)

=== "Crucial T500 2TB NVMe"

    - `2x` 2TB M.2 NVMe `$406 USD`
    - [Crucial Product Page](https://www.crucial.com/ssd/t500/ct2000t500ssd8)

### Storage

=== "Seagate Exos X20 20TB"

    - `6x` 20TB Enterprise HDDs `$2490 USD`
    - [Seagate Product Page](https://www.seagate.com/products/enterprise-drives/exos-x/x20/)


### Networking

=== "QNAP QSW-1105-5T 5-Port"
    
    - `1x` 2.5Gb/s Ethernet Switch `$140 USD`
    - [QNAP Product Page](https://www.qnap.com/en-us/product/qsw-1105-5t)

=== "CAT 8 Ethernet Cables"

    - `2x` 10-ft Cable `$30 USD`
    - `1x` 3-ft Cable `$5 USD`
    - [Vabugo Amazon Store](https://www.amazon.com/stores/VABOGU/page/20815F77-3E58-4871-A2EB-1772920695D9?ref_=ast_bln)

=== "USB-C Ethernet Adapter"

    - 1x USB-C to 2.5Gb/s Ethernet Adapter `$58 USD`
    - [uni Product Page](https://uniaccessories.com/collections/all-usb-c-products/products/usb-c-to-ethernet-adapter-2500mbps)

## Price Breakdown

The prices for computer hardware vary greatly based on numerous factors. The prices included are meant to serve as an estimate and are provided based on the items' list prices.

| Type | Description | Quantity | Base | Price | 
| --- | --- | --- | --- | --- |
| System | QNAP TS-673A 6-Bay | 1 | `$899` | `$899 USD` | 
| > | TeamGroup 16GB DDR4 SODIMM | 2 | `$30` | `$60 USD` | 
| > | Crucial 2TB M.2 NVMe | 2 | `$203` | `$406 USD` | 
| Storage | Segate 20TB Enterprise HDDs | 6 | `$415` | `$2490 USD` | 
| Network | QNAP 2.5Gb/s Ethernet Switch | 1 | `$140` | `$140 USD` | 
| > | Vabugo 10ft Ethernet Cable | 2 | `$15` | `$30 USD` |
| > | Vabugo 3ft Ethernet Cable | 1 | `$5` | `$5 USD` | 
| > | uni USB-C to 2.5Gb/s Ethernet Adapter | 1 | `$58` | `$58 USD` | 
| Total |  |  |  | `$4088 USD`

!!! note "Depending on customer requirements, budget, risk appetite, and vendor discounts the price you see above is likely the most you could expect to pay."