# Network Attached Storage

## Brief

Scoping an 80 terabyte onsite Network Attached Storage (NAS) solution for media group usage

- by `rskntroot` on `2024-06-01`

## Assmptions

At a minimum, the storage solution must provide redundant copies of the data. The solution must function in the event of a single drive. Individual storage drives used must be enterprise-grade, warrantied, with the expectation of 1 million hours Mean Time Between Failures (MTBF).

Given standard network connectivity is at or under 1Gbps speeds, 10Gb/s internal networking is not expected. However, the storage solution should provide future expansion for 10Gb/s networking.

Concerns regarding redudant power or battery backup for the solution are outside the scope of this document and would be handled by the customer. Recommened best practice for storage solutions is to keep on a battery backup to allow for graceful shutdown.

## Hardware

> `$8121 USD | hardware-only estimate*`

**Not included in estimate: shipping, taxes, build & validation services, installation support*

### NAS

#### QNAP TVS-H874T

8-bay NAS: [qnap product page](https://www.qnap.com/en-us/product/tvs-h874t/specs/hardware)
- Thunderbolt 4 support
- EZCOPY USB3.2

Available Upgrades:
- 10/25 Gb/s networking (upgrade)

> `$2899 USD | chassis`

### Drives

#### Seagate Exos X24 24TB

Enterprise 24TB HDD: [seagate product page](https://www.seagate.com/products/enterprise-drives/exos-x/x24/)
- 5-year limited warranty
- 180MB/s Read (7200RPM)
- 2.5M MTBF
- Compatibility Check [ [PASS](https://www.qnap.com/en-us/compatibility/?model=758&category=1&filter[type]=1&filter[brand]=Seagate&filter[capacity]=24000) ]

> `$4792 USD | $599 USD (8 ea)`

#### Solidgram P44 Pro

2TB M.2 NVME: [solidigm product page]( https://www.solidigm.com/products/client/pro-series/p44.html#form=M.2%202280&cap=2%20TB)
- 5-year limited warranty
- 7000 MB/s Read
- 1.6M MTBF
- Compatibility Check [ [PASS](https://www.qnap.com/en-us/compatibility/?model=758&category=1&filter[type]=1&filter[brand]=Seagate&filter[capacity]=24000) ]

> `$398 USD | $199 USD (2 ea)`

### Misc

#### Ethernet Cables

CAT8 Ethernet Cables: [vabugo amazon store](https://www.amazon.com/stores/VABOGU/page/20815F77-3E58-4871-A2EB-1772920695D9?ref_=ast_bln)
- 1/2.5/10/25 Gb/s support
- 10' length (standard)

> `$32 USD | $16 USD (2 ea)`

## Deployment Options

### Hard Drives

**8-Drives**
  - This maxes out the hardware with a capacity of `~80TB` with read speeds maxing out around `~1440MB/s`.

**6-Drives**
  - Using 6 drives will bring the total capcacity to `~60TB` and access speed maxing out at `~1080MB/s`. This saturates a 10Gbps connection.
  - Initial Cost down `$1198 USD | ($599 * 8) - ($599 * 4)`

**4-Drives**
  - The minimum capacity of 4 drives provides a capacity of `~40TB` and access speed maxing out at `~720MB/s` read. Bringing the cost down
  - Initial Cost down `$2396 USD | ($599 * 8) - ($599 * 4)`

**Future Expansion:**
  - Can we add more drives? Yes, this option is available, but requires additional hardware.
  - If it is expected to house more than 80TB in the near future, there are other options for hardware available.

*Notes:*

*2 Drives is not possible, as the requirements for "fully redundant copies of the data" and "functionality in the event of a single drive failure" mandate the use of RAID10.  The minimum drives in a RAID10 deployment is 4 drives.*

### M.2 NVME Drives

*exploring options*

### Alternate NAS

*exploring options*

