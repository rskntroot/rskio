# Network Attached Storage

## Brief

Scoping an 138 terabyte onsite Network Attached Storage (NAS) solution for media group usage

- by `rskntroot` on `2025-02-15`

## Assumptions

To acheive redundant 138TB, RAID 6 will be used.
 This requires a total of 8x 24TB drives and is the max supported for a single chassis.

At a minimum, the storage solution must provide redundant copies of the data.
 The solution must function in the event of a single-drive failure.
 Individual storage drives used must be enterprise-grade, warrantied, with the expectation of 1 million hours MTBF.

Given standard network connectivity is at or under 1Gbps speeds, 10Gb/s internal networking is not expected.
 However, the storage solution should provide future expansion options for 10Gb/s networking.

Concerns regarding redudant power or battery backup for the solution are outside the scope of this document and would be handled by the customer.
 Recommened best practice for storage solutions is to keep on a battery backup to allow for graceful shutdown.

## Hardware

> `$7040 USD | hardware-only estimate*`

!!! warning "* Not included: shipping, taxes, build & validation services, installation support"

### Chassis

=== "UGREEN DXP8800 Plus"

    8-bay NAS: [UGREEN product page](https://nas.ugreen.com/products/ugreen-nasync-dxp8800-plus-nas-storage)

    - Intel X86 12th Generation Intel® Core™ i5
    - 10 Cores 12 Threads
    - Maximum Raw Storage: 208TB (8x 24TB + 2x 8TB)

    > `$1499 USD | Chassis`

=== "TeamGroup 64GB DDR5 SODIMM"

    2x32GB DDR5 SODIMM: [TeamGroup product page](https://www.teamgroupinc.com/en/product-detail/memory/TEAMGROUP/elite-so-dimm-ddr5/elite-so-dimm-ddr5-TED564G5600C46ADC-S01/)

    - 5-year Warranty
    - 7000 MB/s Read

    > `$150 USD | Memory`

=== "TeamGroup MP44Q 2TB NVMe"

    4TB M.2 NVME: [TeamGroup product page](https://www.teamgroupinc.com/en/product-detail/ssd/TEAMGROUP/mp44q/mp44q-TM8FFD004T0C101/)

    - 5-year Warranty
    - 7000 MB/s Read

    > `$598 USD | $299 USD (2 ea)`

### Storage

=== "Seagate Exos X24 24TB"

    Enterprise 24TB HDD: [seagate product page](https://www.seagate.com/products/enterprise-drives/exos-x/x24/)

    - 5-year limited warranty
    - 180MB/s Read (7200RPM)
    - 2.5M MTBF

    > `$4792 USD | $599 USD (8 ea)`

### Networking

=== "Ethernet Cables"

    CAT8 Ethernet Cables: [vabugo amazon store](https://www.amazon.com/stores/VABOGU/page/20815F77-3E58-4871-A2EB-1772920695D9?ref_=ast_bln)

    - 1/2.5/10/25 Gb/s support
    - 3x 10' length
    - 1x 3' length

    > `$50 USD | $15 USD (3 ea) + $5 USD (1ea)`

=== "USB-C Ethernet Adapter"

    - 2x USB-C to 2.5Gb/s Ethernet Adapter `$28 USD`
    - [uni Product Page](https://uniaccessories.com/collections/all-usb-c-products/products/usb-c-to-ethernet-adapter-2500mbps)

    > `$56 | $28 USD (2 ea)`

## Price Breakdown

Hardware pricing can vary greatly.
 The prices included are meant to serve as an estimate and are provided based on the items' list prices.

| Type | Description | Quantity | Base | Price |
| --- | --- | --- | --- | --- |
| System | UGREEN DXP8800 Plus | 1 | `$1399` | `$1399 USD` |
| > | TeamGroup 2x32GB DDR4 SODIMM | 1 | `$145` | `$145 USD` |
| > | TeamGroup 2TB M.2 NVMe | 2 | `$299` | `$598 USD` |
| Storage | Segate 24TB Enterprise HDDs | 8 | `$599` | `$4792 USD` |
| Misc | Vabugo 10ft Ethernet Cable | 3 | `$15` | `$45 USD` |
| > | Vabugo 3ft Ethernet Cable | 1 | `$5` | `$5 USD` |
| > | uni USB-C to 2.5Gb/s Ethernet Adapter | 2 | `$28` | `$56 USD` |
| Total |  |  |  | `$7040 USD` |

!!! note "Depending on customer requirements, budget, and risk appetite the price you see above is likely the most you could expect to pay."
